#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=30:00:00
#SBATCH --output=/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sbatchOutput/lineDetection/output.txt
#SBATCH --error=/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sbatchOutput/lineDetection/error.txt

#python /project/arcc-students/cdixon15/oilCardProject/layoutSeparation/lineDetection.py -i "/project/arcc-students/enhanced_oil_recovery_cards/BOX 1 (310-330)/310 T47N R62W-T47N R68W/310-0000.pdf" -o /project/arcc-students/cdixon15/oilCardProject/layoutSeparation/outputs/310-0000_lines.jpg
#python /project/arcc-students/cdixon15/oilCardProject/oil-Card-Rebase/layoutDetection/lineDetection.py -i "/project/arcc-students/cdixon15/oilCardProject/layoutSeparation/testInputs" -o "/project/arcc-students/cdixon15/oilCardProject/oil-Card-Rebase/processed/lineDetection"
python /project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/layoutDetection/lineDetection.py -i "/project/arcc-students/cdixon15/oilCardProject/testInputs/exampleCards/143-0017.pdf" -o "/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/processed/lineDetection/17.jpg"