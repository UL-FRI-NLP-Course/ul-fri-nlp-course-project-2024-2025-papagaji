from bs4 import BeautifulSoup
import pandas as pd 
import os
from os.path import isfile, join
import re
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup

def get_excel_data(day,month,year,start_hour,start_minute):

    df = pd.read_excel('data/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx', sheet_name=str(year))

    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y %H:%M:%S')


    start_time = datetime(year, month, day, start_hour, start_minute)
    end_time = start_time + timedelta(minutes=30)

    #print(start_time)
    #print(end_time)
    #print()

    df_interval = df[(df['Datum'] >= start_time) & (df['Datum'] < end_time)]


    def extract_cleaned_text(df_rows, column_name):
        texts = df_rows[column_name].dropna().tolist()
        unique_texts = list(set(texts))  # Remove duplicates
        combined = ' '.join(unique_texts)
        return BeautifulSoup(combined, 'html.parser').get_text(separator=' ').strip()

    dela = extract_cleaned_text(df_interval, 'ContentDeloNaCestiSLO')
    mednarodno = extract_cleaned_text(df_interval, 'ContentMednarodneInformacijeSLO')
    nesrece = extract_cleaned_text(df_interval, 'ContentNesreceSLO')
    opozorila = extract_cleaned_text(df_interval, 'ContentOpozorilaSLO')
    ovire = extract_cleaned_text(df_interval, 'ContentOvireSLO')
    pomembno = extract_cleaned_text(df_interval, 'ContentPomembnoSLO')
    splosno = extract_cleaned_text(df_interval, 'ContentSplosnoSLO')
    vreme = extract_cleaned_text(df_interval, 'ContentVremeSLO')
    zastoji = extract_cleaned_text(df_interval, 'ContentZastojiSLO')



    return "Dela: " + dela + "\nMednarodno: " + mednarodno + "\nNesrece: " + nesrece + "\nOpozorila: " + opozorila + "\nOvir: " + ovire + "\nPomembno: " + pomembno + "\nSplosno: " + splosno + "\nVreme: " + vreme + "\nZastoji: " + zastoji





dir = os.path.dirname(__file__) 
dir = os.path.join(dir, 'data/txt/')

test = []

id = 0
for file in os.scandir(dir):  
    id += 1
    if file.is_file(): 

        day,month,year,time = file.path.rsplit('/', 1)[1].split(".")[0].split("-")
        day = int(day)
        month = int(month)
        year = int(year)
        hour = int(time[0:2])
        minute = int(time[2:4])

        excel_data = get_excel_data(day,month,year,hour,minute)

        contents = open(file,encoding="utf-16").read()

        #TODO nisem ziher glede formata za datasete
        test.append({
        "id": id,
        "prompt": excel_data,
        "completion": contents,
        })




for t in test:
    print(t)
    print()





"""t = {
"id": 25,
"prompt": "Write a LinkedIn post to announce that you have accepted a new job offer.\n Input: ",
"completion": "“I’m excited beyond words to share with you my decision to accept the role of Marketing Director at the XYZ Company!\nI couldn’t have had this opportunity if not for the help of my friend, [name], who shared this job opportunity with me, and my former boss, [boss’s name], for her stellar recommendation and guidance.\nI happily look forward to starting this new journey and growing professionally with my new family—the marketing rock stars of XYZ Company.”",
}

print(t)"""