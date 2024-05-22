#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/vertical_card_separation/vert_sep_out_%A.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/vertical_card_separation/vert_sep_err_%A.txt
#SBATCH --mem=15G

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/GPU_env

python -u /project/arcc-students/csloan5/OilWellCards/card_separation/separate_vertical_cards.py -i "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/non_blank_pages/Box10/" -o "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/vert_pages/Box10/" --bs 500

conda deactivate
