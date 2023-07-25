#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sbatchOutput/ocr/output.txt
#SBATCH --error=/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/sbatchOutput/ocr/error.txt

python /project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/ocr/cleanAndConvert.py -i "/project/arcc-students/cdixon15/oilCardProject/testInputs/exampleCards" -o "/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/processed/ocr/exampleCards"
