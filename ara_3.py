from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoConfig
import torch
from vrabec2 import getFromInterval, prompts_and_responses
import evaluate
import gc
from datetime import datetime
# from accelerate import init_empty_weights, cpu_offload, load_checkpoint_and_dispatch

print(torch.cuda.is_available())
torch.cuda.empty_cache()

def getPromptSLO(data):
    return f"""
# Navodila
# Ustvari poročilo o stanju na slovenskih cestah, ki naj vsebuje vse pomembne informacije, ki so podane v vhodnih podatkih. 

# Oblika posamezne informacije:
Cesta in smer + razlog + posledica in odsek
Razlog + cesta in smer + posledica in odsek

# Podani so primeri poročil v parih Podatki Poročilo:
# Primer 1:
# Podatki:
Opozorila: Cesta Rateče - Planica bo zaprta danes do 18. ure
Zastoji: Na hrvaški strani mejnih prehodov Dragonja in Sečovlje proti Sloveniji. Na cesti Rateče - Kranjska Gora - Jesenice, zastoji na posameznih odsekih.
Ovire: Zaprt počasni pas na primorski avtocesti zaradi okvare vozila pri priključku Kastelec proti Ljubljani.
# Poročilo:
Gost promet z občasnimi zastoji je na cesti od Rateč proti Kranjski Gori in Jesenicam.
Cesta Rateče - Planica bo zaprta še do 18-ih.
Pred mejnima prehodoma Dragonja in Sečovlje je zastoj proti Sloveniji.
Na primorski avtocesti je zaradi okvare vozila zaprt počasni pas pri priključku Kastelec proti Ljubljani.

# Primer 2:
# Podatki:
Zastoji: Na ljubljanski južni obvoznici med Rudnikom in Centrom proti Kozarjam. Na cesti Bohinj - Bled, pred Bledom.
Dela: Delovne zapore na cesti  Ljubljana  - Zagorje:   - pri Beričevem bo zaprta do 24. ure;
Splošno: Do 22. ure velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7,5 t.
# Poročilo:
Zaradi del so krajši zastoji na južni ljubljanski obvoznici med priključkoma Rudnik in Center proti Kozarjam.
Krajši zastoji so tudi na cesti Bohinj - Bled pred Bledom.
Zaradi delovne zapore bo cesta Ljubljana - Zagorje do polnoči zaprta pri Beričevem.
Do 22-ih velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7 ton in pol.

# Primer 3:
# Podatki:
Opozorila: Danes velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7,5 t do 13. ure ter na nekaterih primorskih cestah do 16. ure.
Zastoji: Na cesti Vič - Brezovica, Izola Strunjan in Šmarje - Koper. Na primorski hitri cesti med priključkoma Bertoki in Koper proti Izoli. - Med Postojno in Brezovico na posameznih odsekih proti Ljubljani. - Med Razdrtim in Brezovico na posameznih odsekih proti Ljubljani. Na cesti Izola Strunjan in Šmarje - Koper. Na podravski avtocesti med priključkom Zakl in Gruškovjem proti Hrvaški. Pred predorom Karavanke proti Sloveniji in proti Avstriji 3 km, občasno zapirajo predor. Proti Vrhniki: - Na ljubljanski zahodni obvoznici od Kosez in mimo Kozarij. - Na ljubljanski južni obvoznici od Viča mimo Kozarij.
# Poročilo:
Še vedno je zastoj na ljubljanski zahodni obvoznici proti Vrhniki, ki sega vse do gorenjske avtoceste. Občasno zapirajo predor Šentvid. Prav tako je zastoj na ljubljanski južni obvoznici od Barja mimo Kozarij.
Zastoji so tudi na primorski avtocesti med priključkom Senožeče in Brezovico na posameznih odsekih proti Ljubljani, na podravski avtocesti med priključkom Zakl in Gruškovjem proti Hrvaški in na cestah Vič - Brezovica, Lucija - Strunjan in Šmarje - Koper.
Kolona vozil je pred predorom Karavanke, tako na avstrijski kot na slovenski strani, zato predor občasno zapirajo.
Vozila zastajajo tudi na primorski hitri cesti med priključkoma Bertoki in Koper proti Izoli.

# NALOGA: Sestavi poročilo, ki opisuje stanje na cestah. Poročilo naj bo dolgo vsaj dve povedi. Poročilo ne presega petih povedi. 
# Poročilo se mora navezovati na naslednje podatke:
{data}
Poročilo:
"""

