import time

print("Starting imports and loading model...")
start = time.time()

import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# === Config ===
EVAL_FILE = "evaluation.jsonl"
OUTPUT_DIR = Path("fine_tuned_results")
MODEL_PATH = "./gams9b-finetuned_9"

OUTPUT_DIR.mkdir(exist_ok=True)

# === Load Model ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(
    base_model,
    MODEL_PATH,
    device_map="auto"
)

print(f"Model loaded to device: {model.device}")
print(f"Setup took {time.time() - start:.2f}s")

# === Process Entries ===
with open(EVAL_FILE, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        example = json.loads(line)
        filename = example["file"]
        input_text = example["input"]

        inputs = tokenizer(input_text + tokenizer.eos_token, return_tensors="pt").to(model.device)

        # Generate output
        output = model.generate(
            **inputs,
            max_new_tokens = 200,
            min_new_tokens = 50,
            do_sample=True,
            temperature=0.75,
            top_p=0.9,
            top_k=42,
            repetition_penalty=1.12,
        )

        # Trim
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        line_count = len(input_text.splitlines())
        result_lines = generated_text.splitlines()[line_count:]
        result_text = "\n".join(result_lines).strip()

        # === Build header ===
        date_part, time_part = filename.replace(".txt", "").rsplit("-", 1)
        date_formatted = date_part.replace("-", ". ")
        time_formatted = time_part[:2] + "." + time_part[2:]
        header_line = f"Prometne informacije        {date_formatted}         {time_formatted}           1. in 2. program"

        full_output = f"{header_line}\n\n{result_text}"

        # Write to file
        output_path = OUTPUT_DIR / filename
        with open(output_path, "w", encoding="utf-16") as out_f:
            out_f.write(full_output)

        print(f"[{i}] Wrote: {output_path}")
