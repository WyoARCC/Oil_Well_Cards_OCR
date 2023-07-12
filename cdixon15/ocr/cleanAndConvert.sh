#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=7-00:00:00
#SBATCH --output=/project/arcc-students/cdixon15/oilCardProject/typedOCR/output.txt
#SBATCH --error=/project/arcc-students/cdixon15/oilCardProject/typedOCR/error.txt

python /project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/ocr/cleanAndConvert.py -i "/project/arcc-students/enhanced_oil_recovery_cards/BOX 1 (310-330)/310 T47N R62W-T47N R68W" -c /project/arcc-students/cdixon15/oilCardProject/typedOCR/cleaned -o /project/arcc-students/cdixon15/oilCardProject/typedOCR/text
