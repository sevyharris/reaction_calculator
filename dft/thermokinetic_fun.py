# set of functions related to thermokinetic calculations

import os
import glob
import sys
import numpy as np
import pandas as pd
import time
import datetime
import yaml
import job_manager

import arkane.ess.gaussian  # does a lot better at reading gaussian files than ase

import cclib.io

import autotst.species
import autotst.reaction
import autotst.calculator.gaussian
import autotst.calculator.vibrational_analysis

import ase.io.gaussian

# for arkane at end
import rmgpy.chemkin
import arkane.exceptions
import shutil


try:
    DFT_DIR = os.environ['DFT_DIR']
except KeyError:
    DFT_DIR = "/work/westgroup/harris.se/autoscience/reaction_calculator/dft"
    # DFT_DIR = "/home/moon/autoscience/reaction_calculator/dft"

#MAX_JOBS_RUNNING = 40
MAX_JOBS_RUNNING = 50


def get_termination_status(log_file):
    """Analyze a Gaussian run by reading in reverse (allegedly faster than reading from start)
    Returns:
    0 for Normal termination
    1 for Error termination not covered below
    2 for Error termination - due to all degrees of freedom being frozen
    3 for Error termination - Problem with the distance matrix.
    4 for No NMR shielding tensors so no spin-rotation constants  # TODO debug this instead of ignoring it
    5 for MANUAL SKIP
    -1 for no termination
    """
    error_termination = False
    with open(log_file, 'rb') as f:
        f.seek(0, os.SEEK_END)
        error_termination = False
        for i in range(0, 20):
            try:
                f.seek(-2, os.SEEK_CUR)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            saved_position = f.tell()
            last_line = f.readline().decode()
            f.seek(saved_position, os.SEEK_SET)
            if 'Normal termination' in last_line:
                return 0
            elif 'Error termination' in last_line:
                error_termination = True
            elif 'All variables have been frozen' in last_line:
                return 2
            elif 'Problem with the distance matrix' in last_line:
                return 3
            elif 'No NMR shielding tensors so no spin-rotation constants' in last_line:
                return 4
            elif 'MANUAL SKIP' in last_line.upper():
                return 5
        if error_termination:
            return 1
        return -1


def species_log(species_index, message):
    """Function to log messages to the species log file"""
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    logfile = os.path.join(species_dir, 'thermokinetic_fun.log')
    print(f'{datetime.datetime.now()} {message}')
    with open(logfile, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}' + '\n')


def reaction_log(reaction_index, message):
    """Function to log messages to the reaction log file"""
    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    logfile = os.path.join(reaction_dir, 'thermokinetic_fun.log')
    print(f'{datetime.datetime.now()} {message}')
    with open(logfile, 'a') as f:
        f.write(f'{datetime.datetime.now()} {message}' + '\n')


def species_index2smiles(species_index):
    """Function to return species smiles given a species index
    looks up the results in the species_list.csv
    """
    species_csv = os.path.join(DFT_DIR, 'species_list.csv')
    species_df = pd.read_csv(species_csv)
    species_index = species_df['SMILES'].values[species_index]
    return species_index


def species_smiles2index(species_smiles):
    """Function to return species index given a species smiles
    looks up the results in the species_list.csv
    """
    species_csv = os.path.join(DFT_DIR, 'species_list.csv')
    species_df = pd.read_csv(species_csv)
    try:
        species_index = species_df[species_df['SMILES'] == species_smiles]['i'].values[0]
        return species_index
    except IndexError:
        import rmgpy.species
        # now we need to check all the species for isomorphism
        ref_sp = rmgpy.species.Species(smiles=species_smiles)
        for i in range(0, len(species_df)):
            sp = rmgpy.species.Species(smiles=species_df['SMILES'].values[i])
            resonance = sp.generate_resonance_structures()
            if resonance:
                sp = resonance
            else:
                sp = [sp]
            for compare_sp in sp:
                if ref_sp.is_isomorphic(compare_sp):
                    return i
        print(f'could not identify species {species_smiles}')


def reaction_index2smiles(reaction_index):
    """Function to return reaction smiles given a reaction index
    looks up the results in the reaction_list.csv
    """
    reaction_csv = os.path.join(DFT_DIR, 'reaction_list.csv')
    reaction_df = pd.read_csv(reaction_csv)
    reaction_smiles = reaction_df['SMILES'].values[reaction_index]
    return reaction_smiles


def reaction2smiles(reaction):
    """Takes an RMG reaction and returns the smiles representation
    """
    string = ""
    for react in reaction.reactants:
        if isinstance(react, rmgpy.species.Species):
            string += f"{react.molecule[0].to_smiles()}+"
        elif isinstance(react, rmgpy.molecule.Molecule):
            string += f"{react.to_smiles()}+"
    string = string[:-1]
    string += "_"
    for prod in reaction.products:
        if isinstance(prod, rmgpy.species.Species):
            string += f"{prod.molecule[0].to_smiles()}+"
        elif isinstance(prod, rmgpy.molecule.Molecule):
            string += f"{prod.to_smiles()}+"
    label = string[:-1]
    return label


