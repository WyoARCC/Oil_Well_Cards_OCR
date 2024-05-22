#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards_project/batch_output/card_separation/cluster_separation/norm_sep_out_%A.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards_project/batch_output/card_separation/cluster_separation/norm_sep_err_%A.txt
#SBATCH --mem=10G
#SBATCH --gres=gpu:1
#SBATCH --partition=teton-gpu
#SBATCH --mail-type=ALL
#SBATCH --mail-user=csloan5@uwyo.edu

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/GPU_env

python -u /project/arcc-students/csloan5/OilWellCards_project/card_separation/separate_cards.py -i "/project/arcc-students/csloan5/OilWellCards_project/sorted_cards/mixed_cards/" -o "/project/arcc-students/csloan5/OilWellCards_project/sorted_cards/mixed_cards/" --bs 1000

conda deactivate
