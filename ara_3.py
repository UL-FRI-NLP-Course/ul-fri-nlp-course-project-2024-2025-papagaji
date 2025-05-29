from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoConfig
import torch
from vrabec import getFromInterval, prompts_and_responses
import evaluate
import gc
import os
from datetime import datetime
from accelerate import init_empty_weights, cpu_offload, load_checkpoint_and_dispatch

print(torch.cuda.is_available())
torch.cuda.empty_cache()

def getPromptSLO(data):
    return f"""
# NAVODILA
Sestavi prometno poročilo o stanju na slovenskih cestah, ki naj vsebuje vse pomembne informacije podane v vhodnih podatkih.
Poročilo mora:
- vsebovati 3 do 5 povedi
- ne sme biti krajše od 20 besed
- biti napisano samo v naravni slovenščini
- povzeti podatke iz vhoda

Obnovljeni podatki naj imajo naslednjo obliko:
Cesta in smer + razlog + posledica in odsek
ali
Razlog + cesta in smer + posledica in odsek

# Primer vhoda (podatkov) in njegovega izhoda (poročila)
# Vhod:
Nesreče: Cesta Novo mesto - Šentjernej je zaprta pri odcepu za Dolenje Mokro Polje.
Opozorila: Cesta Rateče - Planica bo zaprta danes do 18. ure
Ovire: Zaradi vozila v okvari je zaprt en pas na cesti Črnuče - Ljubljana, proti krožišču Tomačevo.
Zastoji: Na hrvaški strani mejnih prehodov Dragonja in Sečovlje proti Sloveniji.
Splošno: Do 22. ure velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7,5 t.

# Izhod:
Cesta Novo mesto - Šentjernej je zaradi prometne nesreče zaprta pri odcepu za Dolenje Mokro Polje.
Cesta Rateče - Planica bo zaprta še do 18-ih.
Na cesti Črnuče - Ljubljana je proti krožišču Tomačevo zaradi pokvarjenega vozila zaprt en pas. 
Pred mejnima prehodoma Dragonja in Sečovlje je zastoj proti Sloveniji.
Do 22-ih velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7 ton in pol.


# NALOGA
Zdaj v izhodu sestavi prometno poročilo (3 do 5 povedi). Vsebovati mora naslednje vhodne podatke:
# Vhod:
{data}
# Izhod:
"""

def getLLM(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    # tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token = tokenizer.unk_token
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        device_map="auto", 
        trust_remote_code=True
    )
    return model, tokenizer


def executeLLM(model, tokenizer, prompt, max_new_tokens, temperature, top_p, top_k, repetition_penalty):
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).to("cpu")
    # try:
    #     print(f"Shape: {inputs['input_ids'].shape[0]}")
    #     print(f"Token count: {inputs['input_ids'].shape[1]}")
    # except:
    #     print("Inputs error!")
    inputs = inputs.to(model.device) 
    # inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).to(model.device)
    model.eval()
    # if tokenizer.eos_token_id is None:
    #     tokenizer.eos_token_id = tokenizer.convert_tokens_to_ids("<eos>")
    print(tokenizer.pad_token_id, tokenizer.eos_token_id)
    print(tokenizer.eos_token)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            min_new_tokens=20,
            repetition_penalty=repetition_penalty,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    result = tokenizer.decode(output[0].cpu(), skip_special_tokens=True)
    return result


once = True
# model_path = "./mistral_7b_local"
model_path = "./gams_9b_local"
excel, txts, files = prompts_and_responses(chosen_txts_dir='data/txt3/')
gc.collect()
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()
# print(torch.cuda.memory_summary())

model, tokenizer = getLLM(model_path)
rouge = evaluate.load("rouge")
predictions = []

max_new_tokens = 150
temperature = 0.
top_p = 0.9
top_k = 50
repetition_penalty = 1.12
# print("beams", 15)
# print("beam 10, false")
print("max_new_tokens, temperature, top_p, top_k, repetition_penalty")


print(max_new_tokens, temperature, top_p, top_k, repetition_penalty)
print(getPromptSLO(""))

path = os.path.dirname(__file__) 
for data, txt, file in zip(excel, txts, files):
    try:
        with open("out/inputs/data_" + file.name, "w", encoding="utf-16") as out:
            out.write(data)
    except Exception as e:
        print(e)
        print("Could not write file!")
    prompt = getPromptSLO(data)
    result = executeLLM(model, tokenizer, prompt, max_new_tokens, temperature, top_p, top_k, repetition_penalty)
    once = False
    result = result.split("\n# Izhod:")[-1].strip()
    print("__________________________________________________")
    print("----------------------OUT-------------------------")
    print(result)
    print("----------------------REF------------------------")
    print(txt)
    print("----------------------DATA------------------------")
    print(data)
    result = txt.split("\n")[0] + "\nPodatki o prometu.\n" + result
    predictions.append(result)
    results = rouge.compute(predictions=[result], references=[txt])
    print("---------------------ROUGE------------------------")
    print(results)
    try:
        with open("out/results/out_" + file.name, "w", encoding="utf-16") as out:
            out.write(result)
        with open("out/compare/com_" + file.name, "w", encoding="utf-16") as out:
            out.write("-----------------------OUTPUT-----------------------\n" + result + "\n----------------------REFERENCE----------------------\n" + txt)
    except Exception as e:
        print(e)
        print("Could not write file!")
    # torch.cuda.empty_cache()

results = rouge.compute(predictions=predictions, references=txts)
print("Final")
print(results)

del model
del tokenizer