def smiles2reaction(reaction_smiles):
    """Takes the reaction smiles and produces a corresponding rmg reaction
    """
    reaction = rmgpy.reaction.Reaction()
    reactants = []
    products = []

    # handle CO case
    if '[C-]#[O+]' in reaction_smiles:
        CO = rmgpy.species.Species(smiles='[C-]#[O+]')
        reaction_smiles = reaction_smiles.replace('[C-]#[O+]', 'carbonmonoxide')
    if '[O-][N+]#C' in reaction_smiles:
        CHNO = rmgpy.species.Species(smiles='[O-][N+]#C')
        reaction_smiles = reaction_smiles.replace('[O-][N+]#C', 'formonitrileoxide')
    if '[O-][N+]=C' in reaction_smiles:
        CH2NO = rmgpy.species.Species(smiles='[O-][N+]=C')
        reaction_smiles = reaction_smiles.replace('[O-][N+]=C', 'methylenenitroxide')

    reactant_token = reaction_smiles.split('_')[0]
    product_token = reaction_smiles.split('_')[1]

    reactant_tokens = reactant_token.split('+')
    product_tokens = product_token.split('+')

    # print(product_tokens)
    for reactant_str in reactant_tokens:
        if reactant_str == 'carbonmonoxide':
            reactant_str = '[C-]#[O+]'
        elif reactant_str == 'formonitrileoxide':
            reactant_str = '[O-][N+]#C'
        elif reactant_str == 'methylenenitroxide':
            reactant_str = '[O-][N+]=C'
        reactant = rmgpy.species.Species(smiles=reactant_str)
        reactants.append(reactant)

    for product_str in product_tokens:
        if product_str == 'carbonmonoxide':
            product_str = '[C-]#[O+]'
        elif product_str == 'formonitrileoxide':
            product_str = '[O-][N+]#C'
        elif product_str == 'methylenenitroxide':
            ptoduct_str = '[O-][N+]=C'
        # print(product_str)
        product = rmgpy.species.Species(smiles=product_str)
        products.append(product)

    reaction.reactants = reactants
    reaction.products = products
    return reaction


def reaction_smiles2index(reaction_smiles):
    """Function to return reaction index given a smiles reaction
    doesn't necessarily have to be in the right order
    RMG reaction will check for isomorphism
    """
    # first check to see if the exact smiles is in the CSV
    reaction_csv = os.path.join(DFT_DIR, 'reaction_list.csv')
    reaction_df = pd.read_csv(reaction_csv)
    if reaction_smiles in reaction_df['SMILES'].values:
        idx = np.where(reaction_df['SMILES'].values == reaction_smiles)[0][0]
        return reaction_df['i'].values[idx]
    else:
        # use rmgpy.reaction to check for isomorphism
        ref_reaction = smiles2reaction(reaction_smiles)
        for i in range(0, len(reaction_df)):
            csv_reaction = smiles2reaction(reaction_df['SMILES'].values[i])
            if ref_reaction.is_isomorphic(csv_reaction):
                return i
    # reaction not found
    return -1


def get_species_status(species_index, job_type):
    """Check the status of the part of the species calculation by looking in the status file
    Possibilities are:
        - screen_conformers - complete if the conformer optimization files have been generated
        - conformer_opt - run Gaussian to optimize the conformers
    """
    status_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'status.yaml')
    if not os.path.exists(status_file):
        return False
    with open(status_file, 'r') as f:
        try:
            status = yaml.load(f, Loader=yaml.FullLoader)
        except AttributeError:
            status = yaml.safe_load(f)
    if job_type in status:
        return status[job_type]
    return False


def get_reaction_status(reaction_index, job_type):
    """Check the status of the part of the reaction calculation by looking in the status file
    Possibilities are:
        - shell_setup
        - center_setup
        - overall_setup
        - shell_opt - run Gaussian to optimize the conformers
        - center_opt
        - overall_opt
        - arkane?
    """
    status_file = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'status.yaml')
    if not os.path.exists(status_file):
        return False
    with open(status_file, 'r') as f:
        try:
            status = yaml.load(f, Loader=yaml.FullLoader)
        except AttributeError:
            status = yaml.safe_load(f)
    if job_type in status:
        return status[job_type]
    return False


def set_species_status(species_index, job_type, job_status):
    """Set the status of the part of the species calculation by writing the status file
    Possibilities are:
        - screen_conformers - complete if the conformer optimization files have been generated
        - conformer_opt - run Gaussian to optimize the conformers
    """
    status_file = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'status.yaml')
    status = {}
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                status = yaml.load(f, Loader=yaml.FullLoader)
            except AttributeError:
                status = yaml.safe_load(f)
    status[job_type] = job_status
    with open(status_file, 'w') as f:
        yaml.dump(status, f)


def set_reaction_status(reaction_index, job_type, job_status):
    """Set the status of the part of the reaction calculation by writing the status file
    Possibilities are:
        # TODO delete screen_conformers?
        - shell_setup
        - center_setup
        - overall_setup
        - shell_opt - run Gaussian to optimize the conformers
        - center_opt
        - overall_opt
        - arkane?
    """
    status_file = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'status.yaml')
    status = {}
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                status = yaml.load(f, Loader=yaml.FullLoader)
            except AttributeError:
                status = yaml.safe_load(f)
    status[job_type] = job_status
    with open(status_file, 'w') as f:
        yaml.dump(status, f)


def ordered_array_str(list_of_indices):
    # convenient script for putting a list of task numbers into a string that can be used for a SLURM array job
    # assume it's sorted
    if len(list_of_indices) == 1:
        return str(list_of_indices[0])
    elif len(list_of_indices) == 2:
        return f'{list_of_indices[0]},{list_of_indices[1]}'

    array_str = str(list_of_indices[0]) + '-'
    for j in range(1, len(list_of_indices) - 1):
        if list_of_indices[j] - list_of_indices[j - 1] != 1:
            if j > 1:
                array_str += str(list_of_indices[j - 1])
                array_str += f',{list_of_indices[j]}-'
            else:
                array_str = array_str.replace('-', ',')
                array_str += f'{list_of_indices[j]}-'
        # cap the end
        if j + 2 == len(list_of_indices):
            if list_of_indices[j + 1] - list_of_indices[j] != 1:
                array_str += f'{list_of_indices[j]},{list_of_indices[j + 1]}'
            else:
                array_str += f'{list_of_indices[j + 1]}'

    return array_str