# # Primeri poročil v parih Podatki Poročilo:
# # Primer 1:
# # Podatki:
# Ovire: Zaradi vozila v okvari je zaprt en pas na cesti Črnuče - Ljubljana, proti krožišču Tomačevo.
# Mednarodno: Čakalne dobe pri vstopu: Metlika, Slovenska vas, Obrežje in Gruškovje.
# Zastoji: Na severni ljubljanski obvoznici, in to proti Gorenjski.
# # Poročilo
# Na štajerski avtocesti je zaradi pokvarjenega vozila oviran promet proti Mariboru med Lukovico in Blagovico. Nastal je krajši zastoj. Opozarjamo na nevarnost naleta.
# Na regionalni cesti Škofja Loka-Gorenja vas so odstranili posledice nesreče pri Poljanah nad Škofjo Loko.


# # Primer 4:
# # Podatki:
# Opozorila: Danes velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7,5 t do 13. ure ter na nekaterih primorskih cestah do 16. ure.
# Zastoji: Na cesti Vič - Brezovica, Izola Strunjan in Šmarje - Koper. Na primorski hitri cesti med priključkoma Bertoki in Koper proti Izoli. - Med Postojno in Brezovico na posameznih odsekih proti Ljubljani. - Med Razdrtim in Brezovico na posameznih odsekih proti Ljubljani. Na cesti Izola Strunjan in Šmarje - Koper. Na podravski avtocesti med priključkom Zakl in Gruškovjem proti Hrvaški. Pred predorom Karavanke proti Sloveniji in proti Avstriji 3 km, občasno zapirajo predor. Proti Vrhniki: - Na ljubljanski zahodni obvoznici od Kosez in mimo Kozarij. - Na ljubljanski južni obvoznici od Viča mimo Kozarij.
# # Poročilo:
# Še vedno je zastoj na ljubljanski zahodni obvoznici proti Vrhniki, ki sega vse do gorenjske avtoceste. Občasno zapirajo predor Šentvid. Prav tako je zastoj na ljubljanski južni obvoznici od Barja mimo Kozarij.
# Zastoji so tudi na primorski avtocesti med priključkom Senožeče in Brezovico na posameznih odsekih proti Ljubljani, na podravski avtocesti med priključkom Zakl in Gruškovjem proti Hrvaški in na cestah Vič - Brezovica, Lucija - Strunjan in Šmarje - Koper.
# Kolona vozil je pred predorom Karavanke, tako na avstrijski kot na slovenski strani, zato predor občasno zapirajo.
# Vozila zastajajo tudi na primorski hitri cesti med priključkoma Bertoki in Koper proti Izoli.


# # Primer 4:
# # Podatki:
# Zastoji: Na ljubljanski južni obvoznici med Rudnikom in Centrom proti Kozarjam. Na cesti Bohinj - Bled, pred Bledom.
# Dela: Delovne zapore na cesti  Ljubljana  - Zagorje:   - pri Beričevem bo zaprta do 24. ure;
# Splošno: Do 22. ure velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7,5 t.
# # Poročilo:
# Zaradi del so krajši zastoji na južni ljubljanski obvoznici med priključkoma Rudnik in Center proti Kozarjam.
# Krajši zastoji so tudi na cesti Bohinj - Bled pred Bledom.
# Zaradi delovne zapore bo cesta Ljubljana - Zagorje do polnoči zaprta pri Beričevem.
# Do 22-ih velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7 ton in pol.

def getLLM(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        device_map="auto", 
        trust_remote_code=True
    )
    return model, tokenizer

def getLLM1(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        device_map="auto", 
        trust_remote_code=True
    )
    return model, tokenizer

def executeLLM(model, tokenizer, prompt, max_new_tokens, temperature, top_p, top_k, repetition_penalty):
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).to("cpu")
    inputs = inputs.to(model.device) 
    # inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).to(model.device)
    model.eval()
    if tokenizer.eos_token_id is None:
        tokenizer.eos_token_id = tokenizer.convert_tokens_to_ids("<eos>")
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    result = tokenizer.decode(output[0].cpu(), skip_special_tokens=True)
    return result

# model_path = "./mistral_7b_local"
model_path = "./gams_9b_local"
excel, txts, data = prompts_and_responses()
gc.collect()
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()
print(torch.cuda.memory_summary())

model, tokenizer = getLLM(model_path)
rouge = evaluate.load("rouge")
predictions = []

# max_new_tokens = 50
max_new_tokens = 520
temperature = 0.51
top_p = 0.91
top_k = 50
repetition_penalty = 1.13
print("max_new_tokens, temperature, top_p, top_k, repetition_penalty")

print(max_new_tokens, temperature, top_p, top_k, repetition_penalty)
print(getPromptSLO(""))
for data, txt in zip(excel, txts):
    prompt = getPromptSLO(data)
    result = executeLLM(model, tokenizer, prompt, max_new_tokens, temperature, top_p, top_k, repetition_penalty)
    result = result.split("\nPoročilo:")[-1].strip()
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
    torch.cuda.empty_cache()

results = rouge.compute(predictions=predictions, references=txts)
print("Final")
print(results)

del model
del tokenizer
