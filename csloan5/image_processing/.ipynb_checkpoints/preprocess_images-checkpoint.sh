#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=01:00:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards_project/code/output/imgOutput.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards_project/code/error/imgError.txt

python /project/arcc-students/csloan5/OilWellCards_project/code/preprocess_images.py
