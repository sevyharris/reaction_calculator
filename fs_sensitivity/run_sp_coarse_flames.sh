#!/bin/bash
#SBATCH --job-name=flame_sensitivity
#SBATCH --mem=20Gb
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=16
#SBATCH --array=0-4


start_index=$(($SLURM_ARRAY_TASK_ID * 50))

python /work/westgroup/harris.se/autoscience/reaction_calculator/fs_sensitivity/fs_sp_sensitivity_coarse.py $1 $start_index