def screen_species_conformers(species_index):
    """Sort through all the possible conformers and use a cheap calculator
    like Hotbit or LJ to screen the best options to investigate

    Takes a species index and saves the conformers to investigate as .pickle?
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    if get_species_status(species_index, 'screen_conformers'):
        species_log(species_index, 'Conformers already screened')
        return True

    conformer_dir = os.path.join(species_dir, 'conformers')
    os.makedirs(conformer_dir, exist_ok=True)
    species_log(species_index, f'Starting conformer screening job')

    # ------------------ Use Hotbit to screen the conformers ------------------
    # Get species smiles
    species_smiles = species_index2smiles(species_index)
    spec = autotst.species.Species([species_smiles])
    species_log(species_index, f'Loaded species {species_smiles}')

    try:
        import hotbit
        calc = hotbit.Hotbit()
    except (ImportError, RuntimeError):
        # if hotbit fails, use built-in lennard jones
        import ase.calculators.lj
        species_log(species_index, 'Using built-in ase LennardJones calculator instead of Hotbit')
        calc = ase.calculators.lj.LennardJones()
    # hotbit can't handle Ar, He, change calculator to lj if it's in the species
    hotbit_skiplist = ['AR', 'HE', 'NE']
    for element in hotbit_skiplist:
        if element in species_smiles.upper():
            import ase.calculators.lj
            species_log(species_index, f'Using built-in ase LennardJones calculator instead of Hotbit for {element}')
            calc = ase.calculators.lj.LennardJones()
            break

    spec.generate_conformers(
        ase_calculator=calc,
        max_combos=10000,
        max_conformers=1000,
        results_dir=conformer_dir,
        save_results=True,
    )

    n_conformers = 0
    for key in spec.conformers:
        n_conformers += len(spec.conformers[key])
    species_log(species_index, f'{n_conformers} found with {str(calc)}')

    # ------------------ Use Gaussian to do a more detailed calculation ------------------
    species_log(species_index, "Generating gaussian input files")
    save_offset = 0
    for resonance_smiles in spec.conformers.keys():
        for i, cf in enumerate(spec.conformers[resonance_smiles]):
            conformer_index = i + save_offset
            gaussian = autotst.calculator.gaussian.Gaussian(conformer=cf)
            calc = gaussian.get_conformer_calc()
            calc.label = f'conformer_{conformer_index:04}'
            calc.directory = conformer_dir
            calc.parameters.pop('scratch')
            calc.parameters.pop('multiplicity')
            calc.parameters['mult'] = cf.rmg_molecule.multiplicity
            calc.chk = f'conformer_{conformer_index:04}.chk'
            calc.write_input(cf.ase_molecule)
        save_offset += len(spec.conformers[resonance_smiles])

    # write to the status file to indicate that the conformer screening is complete
    set_species_status(species_index, 'screen_conformers', True)
    species_log(species_index, f'Conformer screening complete')
    return True


def optimize_conformers(species_index):
    """Optimize the conformers that were screened"""
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    species_log(species_index, f'Starting conformer optimization job')

    # check if the run was already completed
    if get_species_status(species_index, 'conformer_opt'):
        species_log(species_index, f'Conformer optimization already ran')
        return True
    if conformers_done_optimizing(conformer_dir):
        species_log(species_index, f'Conformer optimization already ran')
        set_species_status(species_index, 'conformer_opt', True)
        return True

    n_conformers = len(glob.glob(os.path.join(conformer_dir, 'conformer_*.com')))
    rerun_indices = []
    for i in range(0, n_conformers):
        conformer_logfile = os.path.join(conformer_dir, f'conformer_{i:04}.log')
        if os.path.exists(conformer_logfile):
            termination_status = get_termination_status(conformer_logfile)
            if termination_status == 1 or termination_status == -1:
                rerun_indices.append(i)

    # Make slurm script to run all the conformer calculations
    slurm_run_file = os.path.join(conformer_dir, 'run.sh')
    slurm_settings = {
        '--job-name': f'g16_cf_{species_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'west,short',
        '--exclude': 'c5003',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-{n_conformers - 1}%30',
    }
    if rerun_indices:
        slurm_run_file = os.path.join(conformer_dir, 'rerun.sh')
        slurm_settings['--partition'] = 'short'
        slurm_settings['--constraint'] = 'cascadelake'
        slurm_settings['--array'] = ordered_array_str(rerun_indices)
        slurm_settings['--cpus-per-task'] = 32
        slurm_settings.pop('--exclude')

    slurm_file_writer = job_manager.SlurmJobFile(
        full_path=slurm_run_file,
    )
    slurm_file_writer.settings = slurm_settings
    slurm_file_writer.content = [
        'export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n',
        'mkdir -p $GAUSS_SCRDIR\n',
        'module load gaussian/g16\n',
        'source /shared/centos7/gaussian/g16/bsd/g16.profile\n\n',

        'RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n',
        'fname="conformer_${RUN_i}.com"\n\n',

        'g16 $fname\n',
    ]
    slurm_file_writer.write_file()

    # submit the job
    start_dir = os.getcwd()
    os.chdir(conformer_dir)
    gaussian_conformers_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {slurm_run_file}"

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    gaussian_conformers_job.submit(slurm_cmd)
    os.chdir(start_dir)


def conformers_done_optimizing(base_dir, completion_threshold=0.6, base_name='conformer_'):
    """function to see if all the conformers are done optimizing, returns True if so"""
    n_conformers = len(glob.glob(os.path.join(base_dir, f'{base_name}*.com')))
    if n_conformers == 0:
        return False
        # print(f'No conformers with basename {base_name} found in {base_dir}')
    incomplete_indices = []
    good_runs = []
    finished_runs = []
    for i in range(0, n_conformers):
        conformer_file = os.path.join(base_dir, f'{base_name}{i:04}.log')
        if not os.path.exists(conformer_file):
            return False
        opt_status = get_termination_status(conformer_file)
        if opt_status == 0:
            good_runs.append(i)
            finished_runs.append(i)
        elif opt_status == 2 or opt_status == 3 or opt_status == 4 or opt_status == 5:
            # not good optimizations, but we're going to keep going anyways
            finished_runs.append(i)
        else:
            # optimization didn't finish
            incomplete_indices.append(i)
    # print(len(finished_runs) / float(n_conformers))
    if len(finished_runs) / float(n_conformers) >= completion_threshold and len(good_runs) > 0:
        return True
    return False


def wait_for_conformer_opt(species_index):
    """Wait for the conformer optimization to finish"""
    # check if the run was already completed
    if get_species_status(species_index, 'conformer_opt'):
        species_log(species_index, f'Conformer optimization already ran')
        return True

    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    opt_completed = conformers_done_optimizing(conformer_dir)
    while not opt_completed:
        time.sleep(60)
        opt_completed = conformers_done_optimizing(conformer_dir)

    # write to the status file to indicate that the conformer screening is complete
    set_species_status(species_index, 'conformer_opt', True)
    species_log(species_index, f'Conformer optimization complete')


def arkane_species_complete(species_index):
    """Function to check whether the arkane job is complete for a species
    Expects to find the following directory structure:
    DFT_DIR/thermo/species_XXXX/arkane/RMG_libraries/thermo.py
    Returns True if complete, False otherwise
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    arkane_result = os.path.join(species_dir, 'arkane', 'RMG_libraries', 'thermo.py')
    return os.path.exists(arkane_result)


