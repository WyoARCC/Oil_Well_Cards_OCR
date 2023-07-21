#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=01:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards/batch_output/parsing/type3_parse_out_%A.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards/batch_output/parsing/type3_parse_err_%A.txt
#SBATCH --mem=16G

module load miniconda3/23.1.0
conda activate /project/arcc-students/csloan5/environments/GPU_env

python -u /project/arcc-students/csloan5/OilWellCards/text_parsing/type3_card_parser.py -i "/project/arcc-students/csloan5/OilWellCards/test_set/vert_card_text/" -o "/project/arcc-students/csloan5/OilWellCards/test_output/first_try.csv"

conda deactivate
