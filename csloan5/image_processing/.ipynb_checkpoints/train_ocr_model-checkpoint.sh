#!/bin/bash

#SBATCH --account=arcc-students
#SBATCH --time=00:10:00
#SBATCH --output=/project/arcc-students/csloan5/OilWellCards_project/code/output/tf_output.txt
#SBATCH --error=/project/arcc-students/csloan5/OilWellCards_project/code/error/tf_error.txt
#SBATCH --job-name=tensorflow_test
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --gres=gpu:1

echo "Load Modules:"
module load arcc/1.0
module load cudnn/8.8.0.121 
module load cuda/11.8.0
module load miniconda3/4.3.30

echo "Check GPU Allocation:"
echo "Running nvidia-smi:"
srun nvidia-smi -L
nvcc --version

echo "Activate Conda Environment"
conda activate /pfs/tc1/project/arcc-students/csloan5/OilWellCards_project/tf_env/

python --version

echo "- - - - - - - - - - - - - - - - - - - - -"
srun python /project/arcc-students/csloan5/OilWellCards_project/code/tensorflow_test.py
echo "- - - - - - - - - - - - - - - - - - - - -"

echo "Deactivate Conda:"
conda deactivate

echo "Done"