def get_gaussian_file_energy(gaussian_log_file):
    """Function to get the energy from a Gaussian .log file"""
    with open(gaussian_log_file, 'r') as f:
        # check that it's really a gaussian file
        line = f.readline()
        if 'Gaussian' not in line:
            return None
        f.seek(0)
        gl = arkane.ess.gaussian.GaussianLog(gaussian_log_file, check_for_errors=False)
        return gl.load_energy()


def get_gaussian_file_geometry(gaussian_log_file):
    """Function to get the ase atoms object from a Gaussian .log file"""
    with open(gaussian_log_file, 'r') as f:
        # check that it's really a gaussian file
        line = f.readline()
        if 'Gaussian' not in line:
            return None
        f.seek(0)
        atoms = ase.io.gaussian.read_gaussian_out(f)
        return atoms


def get_lowest_energy_gaussian_file(base_dir):
    """Function to get the lowest energy gaussian .log file from a directory"""
    lowest_energy = 1e6
    lowest_file = None
    log_files = glob.glob(os.path.join(base_dir, '*.log'))
    for gaussian_log_file in log_files:
        energy = get_gaussian_file_energy(gaussian_log_file)
        if energy is None:
            continue
        if energy < lowest_energy:
            lowest_energy = energy
            lowest_file = gaussian_log_file
    return lowest_file


def get_rotor_info(conformer, torsion, torsion_index):
    _, j, k, _ = torsion.atom_indices

    # Adjusted since mol's IDs start from 0 while Arkane's start from 1
    tor_center_adj = [j + 1, k + 1]

    tor_log = f'rotor_{torsion_index:04}.log'
    top_IDs = []
    for num, tf in enumerate(torsion.mask):
        if tf:
            top_IDs.append(num)

    # Adjusted to start from 1 instead of 0
    top_IDs_adj = [ID + 1 for ID in top_IDs]

    info = f"     HinderedRotor(scanLog=Log('{tor_log}'), pivots={tor_center_adj}, top={top_IDs_adj}, fit='fourier'),"

    return info


def write_arkane_conformer_file(conformer, gauss_log, arkane_dir, include_rotors=False):
    # assume rotor and conformer logs have already been copied into the arkane directory
    species_name = os.path.basename(gauss_log[:-4])
    parser = cclib.io.ccread(gauss_log)
    symbol_dict = {
        35: "Br",
        17: "Cl",
        9: "F",
        8: "O",
        7: "N",
        6: "C",
        1: "H",
        18: "Ar",
        2: "He",
        10: "Ne",
    }

    atoms = []

    for atom_num, coords in zip(parser.atomnos, parser.atomcoords[-1]):
        atoms.append(ase.Atom(symbol=symbol_dict[atom_num], position=coords))

    conformer._ase_molecule = ase.Atoms(atoms)
    conformer.update_coords_from("ase")
    output = ['#!/usr/bin/env python',
              '# -*- coding: utf-8 -*-', ]

    output += ["", f"spinMultiplicity = {conformer.rmg_molecule.multiplicity}", ""]
    model_chemistry = 'M06-2X/cc-pVTZ'

    # use relative path for easy transfer -- assume we will copy the log files into the Arkane folder
    gauss_log_relative = os.path.basename(gauss_log)
    output += ["energy = {", f"    '{model_chemistry}': Log('{gauss_log_relative}'),", "}", ""]  # fix this

    output += [f"geometry = Log('{gauss_log_relative}')", ""]
    output += [
        f"frequencies = Log('{gauss_log_relative}')", ""]

    # get the rotors
    torsions = conformer.get_torsions()
    n_rotors = len(torsions)

    if include_rotors and n_rotors > 0:
        output += ["rotors = ["]
        if len(conformer.torsions) == 0:
            conformer.get_molecules()
            conformer.get_geometries()
        for i, torsion in enumerate(conformer.torsions):
            output += [get_rotor_info(conformer, torsion, i)]
        output += ["]"]

    input_string = ""

    for t in output:
        input_string += t + "\n"

    with open(os.path.join(arkane_dir, species_name + '.py'), "w") as f:
        f.write(input_string)
    return True


