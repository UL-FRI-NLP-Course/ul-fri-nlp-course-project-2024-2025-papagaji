from transformers import AutoTokenizer, Trainer, TrainingArguments, AutoModelForSeq2SeqLM, AutoModelForCausalLM, BitsAndBytesConfig, DataCollatorWithPadding
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
import os


os.environ["TOKENIZERS_PARALLELISM"] = "false"


model_name = "cjvt/GaMS-9B-Instruct"

dataset = load_dataset("json", data_files={"train": "train_4.jsonl", "validation": "val_4.jsonl"})

tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    prompts = batch["input"]
    responses = batch["output"]

    full_texts = [
        f"{prompt}{tokenizer.eos_token}{response}{tokenizer.eos_token}"
        for prompt, response in zip(prompts, responses)
    ]

    model_inputs = tokenizer(
        full_texts,
        truncation=True,
        max_length=512,
        padding='max_length',
    )

    model_inputs["labels"] = model_inputs["input_ids"].copy()
    return model_inputs


tokenized = dataset.map(tokenize, batched=True)


bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_has_fp16_weight=False
)


model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation="eager",
)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none"
)

model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir="./gams9b-finetuned_9",
    per_device_train_batch_size=2,
    num_train_epochs=5,
    fp16=True,
    save_strategy="epoch",
    logging_dir="./logs",
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer, pad_to_multiple_of=8)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    data_collator=data_collator,
)


print("starting training")

trainer.train()

trainer.save_model("gams9b-finetuned_9")

