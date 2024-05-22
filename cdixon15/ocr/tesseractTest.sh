#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=00:10:00
#SBATCH --output=/project/arcc-students/cdixon15/oilCardProject/tesseractTests/sbatchOutput/output.txt
#SBATCH --error=/project/arcc-students/cdixon15/oilCardProject/tesseractTests/sbatchOutput/error.txt

python /project/arcc-students/cdixon15/oilCardProject/tesseractTests/tesseractTest.py -i '/project/arcc-students/cdixon15/oilCardProject/testInputs/310-0002.pdf' -o '/project/arcc-students/cdixon15/oilCardProject/tesseractTests/processed'