def setup_arkane_species(species_index, include_rotors=False):
    """Function to set up the Arkane species directory for a given species
    default is to not do rotors. But if rotors are specified, the arkane directory
    will be arkane_rotors
    """
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    conformer_dir = os.path.join(species_dir, 'conformers')
    arkane_dir = os.path.join(species_dir, 'arkane')
    os.makedirs(arkane_dir, exist_ok=True)
    if include_rotors:
        arkane_dir = os.path.join(species_dir, 'arkane_rotors')
    species_log(species_index, f'Setting up Arkane species')
    if arkane_species_complete(species_index):
        species_log(species_index, f'Arkane species already complete')
        return True

    species_smiles = species_index2smiles(species_index)
    # make a conformer object from the SMILES
    new_cf = autotst.species.Conformer(smiles=species_smiles)
    # read the conformer geometry from the file
    conformer_file = get_lowest_energy_gaussian_file(conformer_dir)

    shutil.copy(conformer_file, arkane_dir)
    with open(conformer_file, 'r') as f:
        atoms = ase.io.gaussian.read_gaussian_out(f)

    new_cf._ase_molecule = atoms
    new_cf.update_coords_from(mol_type="ase")

    if include_rotors:
        rotor_dir = os.path.join(species_dir, 'rotors')
        torsions = new_cf.get_torsions()
        for i, torsion in enumerate(torsions):
            # TODO check for valid output
            torfile = os.path.join(rotor_dir, f'rotor_{i:04}.log')
            shutil.copy(torfile, arkane_dir)

    # write the Arkane conformer file
    write_arkane_conformer_file(new_cf, conformer_file, arkane_dir, include_rotors=include_rotors)

    # write the Arkane input file
    input_file = os.path.join(arkane_dir, 'input.py')
    formula = new_cf.rmg_molecule.get_formula()
    lines = [
        '#!/usr/bin/env python\n\n',
        f'modelChemistry = "M06-2X/cc-pVTZ"\n',
        f'useHinderedRotors = {include_rotors}' + '\n',
        'useBondCorrections = False\n\n',

        'frequencyScaleFactor = 0.982\n',

        f"species('{formula}', '{os.path.basename(conformer_file[:-4])}.py', structure=SMILES('{new_cf.rmg_molecule.smiles}'))\n\n",

        f"thermo('{formula}', 'NASA')\n",
    ]
    with open(input_file, 'w') as f:
        f.writelines(lines)

    # copy a run script into the arkane directory
    run_script = os.path.join(arkane_dir, 'run_arkane.sh')
    with open(run_script, 'w') as f:
        # Run on express
        f.write('#!/bin/bash\n')
        f.write('#SBATCH --partition=express,short,west\n')
        f.write('#SBATCH --time=00:20:00\n\n')
        f.write('python ~/rmg/RMG-Py/Arkane.py input.py\n\n')


def run_arkane_species(species_index):
    # Run the arkane job
    
    species_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}')
    arkane_dir = os.path.join(species_dir, 'arkane')

    if arkane_species_complete(species_index):
        species_log(species_index, f'arkane already ran for species {species_index}')
        return True

    # Run the arkane job
    arkane_run_file = os.path.join(arkane_dir, 'run_arkane.sh')
    if not os.path.exists(arkane_run_file):
        species_log(species_index, f'arkane run not set up for species {species_index}')
        return False

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    start_dir = os.getcwd()
    os.chdir(arkane_dir)
    arkane_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {arkane_run_file}"
    arkane_job.submit(slurm_cmd)
    os.chdir(start_dir)


def delete_double_spaces(gaussian_com_file):
    # Get rid of first double-linespace found,
    # usually between xyz and modredundant sections
    double_space = False
    lines = []
    with open(gaussian_com_file, 'r') as f:
        lines = f.readlines()
        for j in range(1, len(lines)):
            if lines[j] == '\n' and lines[j - 1] == '\n':
                double_space = True
                break
    if double_space:
        lines = lines[0:j - 1] + lines[j:]
        with open(gaussian_com_file, 'w') as f:
            f.writelines(lines)


