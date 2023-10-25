#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=05:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/duplicate_mover/dupe_sep_out_%A.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/duplicate_mover/dupe_sep_err_%A.txt

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/normal/

python -u /pfs/tc1/project/arcc-students/csloan5/OilWellCards/card_separation/move_duplicate_cards.py --source "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/non_blank_pages/" --dupe "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/temp/" -o "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/temp2/"

conda deactivate
