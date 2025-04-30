import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


df = pd.read_excel('data/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx', sheet_name='2024')

df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y %H:%M:%S')

start_time = datetime(2024, 1, 1, 16, 0)
end_time = datetime(2024, 1, 1, 16, 30)
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

print("Dela: ", dela)
print("Mednarodno: ", mednarodno)
print("Nesrece: ", nesrece)
print("Opozorila: ", opozorila)
print("Ovir: ", ovire)
print("Pomembno: ", pomembno)
print("Splosno: ", splosno)
print("Vreme: ", vreme)
print("Zastoji: ", zastoji)