def setup_opt(reaction_index, opt_type, direction='forward', max_combos=1000, max_conformers=100):
    """Function to set up the gaussian files for a particular opt type
    screens the conformers using hotbit, then writes the gaussian input files
    types are 'shell', 'center', 'overall'

    shell freezes 3 core atoms of reaction and relaxes the rest of the molecule
    center optimizes 3 core atoms of reaction to TS and freezes the rest of the molecule
    overall optimizes the entire molecule to TS
    """

    assert opt_type in ['shell', 'center', 'overall'], f'opt_type must be one of shell, center, overall. Got {opt_type}'

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    if not os.path.exists(reaction_dir):
        os.makedirs(reaction_dir, exist_ok=True)
    screen_dir = os.path.join(reaction_dir, 'screen')
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir, exist_ok=True)
    reaction_log(reaction_index, f'Starting {opt_type} opt job')

    # check if the opt setup is already complete
    if get_reaction_status(reaction_index, f'{opt_type}_setup') or \
       get_reaction_status(reaction_index, f'{opt_type}_opt'):
        reaction_log(reaction_index, f'{opt_type} opt setup complete')
        return True

    screen_dir = os.path.join(reaction_dir, 'screen')
    opt_dir = os.path.join(reaction_dir, opt_type)
    os.makedirs(opt_dir, exist_ok=True)

    opt_label = 'fwd_ts_0000.log'
    if direction == 'reverse':
        opt_label = 'rev_ts_0000.log'

    # don't run center if shell isn't complete and
    # don't run overall if center isn't complete
    if opt_type == 'center':
        shell_dir = os.path.join(reaction_dir, 'shell')
        if get_reaction_status(reaction_index, 'shell_opt'):
            pass
        elif conformers_done_optimizing(shell_dir, base_name=opt_label[:-8]):
            set_reaction_status(reaction_index, 'shell_opt', True)
        else:
            reaction_log(reaction_index, f'Center opt setup incomplete, shell opt not complete')
            return False
    elif opt_type == 'overall':
        center_dir = os.path.join(reaction_dir, 'center')
        if get_reaction_status(reaction_index, 'center_opt'):
            pass
        elif conformers_done_optimizing(center_dir, base_name=opt_label[:-8]):
            set_reaction_status(reaction_index, 'center_opt', True)
        else:
            reaction_log(reaction_index, f'Overall opt setup incomplete, center opt not complete')
            return False

    # ------------------ Use Hotbit to screen the conformers ------------------
    # Get reaction smiles
    reaction_smiles = reaction_index2smiles(reaction_index)
    reaction_log(reaction_index, f'Constructing reaction in AutoTST...')
    reaction = autotst.reaction.Reaction(label=reaction_smiles)

    reaction.ts[direction][0].get_molecules()
    try:  # TODO fix issues with import in a try block
        import hotbit
        calc = hotbit.Hotbit()
    except (ImportError, RuntimeError):
        # if hotbit fails, use built-in lennard jones
        import ase.calculators.lj
        reaction_log(reaction_index, 'Using built-in ase LennardJones calculator instead of Hotbit')
        calc = ase.calculators.lj.LennardJones()
    reaction.generate_conformers(
        ase_calculator=calc,
        max_combos=max_combos,
        max_conformers=max_conformers,
        save_results=True,
        results_dir=screen_dir,
    )
    reaction_log(reaction_index, f'Done generating conformers in AutoTST...')
    reaction_log(reaction_index, f'{len(reaction.ts[direction])} conformers found')

    # -------------- Write the results as gaussiuan calculations in the shell dir
    # Check for already finished shell logfiles
    # first, return if all of them have finished
    for i in range(0, len(reaction.ts[direction])):
        opt_label = opt_label[:-8] + f'{i:04}.log'

        ts = reaction.ts[direction][i]
        gaussian = autotst.calculator.gaussian.Gaussian(conformer=ts)
        if opt_type == 'shell':
            calc = gaussian.get_shell_calc()
        elif opt_type == 'center':
            calc = gaussian.get_center_calc()
        elif opt_type == 'overall':
            calc = gaussian.get_overall_calc()
        else:
            raise ValueError(f'opt_type must be one of shell, center, overall. Got {opt_type}')
        calc.label = opt_label[:-4]
        calc.directory = opt_dir
        calc.parameters.pop('scratch')
        calc.parameters.pop('multiplicity')
        calc.parameters['mult'] = ts.rmg_molecule.multiplicity
        calc.write_input(ts.ase_molecule)

        # Get rid of double-space between xyz block and mod-redundant section
        delete_double_spaces(os.path.join(opt_dir, calc.label + '.com'))

    # write to the status file to indicate that the conformer screening is complete
    set_reaction_status(reaction_index, f'{opt_type}_setup', True)
    reaction_log(reaction_index, f'{opt_type} setup complete')
    return True


def run_opt(reaction_index, opt_type, direction='forward'):
    """Run a shell, center, or overall optimization
    opt_type can be 'shell', 'center', or 'overall'
    """
    assert opt_type in ['shell', 'center', 'overall']

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    opt_dir = os.path.join(reaction_dir, opt_type)

    if not os.path.exists(opt_dir):
        reaction_log(reaction_index, f'{opt_type} optimization not set up yet')
        return False

    reaction_log(reaction_index, f'Starting {opt_type} optimization job')

    # manually check if the center optimizations are complete
    opt_label = 'fwd_ts_0000.log'
    if direction == 'reverse':
        opt_label = 'rev_ts_0000.log'

    # check if the run was already completed
    if get_reaction_status(reaction_index, f'{opt_type}_opt'):
        reaction_log(reaction_index, f'{opt_type} optimization already ran')
        return True
    elif conformers_done_optimizing(opt_dir, base_name=opt_label[:-8]):
        reaction_log(reaction_index, f'{opt_type} optimization already ran')
        set_reaction_status(reaction_index, f'{opt_type}_opt', True)
        return True

    n_conformers = len(glob.glob(os.path.join(opt_dir, f'{opt_label[:-8]}*.com')))
    rerun_indices = []
    for i in range(0, n_conformers):
        conformer_logfile = os.path.join(opt_dir, f'{opt_label[:-8]}{i:04}.log')
        if os.path.exists(conformer_logfile):
            termination_status = get_termination_status(conformer_logfile)
            if termination_status == 1 or termination_status == -1:
                rerun_indices.append(i)

    # Make slurm script to run all the conformer calculations
    slurm_run_file = os.path.join(opt_dir, 'run.sh')
    slurm_settings = {
        '--job-name': f'g16_{opt_type}_{reaction_index}',
        '--error': 'error.log',
        '--nodes': 1,
        '--partition': 'west,short',
        '--exclude': 'c5003',
        '--mem': '20Gb',
        '--time': '24:00:00',
        '--cpus-per-task': 16,
        '--array': f'0-{n_conformers - 1}%30',
    }
    if rerun_indices:
        slurm_run_file = os.path.join(opt_dir, 'rerun.sh')
        slurm_settings['--partition'] = 'short'
        slurm_settings['--constraint'] = 'cascadelake'
        slurm_settings['--array'] = ordered_array_str(rerun_indices)
        slurm_settings['--cpus-per-task'] = 32
        slurm_settings.pop('--exclude')

    slurm_file_writer = job_manager.SlurmJobFile(
        full_path=slurm_run_file,
    )
    slurm_file_writer.settings = slurm_settings
    slurm_file_writer.content = [
        'export GAUSS_SCRDIR=/scratch/harris.se/guassian_scratch\n',
        'mkdir -p $GAUSS_SCRDIR\n',
        'module load gaussian/g16\n',
        'source /shared/centos7/gaussian/g16/bsd/g16.profile\n\n',

        'RUN_i=$(printf "%04.0f" $(($SLURM_ARRAY_TASK_ID)))\n',
        f'fname="{opt_label[:-8]}' + '${RUN_i}.com"\n\n',

        'g16 $fname\n',
    ]
    slurm_file_writer.write_file()

    # submit the job
    start_dir = os.getcwd()
    os.chdir(opt_dir)
    gaussian_opt_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {slurm_run_file}"

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()
    reaction_log(reaction_index, f'Running SLURM job: {slurm_cmd}')
    gaussian_opt_job.submit(slurm_cmd)
    os.chdir(start_dir)


