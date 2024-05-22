#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/code/batch_output/out_%A.txt
#SBATCH --error=/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/code/batch_output/err_%A.txt
#SBATCH --mem=16G

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/GPU_env

python -u /pfs/tc1/project/arcc-students/OilWellProject2023.Summer/code/GeneralParser.py -i "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/ConvertedCSVFiles/" -o "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/code/General_cards_parsed_Final.csv"

conda deactivate
