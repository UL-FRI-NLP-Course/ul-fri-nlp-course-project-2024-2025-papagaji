# 🛣️ NLP Project: Automatic Generation of Slovenian Traffic News for RTV Slovenija

This repository contains the full implementation of an NLP project developed for the Natural Language Processing course. The objective was to automatically generate short Slovenian traffic reports for RTV Slovenija using prompt engineering and fine-tuning of a large language model.

## 📁 Project Structure

- `report/report.pdf` – Final project report  
- `data/` – Raw and processed data used for training, evaluation, and testing  
- `evalvacija/` – Contains generated predictions and references for evaluation  (old)
- `extract_data.py` – Converts `.rtf` reference files to `.txt` 
- `rouge.py` – Computes ROUGE scores to evaluate generated outputs  
- `ara_2.py` – Prompt-based report generation script  (old)
- `prompts_and_responses.py` – Generates reports using prompt engineering with relevant input data  (old)

### 📝 Prompt engineering Scripts
- `model_download.py` - Locally downloads the GaMS 9B model (needs 35 GB disk space)
- `prompt_input_preparation.py` – Fetches inputs required for prompt engineering
- `prompt_engineering.py` – Runs LLM using a prompt, writing output to `prompt_engineering_results/`

### 📦 Fine-tuning Scripts

- `prepare_txt_files_ft.py` – Converts all reference reports (year 2024) into `.txt` format  
- `fine_tunning_data_collection.py` – Collects training/validation data for fine-tuning  
  - Outputs: `train_4.jsonl`, `val_4.jsonl`  
- `fine_tuning.py` – Fine-tunes the LLM on the above dataset  
- `llm_finetune_9/` – Folder of the fine-tuned model  
- `evaluation_data_collection.py` – Collects evaluation data from the reference reports from folder `2023/`
- `generate_finetuned_results.py` – Generates reports using the fine-tuned model on many examples  
- `generate_finetuned.py` – Generates a report on a single example with the fine-tuned model  

## ⚙️ Setup Instructions

### 1. ✅ Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

### 🔽 2. Download the Data

Download the dataset from [this link](https://unilj-my.sharepoint.com/personal/slavkozitnik_fri1_uni-lj_si/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fslavkozitnik%5Ffri1%5Funi%2Dlj%5Fsi%2FDocuments%2FPredmeti%2FONJ%2FONJ%5F2025%5FSpring%2FProjects%2FRTVSlo%2Ezip&parent=%2Fpersonal%2Fslavkozitnik%5Ffri1%5Funi%2Dlj%5Fsi%2FDocuments%2FPredmeti%2FONJ%2FONJ%5F2025%5FSpring%2FProjects&ga=1) and extract its contents into the `data/` folder.

### 📑 3. Convert .RTF Files to .TXT
Run the following to convert reference `.rtf` reports into `.txt` format:

```bash
python extract_data.py
```
 The converted files are then put into a new folder data/txts.

### 📊 4. Generate Reports
#### 4.1 Generating Reports with Prompt Engineering 
1. Download the model:
```bash
python model_download.py
```

2. Run the prompt engineering script on 2023 dataset (must have excel data in `data/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx`):
```bash
python prompt_engineering.py
```

Outputs are saved in `prompt_engineering_results/`.


#### 4.2 Generating Reports with Fine-tuning
To generate a report using the fine-tuned model for a single input:

Single example generation:
1. Edit the `data` variable in generate_finetuned.py with your input.
2. Run the script:
```bash
python generate_finetuned.py
```
Multiple examples generation:
1. Prepare the evaluation data:
```bash
python evaluation_data_collection.py
```
It will prepare the data based on the references inside the `2023/` folder.

2. Generate reports:
```bash
python generate_finetuned_results.py
```
Outputs are saved in `finetuned_results/`.

### 🔧 5 Fine-tuning the Model
1. Prepare .txt reference files:
```bash
python prepare_txt_files_ft.py
```
2. Collect data for training:
```bash
python fine_tunning_data_collection.py
```
This creates train_4.jsonl and val_4.jsonl

3. Fine-tune the model:
```bash
python fine_tuning.py
```

The trained model will be saved in llm_finetune_9/.


### 📊 Evaluation
Run rouge.py to compute ROUGE scores between generated outputs and reference reports.


### 🖥️ Running on SLURM
To run scripts on a SLURM-based cluster just change the file you want to run inside the file `run.sh` and set bigger a higher time limit if needed.
After that you just submit the job with the following command:
```bash
sbatch run.sh
```

You can check the status of your job with:
```bash
squeue --me
```

