import pandas as pd
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

def getFromInterval(df, end, rec=0, delta=45):
    start = end - timedelta(minutes=delta)
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
    if out == "" and rec < 5:
        out = getFromInterval(df, start, rec + 1, 30) #try again with older data
    return out


def inputs_and_responses(year=2023, chosen_txts_dir='out/chosen_txts/'):
    dir = os.path.dirname(__file__) 
    dir_txts = os.path.join(dir, chosen_txts_dir) 

    excel_data_list = []
    txt_data_list = []
    file_list = []
    index = 0
    df = pd.read_excel('data/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx', sheet_name=str(year), engine='openpyxl', skiprows=0)
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y %H:%M:%S')
    for file in os.scandir(dir_txts):  
        index += 1
        if file.is_file(): 
            
            day,month,year,time = file.path.rsplit('/', 1)[1].split(".")[0].split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            hour = int(time[0:2])
            minute = int(time[2:4])

            end = datetime(year, month, day, hour-1, minute)
            excel_data = getFromInterval(df, end)
            excel_data_list.append(excel_data)
            file_list.append(file)

            with open(file, 'r', encoding='utf-16') as file:
                lines = file.readlines()
                txt_data = ''.join(lines)
                txt_data_list.append(txt_data)

    return excel_data_list, txt_data_list, file_list

def extract_cleaned_text(df_rows, column_name):
    texts = df_rows[column_name].dropna().tolist()
    dupli = []
    if len(texts) > 0:
        for i in texts:
            soup = BeautifulSoup(i, 'html.parser').get_text(separator=' ')
            stavki = re.split(r'(?<!\d)[\.!] ', soup) # razčleni po '. ' ki spredaj nima številke ('19. ura' - ne ujame)
            for j in range(len(stavki)):
                if len(stavki[j]) > 5:
                    if j < len(stavki) - 1:
                        dupli.append(stavki[j] + ".")
                    else:
                        dupli.append(stavki[j])
    unique_texts = list(set(dupli))  # Remove duplicates
    return ' '.join(unique_texts)
