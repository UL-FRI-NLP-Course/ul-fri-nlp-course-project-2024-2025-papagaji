from bs4 import BeautifulSoup
import pandas as pd 
import os
from striprtf.striprtf import rtf_to_text
import re

#55k + 57k + 58k = 170k vrstic

class Row():
    def __init__(self, df, offset):
        self.data = []
        self.string = ""
        for i in range(27):
            row = str(df.iloc[offset, i])
            if row[0] == '<':
                txt = parseHTML(row)
                self.data.append(txt)
                self.string += txt + "\n"
            else:
                self.data.append(row)
    def toString(self): # vrne vse vrstice združene
        return self.string
    def getTime(self):
        return self.data[1]
    def getA1(self): # isto kot Pomembno(?)
        return self.data[3]
    def getB1(self): # ostale novice združene
        return self.data[4]
    def getPomembno(self):
        return self.__addTitle(10)
    def getNesrece(self):
        return self.__addTitle(12)
    def getZastoji(self):
        return self.__addTitle(14)
    def getVreme(self):
        return self.__addTitle(16)
    def getOvire(self):
        return self.__addTitle(18)
    def getDela(self):
        return self.__addTitle(20)
    def getOpozorila(self):
        return self.__addTitle(22)
    def getMednarodno(self):
        return self.__addTitle(24)
    def getSplosno(self):
        return self.__addTitle(26)
    def getCol(self, i):
        return self.data[i]
    def __addTitle(self, i):
        if self.data[i-1] != "nan":
            return self.data[i-1] + "\n" + self.data[i]
        return self.data[i]

# prebere n vrstic od offseta naprej
def readRows(sheet, n, offset):
    df = pd.read_excel('data/Podatki - PrometnoPorocilo_2022_2023_2024.xlsx', sheet_name=sheet, engine='openpyxl', skiprows=offset, nrows=n)
    return df

def parseHTML(html, removeA=True):
    soup = BeautifulSoup(html, 'html.parser')
    if removeA: #odstranimo hyperlinke
        for a in soup.find_all('a'):
            a.decompose()
    txt = soup.get_text(separator=" ", strip=True)
    return txt

def parseRTF(dir, filename):
    with open(os.path.join(dir, filename), "r", encoding="utf-8") as f:
        rtf = f.read()
    txt = rtf_to_text(rtf)
    return txt

# ustvari nov .txt file iz .rtf
def convertRTFtoTXT(indir, infile, outdir):
    txt = parseRTF(indir, infile)
    head = txt.split("\n")[0]
    # print(head)
    pattern = r'(\d{1,2})\.?\s?(\d{1,2})\.?\s?(\d{4})\s+(\d{1,2})\s?[\.,:]\s?(\d{2})'
    match = re.search(pattern, head)
    if match:
        day, month, year, hour, minute = match.groups()
        outfile = f"{day.zfill(2)}-{month.zfill(2)}-{year}-{hour.zfill(2)}{minute}.txt"

        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, outfile), "w", encoding="utf-16") as out:
            out.write(txt)

base_folder = 'data/Podatki - rtvslo.si/Promet 2024/'

for month_folder in os.listdir(base_folder):
    full_month_path = os.path.join(base_folder, month_folder)

    converted_folder = os.path.join(full_month_path, "converted2")
    os.makedirs(converted_folder, exist_ok=True)

    for file in os.scandir(full_month_path):
        full_file_path = os.path.join(full_month_path, file)
        if file.is_file():
            try:
                convertRTFtoTXT(full_month_path, file.name, converted_folder)
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError in {file}: {e}")
            except Exception as e:
                print(f"Error processing {file}: {e}")