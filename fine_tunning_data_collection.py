import pandas as pd
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import json


def getFromInterval(df, end, minutes):
    start = end - timedelta(minutes=minutes)
    df_interval = df[(df['Datum'] >= start) & (df['Datum'] < end)]

    out = ""
    pomembno = extract_cleaned_text(df_interval, 'ContentPomembnoSLO')
    if pomembno != "":
        out += "Pomembno: " + pomembno + "\n"
    opozorila = extract_cleaned_text(df_interval, 'ContentOpozorilaSLO')
    if opozorila != "":
        out += "Opozorila: " + opozorila + "\n"
    nesrece = extract_cleaned_text(df_interval, 'ContentNesreceSLO')
    if nesrece != "":
        out += "Nesreče: " + nesrece + "\n"
    zastoji = extract_cleaned_text(df_interval, 'ContentZastojiSLO')
    if zastoji != "":
        out += "Zastoji: " + zastoji + "\n"
    ovire = extract_cleaned_text(df_interval, 'ContentOvireSLO')
    if ovire != "":
        out += "Ovire: " + ovire + "\n"
    vreme = extract_cleaned_text(df_interval, 'ContentVremeSLO')
    if vreme != "":
        out += "Vreme: " + vreme + "\n"
    dela = extract_cleaned_text(df_interval, 'ContentDeloNaCestiSLO')
    if dela != "":
        out += "Dela: " + dela + "\n"
    mednarodno = extract_cleaned_text(df_interval, 'ContentMednarodneInformacijeSLO')
    if mednarodno != "":
        out += "Mednarodno: " + mednarodno + "\n"
    splosno = extract_cleaned_text(df_interval, 'ContentSplosnoSLO')
    if splosno != "":
        out += "Splošno: " + splosno
    return out


def prompts_and_responses(folder):
    dir = os.path.dirname(__file__)
    dir = os.path.join(dir, 'data/Podatki - rtvslo.si/Promet 2024/' + folder + '/converted/')  # nastavi pravilen path !!!

    excel_data_list = []
    txt_data_list = []
    index = 0
    df = pd.read_excel('data/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx', sheet_name="2024", engine='openpyxl',
                       skiprows=0)
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y %H:%M:%S')
    for file in os.scandir(dir):
        index += 1
        if file.is_file():
            day, month, year, time = file.path.rsplit('/', 1)[1].split(".")[0].split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            hour = int(time[0:2])
            minute = int(time[2:4])

            if month == 0: # 1 edge case december 2024
                print(0)
                continue

            end = datetime(year, month, day, hour, minute)

            # taking into account that the data is in UTC and we need to convert it to CEST
            end = end - timedelta(hours=1)
            excel_data = getFromInterval(df, end, 45)

            if excel_data == "":
                excel_data = getFromInterval(df, end, 75)


            with open(file, 'r', encoding='utf-16') as file:
                lines = file.readlines()

                if len(lines) > 1 and lines[1].strip() == 'Podatki o prometu.':
                    lines = lines[2:]  # Skip first and second line
                else:
                    lines = lines[1:]

                txt_data = ''.join(lines)
                txt_data_list.append(txt_data)

            excel_data_list.append(excel_data)

    return excel_data_list, txt_data_list


def extract_cleaned_text(df_rows, column_name):
    texts = df_rows[column_name].dropna().tolist()
    dupli = []
    if len(texts) > 0:
        for i in texts:
            soup = BeautifulSoup(i, 'html.parser').get_text(separator=' ')
            stavki = re.split(r'(?<!\d)[\.!] ',
                              soup)  # razčleni po '. ' ki spredaj nima številke ('19. ura' - ne ujame)
            for j in range(len(stavki)):
                if len(stavki[j]) > 5:
                    if j < len(stavki) - 1:
                        dupli.append(stavki[j] + ".")
                    else:
                        dupli.append(stavki[j])
    unique_texts = list(set(dupli))  # Remove duplicates
    return ' '.join(unique_texts)


# Collecting data for fine-tuning
base_folder = 'data/Podatki - rtvslo.si/Promet 2024/'

input = []
output = []

for month_folder in os.listdir(base_folder):
    month_input, month_output = prompts_and_responses(month_folder)

    input.extend(month_input)
    output.extend(month_output)
    #break

data = []

for i, line in enumerate(input):
    if line == "" or output[i] == "":
        continue

    data.append({'input': line, 'output': output[i]})

split_index = int(0.9 * len(data))
train = data[:split_index]
val = data[split_index:]

print("Train:", len(train))
print("Test:", len(val))

def save_jsonl(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

save_jsonl(train, 'train_4.jsonl')
save_jsonl(val, 'val_4.jsonl')