def check_vib_irc(reaction_index, gaussian_logfile):
    """Function to check if the TS optimization was successful
    """
    # check for valid termination status
    termination_status = get_termination_status(gaussian_logfile)
    if termination_status != 0:
        print('logfile did not terminate normally')
        return False

    reaction_smiles = reaction_index2smiles(reaction_index)
    reaction = autotst.reaction.Reaction(label=reaction_smiles)
    va = autotst.calculator.vibrational_analysis.VibrationalAnalysis(
        transitionstate=reaction.ts['forward'][0], log_file=gaussian_logfile
    )
    result = va.validate_ts()
    if result:
        print('TS is valid')
    else:
        print('TS is not valid')
    return result


def arkane_reaction_complete(reaction_index):
    return os.path.exists(os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}', 'arkane', 'RMG_libraries', 'reactions.py'))


def setup_arkane_reaction(reaction_index, direction='forward', force_valid_ts=False):
    """Function to setup the arkane job for a reaction
    """
    # check if the arkane job was already completed
    if get_reaction_status(reaction_index, 'arkane_calc'):
        re(reaction_index, 'Arkane job already ran')
        return True
    elif arkane_reaction_complete(reaction_index):
        set_reaction_status(reaction_index, 'arkane_setup', True)
        set_reaction_status(reaction_index, 'arkane_calc', True)
        reaction_log(reaction_index, 'Arkane job already ran')
        return True

    ## Check for overall job status completion
    #if not get_reaction_status(reaction_index, 'overall_opt'):
    #    reaction_log(reaction_index, 'Cannot run arkane until overall job is complete')
    #    return False

    reaction_smiles = reaction_index2smiles(reaction_index)
    reaction_log(reaction_index, f'starting setup_arkane_reaction for reaction {reaction_index} {reaction_smiles}')

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    overall_dir = os.path.join(reaction_dir, 'overall')
    arkane_dir = os.path.join(reaction_dir, 'arkane')
    os.makedirs(arkane_dir, exist_ok=True)

    species_dict_file = "/work/westgroup/harris.se/autoscience/autoscience/butane/models/rmg_model/species_dictionary.txt"
    species_dict = rmgpy.chemkin.load_species_dictionary(species_dict_file)

    def get_sp_name(smiles):
        if smiles == '[CH2]C=CC':  # manually change to resonance structures included in model
            smiles = 'C=C[CH]C'
        elif smiles == '[CH2][CH]C=C':
            smiles = '[CH2]C=C[CH2]'
        for entry in species_dict.keys():
            if species_dict[entry].smiles == smiles:
                return str(species_dict[entry])
        # need to look for isomorphism
        print(f'Failed to get species name for {smiles}')
        return smiles

    def get_reaction_label(rmg_reaction):
        label = ''
        for reactant in rmg_reaction.reactants:
            label += get_sp_name(reactant.smiles) + ' + '
        label = label[:-2]
        label += '<=> '
        for product in rmg_reaction.products:
            label += get_sp_name(product.smiles) + ' + '
        label = label[:-3]
        return label

    # Read in the reaction
    reaction_smiles = reaction_index2smiles(reaction_index)
    reaction = autotst.reaction.Reaction(label=reaction_smiles)
    reaction_log(reaction_index, f'Creating arkane files for reaction {reaction_index} {reaction.label}')
    reaction.ts[direction][0].get_molecules()

    # pick the lowest energy valid transition state:
    TS_logs = glob.glob(os.path.join(overall_dir, f'fwd_ts_*.log'))
    TS_log = ''
    lowest_energy = 1e5
    for logfile in TS_logs:
        # skip if the TS is not valid
        if not force_valid_ts:
            if not check_vib_irc(reaction_index, logfile):
                continue

        try:
            g_reader = arkane.ess.gaussian.GaussianLog(logfile)
            energy = g_reader.load_energy()
            if energy < lowest_energy:
                lowest_energy = energy
                TS_log = logfile
        except arkane.exceptions.LogError:
            print(f'skipping bad logfile {logfile}')
            continue
    if not TS_log:
        raise ValueError('No Valid TS found')

    # -------------------- Write the input file ---------------------- #
    model_chemistry = 'M06-2X/cc-pVTZ'
    lines = [
        f'modelChemistry = "{model_chemistry}"\n',
        'useHinderedRotors = False\n',
        'useBondCorrections = False\n\n',
    ]

    completed_species = []
    for reactant in reaction.rmg_reaction.reactants + reaction.rmg_reaction.products:
        # check for duplicates
        duplicate = False
        for sp in completed_species:
            if reactant.is_isomorphic(sp):
                duplicate = True
        if duplicate:
            continue

        species_smiles = reactant.smiles
        if species_smiles == '[CH2]C=CC':  # TODO clean up this fix where we manually switch back to other resonance structure
            species_smiles = 'C=C[CH]C'
        elif species_smiles == '[CH2][CH]C=C':
            species_smiles = '[CH2]C=C[CH2]'
        species_name = get_sp_name(species_smiles)
        species_index = species_smiles2index(species_smiles)
        species_arkane_dir = os.path.join(DFT_DIR, 'thermo', f'species_{species_index:04}', 'arkane')
        try:
            species_file = os.path.join(f'species_{species_index:04}', os.path.basename(glob.glob(os.path.join(species_arkane_dir, 'conformer_*.py'))[0]))
        except IndexError:
            raise IndexError(f'No species conformer file found in {species_arkane_dir}')        

        try:
            shutil.copytree(species_arkane_dir, os.path.join(arkane_dir, f'species_{species_index:04}'))
        except FileExistsError:
            pass

        # TODO - copy the species into the destination so the arkane calculation can be copied and redone elsewhere
        lines.append(f'species("{species_name}", "{species_file}", structure=SMILES("{species_smiles}"))\n')
        lines.append(f'thermo("{species_name}", "NASA")\n\n')

        completed_species.append(reactant)

    lines.append('\n')

    TS_name = 'TS'
    TS_file = 'TS.py'
    TS_arkane_path = os.path.join(arkane_dir, TS_file)
    shutil.copy(TS_log, arkane_dir)

    lines.append(f'transitionState("{TS_name}", "{TS_file}")\n')

    reaction_label = get_reaction_label(reaction.rmg_reaction)
    reactants = [get_sp_name(reactant.smiles) for reactant in reaction.rmg_reaction.reactants]
    products = [get_sp_name(product.smiles) for product in reaction.rmg_reaction.products]
    lines.append(f'reaction(\n')
    lines.append(f'    label = "{reaction_label}",\n')
    lines.append(f'    reactants = {reactants},\n')
    lines.append(f'    products = {products},\n')
    lines.append(f'    transitionState = "{TS_name}",\n')
    lines.append(f'#    tunneling = "Eckart",\n')
    lines.append(f')\n\n')

    lines.append(f'statmech("{TS_name}")\n')
    lines.append(f'kinetics("{reaction_label}")\n\n')

    # write the TS file
    ts_lines = [
        'energy = {"' + f'{model_chemistry}": Log("{os.path.basename(TS_log)}")' + '}\n\n',
        'geometry = Log("' + f'{os.path.basename(TS_log)}")' + '\n\n',
        'frequencies = Log("' + f'{os.path.basename(TS_log)}")' + '\n\n',
    ]
    with open(TS_arkane_path, 'w') as g:
        g.writelines(ts_lines)

    arkane_input_file = os.path.join(arkane_dir, 'input.py')
    with open(arkane_input_file, 'w') as f:
        f.writelines(lines)
    # ----------------------------------------------------------------- #

    # make the slurm script to run arkane
    run_script = os.path.join(arkane_dir, 'run_arkane.sh')
    with open(run_script, 'w') as f:
        # Run on express
        f.write('#!/bin/bash\n')
        f.write('#SBATCH --partition=express,short,west\n')
        f.write('#SBATCH --time=00:20:00\n\n')
        f.write('python ~/rmg/RMG-Py/Arkane.py input.py\n\n')

    reaction_log(reaction_index, f'finished setting up arkane for reaction {reaction_index} {reaction_label}')
    set_reaction_status(reaction_index, 'arkane_setup', True)


