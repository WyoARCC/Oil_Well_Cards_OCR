#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=24:00:00
#SBATCH --output=/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sbatchOutput/sortTypeOne/output.txt
#SBATCH --error=/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sbatchOutput/sortTypeOne/error.txt

python /project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sortTypeOne.py -i "/project/arcc-students/enhanced_oil_recovery_cards" -o "/project/arcc-students/cdixon15/oilCardProject/typeOneSorted"
