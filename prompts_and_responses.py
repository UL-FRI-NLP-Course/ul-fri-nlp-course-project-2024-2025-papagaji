from bs4 import BeautifulSoup
import pandas as pd 
import os
from os.path import isfile, join
import re
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup
from ara_2 import generate
from pathlib import Path


def get_excel_data(day,month,year,end_hour,end_minute):
    dir = os.path.dirname(__file__) 
    df = pd.read_excel(os.path.join(dir, 'data/RTVSlo/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx'), sheet_name=str(year))

    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y %H:%M:%S')

    end_time = datetime(year, month, day, end_hour, end_minute)

    num_mins = 45
    found_anything = False
    while(not found_anything):

        print("MINUTE: " + str(num_mins))
        start_time = end_time - timedelta(minutes=num_mins)

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

        num_mins += 15

        if(not (dela == "" and mednarodno == "" and nesrece == "" and opozorila == "" and ovire == "" and pomembno == "" and splosno == "" and vreme == "" and zastoji == "")):
            found_anything = True

    print("START = " + start_time.strftime("%H.%M") + "END = " + end_time.strftime("%H.%M") )

    datum = end_time.strftime("%d. %m. %Y")
    ura = end_time.strftime("%H.%M")
    
    out = "\nDatum: " + datum + "\nUra: " + ura + "\n"
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

    
def prompts_and_responses():
    dir = os.path.dirname(__file__) 
    dir = os.path.join(dir, 'data/txt/')

    excel_data_list = []
    txt_data_list = []

    index = 0
    for file in os.scandir(dir):  
        index += 1
        if file.is_file(): 

            day,month,year,time = file.path.rsplit('/', 1)[1].split(".")[0].split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            hour = int(time[0:2])
            minute = int(time[2:4])

            excel_data = get_excel_data(day,month,year,hour,minute)
            excel_data_list.append(excel_data)

            txt_data = open(file,encoding="utf-16").read()
            txt_data_list.append(txt_data)

            # TODO currently just gets first 5 pairs of data
            if(index == 1):
                return excel_data_list, txt_data_list


def responses_write_to_file(chosen_txts_dir='generate_responses_prompt_engineering/chosen_txts/',results_dir='generate_responses_prompt_engineering/results_txt/',inputs_dir='generate_responses_prompt_engineering/inputs/',generate_responses=True):
    dir_ = os.path.dirname(__file__) 
    dir = os.path.join(dir_, chosen_txts_dir)

    write_dir = os.path.join(dir_, results_dir)
    write_dir_inputs = os.path.join(dir_, inputs_dir)

    index = 0
    for file in os.scandir(dir):  

        outfile = os.path.join(write_dir, "result_" + file.name)
        outfile_inputs = os.path.join(write_dir_inputs, "data_" + file.name)

        outfile_path = Path(outfile)

        if(outfile_path.is_file()):
            print("Results for this file already exist! skipping.")
            continue

        index += 1
        if file.is_file(): 
            day,month,year,time = file.path.rsplit('/', 1)[1].split(".")[0].split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            hour = int(time[0:2])
            minute = int(time[2:4])

            print(day,month,year,hour,minute)

            excel_data = get_excel_data(day,month,year,hour,minute)
            print("excel:")
            print(excel_data)

            result = ""
            if (generate_responses):
                result = generate(excel_data)
            print(result)
            if(generate_responses):
                try:
                    with open(outfile, "x", encoding="utf-16") as out:
                        out.write(result)
                except:
                    try:
                        with open(outfile, "w", encoding="utf-16") as out:
                            out.write(result)
                    except:
                        print("Could not write file!")

            try:
                with open(outfile_inputs, "x", encoding="utf-16") as out:
                    out.write(excel_data)
            except:
                try:
                    with open(outfile_inputs, "w", encoding="utf-16") as out:
                        out.write(excel_data)
                except:
                    print("Could not write file!")

            

responses_write_to_file(generate_responses=False)