def run_arkane_reaction(reaction_index, direction='forward'):
    # Run the arkane job

    # check if the arkane job was already completed
    if get_reaction_status(reaction_index, 'arkane_calc'):
        reaction_log(reaction_index, 'Arkane job already ran')
        return True
    elif arkane_reaction_complete(reaction_index):
        set_reaction_status(reaction_index, 'arkane_setup', True)
        set_reaction_status(reaction_index, 'arkane_calc', True)
        reaction_log(reaction_index, 'Arkane job already ran')
        return True
    elif not get_reaction_status(reaction_index, 'arkane_setup'):
        reaction_log(reaction_index, 'Arkane job not set up.')
        return False

    reaction_dir = os.path.join(DFT_DIR, 'kinetics', f'reaction_{reaction_index:04}')
    arkane_dir = os.path.join(reaction_dir, 'arkane')

    # wait for fewer than MAX_JOBS_RUNNING jobs running
    jobs_running = job_manager.count_slurm_jobs()
    while jobs_running > MAX_JOBS_RUNNING:
        time.sleep(60)
        jobs_running = job_manager.count_slurm_jobs()

    # Run the arkane job
    arkane_run_file = os.path.join(arkane_dir, 'run_arkane.sh')
    start_dir = os.getcwd()
    os.chdir(arkane_dir)
    arkane_job = job_manager.SlurmJob()
    slurm_cmd = f"sbatch {arkane_run_file}"
    arkane_job.submit(slurm_cmd)
    os.chdir(start_dir)


if __name__ == '__main__':
    # for idx in [419, 1814, 1287, 748, 370, 1103, 371]:
    for idx in [1288]:
        setup_opt(idx, 'center')
        run_opt(idx, 'center')

    exit(0)
    top_reactions = [
        915, 749, 324, 419, 1814, 1287, 748, 1288, 370, 1103,
        371, 213, 420, 581, 464, 1289, 720, 722, 1658, 574, 725, 1736,
        418, 1290, 1721, 1665, 1685, 427, 1714, 1766, 655, 1773, 1003, 650,
        985, 918, 585, 692, 1532, 1326, 1578, 1428, 916, 595, 693, 1242
    ]

    if len(sys.argv) > 1:
        reaction_index = int(sys.argv[1])
        screen_reaction_ts(reaction_index)
    else:
        for rxn in top_reactions:
            # 324 has errors, 915 and 749 are just currently running
            if rxn in [915, 749, 324]:
                continue
            print('Screen reaction', rxn)
            screen_reaction_ts(rxn)
            run_shell_opt(rxn)
    exit(0)
    # setup_arkane_species(87)
    # exit(0)

    # run one

    # if len(sys.argv) > 1:
    #     species_index = int(sys.argv[1])
    # else:
    #     species_index = 87
    # screen_conformers(species_index)
    # optimize_conformers(species_index)
    # exit(0)
    # run all
    # wait until # jobs is below 40 to start a new thing:
    import job_manager

    # for species_index in range(40, 65):
    # for species_index in range(15, 110):
    for species_index in range(0, 15):
        jobs_running = job_manager.count_slurm_jobs()
        while jobs_running > 40:
            time.sleep(60)
            jobs_running = job_manager.count_slurm_jobs()
        screen_species_conformers(species_index)
        optimize_conformers(species_index)
