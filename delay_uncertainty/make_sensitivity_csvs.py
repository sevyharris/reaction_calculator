import os
import sys
import cantera as ct
import numpy as np
import pandas as pd
import concurrent.futures
import rmgpy.chemkin
import subprocess


try:
    experimental_table_index = int(sys.argv[1])
except IndexError:
    experimental_table_index = 7

experimental_condition_index = 7


# perturb every species and reaction in the mechanism
# we'll select the perturbations one at a time later in the script
def perturb_species(species, delta):
    # takes in an RMG species object
    # change the enthalpy offset
    for poly in species.thermo.polynomials:
        new_coeffs = poly.coeffs
        new_coeffs[5] *= (1.0 + delta)
        poly.coeffs = new_coeffs


def perturb_reaction(rxn, delta):
    # takes in an RMG reaction object
    # delta is the ln(k) amount to perturb the A factor
    # delta is a multiplicative factor- units don't matter, yay!
    # does not deepycopy because there's some issues with rmgpy.reactions copying
    rxn.kinetics.A.value *= np.exp(delta)


chemkin = '/home/moon/autoscience/reaction_calculator/delay_uncertainty/base_model/chem_annotated.inp'
chemkin = '/work/westgroup/harris.se/autoscience/reaction_calculator/delay_uncertainty/base_model/chem_annotated.inp'
chemkin = '/work/westgroup/harris.se/autoscience/fuels/butane/small_lib_20230801/chem_annotated.inp'

working_dir = os.path.dirname(chemkin)
transport = os.path.join(working_dir, 'tran.dat')
species_dict = os.path.join(working_dir, 'species_dictionary.txt')
species_list, reaction_list = rmgpy.chemkin.load_chemkin_file(chemkin, dictionary_path=species_dict, transport_path=transport)
print(f'Loaded {len(species_list)} species, {len(reaction_list)} reactions')
base_cti_path = os.path.join(working_dir, 'base.cti')
perturbed_chemkin = os.path.join(working_dir, 'perturbed.inp')
perturbed_cti_path = os.path.join(working_dir, 'perturbed.cti')

skip_create_perturb = False
if os.path.exists(perturbed_cti_path):
    skip_create_perturb = True
    print('Perturbed cti already exists, skipping creation of perturbed mechanism')

if not skip_create_perturb:
    # load the chemkin file and create a normal and perturbed cti for simulations:
    # # write base cantera
    subprocess.run(['ck2cti', f'--input={chemkin}', f'--transport={transport}', f'--output={base_cti_path}'])

    delta = 0.1
    for i in range(0, len(species_list)):
        perturb_species(species_list[i], delta)

    for i in range(0, len(reaction_list)):
        try:
            perturb_reaction(reaction_list[i], delta)
        except AttributeError:
            continue

    # save the results
    rmgpy.chemkin.save_chemkin_file(perturbed_chemkin, species_list, reaction_list, verbose=True, check_for_duplicates=True)
    subprocess.run(['ck2cti', f'--input={perturbed_chemkin}', f'--transport={transport}', f'--output={perturbed_cti_path}'])

# for now the goal is just to make the base and perturbed models
exit(0)

# load the 2 ctis
base_gas = ct.Solution(base_cti_path)
perturbed_gas = ct.Solution(perturbed_cti_path)


# Take Reactor Conditions from Table 7 of supplementary info in
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
def run_simulation(T, P, X):
    # function to run a RCM simulation

    # gas is a global object
    t_end = 1.0  # time in seconds
    base_gas.TPX = T, P, X

    reactor = ct.IdealGasReactor(base_gas)
    reactor_net = ct.ReactorNet([reactor])

    times = [0]
    T = [reactor.T]
    P = [reactor.thermo.P]
    X = [reactor.thermo.X]  # mol fractions
    while reactor_net.time < t_end:
        reactor_net.step()

        times.append(reactor_net.time)
        T.append(reactor.T)
        P.append(reactor.thermo.P)
        X.append(reactor.thermo.X)

    slopes = np.gradient(P, times)
    delay_i = np.argmax(slopes)
    return times[delay_i]


# Load the experimental conditions
ignition_delay_data = '/work/westgroup/harris.se/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
# ignition_delay_data = '/home/moon/autoscience/autoscience/butane/experimental_data/butane_ignition_delay.csv'
df_exp = pd.read_csv(ignition_delay_data)

