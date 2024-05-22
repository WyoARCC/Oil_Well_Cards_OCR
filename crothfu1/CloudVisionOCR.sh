#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/crothfu1/OilWellProject/Code/sbatch_output/OCR_out_%A.txt
#SBATCH --error=/project/arcc-students/crothfu1/OilWellProject/Code/sbatch_output/OCR_err_%A.txt

module load miniconda3/23.1.0
conda activate /pfs/tc1/project/arcc-students/crothfu1/environments/ocr_env

python /project/arcc-students/crothfu1/OilWellProject/Code/CloudVisionOCR.py

conda deactivate
