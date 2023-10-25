#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=10:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards_project/code/output/out.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards_project/code/error/err.txt

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/GPU_env

python /project/arcc-students/csloan5/OilWellCards_project/code/image_processing/convert_pdfs_to_jpgs.py

conda deactivate