# slice just table 7, where phi=1.0
table_exp = df_exp[df_exp['Table'] == experimental_table_index]
# Define Initial conditions using experimental data
tau_exp = table_exp['time (ms)'].values.astype(float)  # ignition delay
T7 = table_exp['T_C'].values  # Temperatures
P7 = table_exp['nominal pressure(atm)'].values * ct.one_atm  # pressures in atm
# list of starting conditions
# Mixture compositions taken from table 2 of
# https://doi-org.ezproxy.neu.edu/10.1016/j.combustflame.2010.01.016
concentrations = []
# for phi = 1
x_diluent = 0.7649
conc_dict = {
    'O2(2)': 0.2038,
    'butane(1)': 0.03135
}

for i in range(0, len(table_exp)):
    x_N2 = table_exp['%N2'].values[i] / 100.0 * x_diluent
    x_Ar = table_exp['%Ar'].values[i] / 100.0 * x_diluent
    x_CO2 = table_exp['%CO2'].values[i] / 100.0 * x_diluent
    conc_dict['N2'] = x_N2
    conc_dict['Ar'] = x_Ar
    conc_dict['CO2(7)'] = x_CO2
    concentrations.append(conc_dict)


def same_reaction(rxn1, rxn2):
    """Returns true IFF reactions have same reactants, products, and type"""
    if rxn1.reactants == rxn2.reactants and rxn1.products == rxn2.products and type(rxn1) == type(rxn2):
        return True
    else:
        return False


# compute and save the delays
species_delays = np.zeros((len(perturbed_gas.species()), len(concentrations)))
reaction_delays = np.zeros((len(perturbed_gas.reactions()), len(concentrations)))

for i in range(0, len(perturbed_gas.species())):
    print(f'perturbing {i} {perturbed_gas.species()[i]}')
    # load the base gas
    base_gas = ct.Solution(base_cti_path)

    # run the simulations at condition #j
    base_gas.modify_species(i, perturbed_gas.species()[i])

    # Run all simulations in parallel
    delays = np.zeros(len(concentrations))
    condition_indices = np.arange(0, len(concentrations))

    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [T7[j] for j in condition_indices],
            [P7[j] for j in condition_indices],
            [concentrations[j] for j in condition_indices]
        )):
            delays[condition_index] = delay_time
    species_delays[i, :] = delays

# save the result
np.save(os.path.join(working_dir, f'species_delays_{experimental_table_index:04}.npy'), species_delays)

for i in range(0, len(perturbed_gas.reactions())):
    print(f'perturbing {i} {perturbed_gas.reactions()[i]}')
    # TODO skip the ones that haven't actually been perturbed because PDEP or whatever
    try:
        a = base_gas.reactions()[i].rate
    except AttributeError:
        print(f'skipping reaction {i}: {base_gas.reactions()[i]} because it is not perturbed from the base mechanism')
        continue

    # load the base gas
    base_gas = ct.Solution(base_cti_path)
    # order is not preserved between the mechanisms, so we have to find the reaction that matches
    if same_reaction(perturbed_gas.reactions()[i], base_gas.reactions()[i]):
        perturbed_index = i
    else:
        for k in range(0, len(base_gas.reactions())):
            if same_reaction(perturbed_gas.reactions()[k], base_gas.reactions()[i]):
                perturbed_index = k
                break
        else:
            raise ValueError('Could not find matching reaction in base mechanism')

    base_gas.modify_reaction(i, perturbed_gas.reactions()[perturbed_index])

    # Run all simulations in parallel
    delays = np.zeros(len(concentrations))
    condition_indices = np.arange(0, len(concentrations))

    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        for condition_index, delay_time in zip(condition_indices, executor.map(
            run_simulation,
            [T7[j] for j in condition_indices],
            [P7[j] for j in condition_indices],
            [concentrations[j] for j in condition_indices]
        )):
            delays[condition_index] = delay_time
    reaction_delays[i, :] = delays
    if i % 100 == 0:
        np.save(os.path.join(working_dir, f'reaction_delays_{experimental_table_index:04}.npy'), reaction_delays)

# save the result
np.save(os.path.join(working_dir, f'reaction_delays_{experimental_table_index:04}.npy'), reaction_delays)
