#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=05:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/duplicate_copier/dupe_sep_out_%A.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/duplicate_copier/dupe_sep_err_%A.txt

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/normal/

python -u /pfs/tc1/project/arcc-students/csloan5/OilWellCards/file_management/copy_duplicate_files.py --copy "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/ConvertedCSVFiles/" --source "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/typeOne/" -o "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/Type_1_CSVs/"

conda deactivate
