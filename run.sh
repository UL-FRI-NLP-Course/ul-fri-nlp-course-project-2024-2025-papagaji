#!/bin/sh

#SBATCH --job-name=NLP_project_papagaji
#SBATCH --partition=gpu
#SBATCH --output=out.txt   
#SBATCH --reservation=fri  
#SBATCH --cpus-per-task=16
#SBATCH --gpus=1
#SBATCH --time=01:00:00


source ~/ONJ/ul-fri-nlp-course-project-2024-2025-papagaji/nlp_env/bin/activate

srun python3 ara.py
