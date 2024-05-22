#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/pdf_page_split/split_out_%A.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards/batch_output/card_separation/pdf_page_split/split_err_%A.txt
#SBATCH --mem=15G

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/normal/

python /project/arcc-students/csloan5/OilWellCards/card_separation/split_pdfs.py -i "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/Master/non_blank/normBox10/" --not "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/Master/non_blank/Box10/" --blank "/pfs/tc1/project/arcc-students/OilWellProject2023.Summer/Master/blank/Box10/"

conda deactivate
