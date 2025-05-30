import time

print("Starting imports...")
start = time.time()

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch


model_path = "./gams9b-finetuned_9"
tokenizer = AutoTokenizer.from_pretrained(model_path)

base_model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)

model = PeftModel.from_pretrained(
    base_model,
    model_path,
    device_map="auto"
)

print("Setup took", time.time() - start, "seconds")


data= '''
Dela:  V Ljubljani je zaprta Šmartinska cesta   med Novimi  Jaršami  in  Sneberjami  zaradi rekonstrukcije, do 31. avgusta. Obvoz je po avtocesti priključkoma Nove Jarše in Sneberje v obe smeri, tudi za vozila brez vinjete. Na gorenjski avtocesti: -  Zaprt  je  priključek Radovljica proti Ljubljani,  predvidoma do 23. 6. Obvoz je preko priključka Lesce. - Nocoj 13./14. 6. med 20. in 5. uro bo promet skozi predor Karavanke potekal izmenično enosmerno s čakalno dobo pred predorom. - v predoru Karavanke bodo zaradi miniranja na avstrijski strani predvidoma do marca 2024 potekale kratkotrajne zapore, do 4 krat dnevno. V sredo, 14. 6. med 23. in 23.30, je predvidena 30 minutna popolna zapora na štajerski avtocesti med Krtino in Domžalami v obe smeri zaradi postavitve portala. Možni bodo zastoji. Zaradi snemanja vozišča bo v sredo in četrtek dopoldne promet oviran na primorski avtocesti in vipavski hitri cesti. Več o delovnih zaporah v prometni napovedi . 
Nesrece:  Na južni ljubljanski obvoznici je na izvozu Rudnik iz smeri razcepa Malence močno oviran promet.
Opozorila:  Zaradi mednarodne kolesarske dirke "Tour of Slovenia 2023" bodo od srede, 14. junija, do nedelje, 18. junija, 30 do 60 minutne popolne zapore nekaterih glavnih cest.  Več o prireditvi in zaporah cest.
Zastoji:  Na cesti Hrpelje - Kozina. Na severni ljubljanski obvoznici v delovni zapori proti razcepu Zadobrova. Zaradi popoldanske prometne konice je promet povečan na cestah iz mestnih središč ter na mestnih obvoznicah.   Na cesti Hrpelje - Kozina. Zaradi popoldanske prometne konice je promet povečan na cestah iz mestnih središč ter na mestnih obvoznicah.
'''

print("\n\n")

inputs = tokenizer(data + tokenizer.eos_token, return_tensors="pt").to(model.device)

output = model.generate(
    **inputs,
    max_new_tokens=150,
    do_sample=True,
    temperature=0.5,
    top_p=0.9,
    top_k=50,
    repetition_penalty=1.12,
)

generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

print("Generated text:")
line_count = len(data.splitlines())
result_lines = generated_text.splitlines()[line_count:]
result_text = "\n".join(result_lines)
print(result_text)
