#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards_project/batch_output/card_separation/out.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards_project/batch_output/card_separation/err.txt
#SBATCH --mem=10G
#SBATCH --gres=gpu:1
#SBATCH --partition=teton-gpu

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/GPU_env

python /project/arcc-students/csloan5/OilWellCards_project/card_separation/separate_vertical_cards.py -i "/project/arcc-students/enhanced_oil_recovery_cards/" -o "/project/arcc-students/csloan5/OilWellCards_project/sorted_cards/"

conda deactivate
