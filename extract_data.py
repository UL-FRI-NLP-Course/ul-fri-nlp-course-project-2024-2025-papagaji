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
    with open(os.path.join(dir, filename + ".rtf"), "r", encoding="utf-8") as f:
        rtf = f.read()
    txt = rtf_to_text(rtf)
    return txt

# ustvari nov .txt file iz .rtf
def convertRTFtoTXT(indir, infile, outdir):
    txt = parseRTF(indir, infile)
    head = txt.split("\n")[0]
    print(head)
    date = re.search(r'\d{2}\.\s\d{2}\.\s\d{4}', head).group(0).split(". ")
    time = re.search(r'\d{2}\.\d{2}\s', head).group(0).strip().split(".")
    outfile = f"{date[1]}-{date[1]}-{date[2]}-{time[0]}{time[1]}.txt"
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, outfile), "w", encoding="utf-16") as out:
        out.write(txt)

# N = 10
# df = readRows('2024', N, 0)
# row = Row(df, 0)
# print(row.getB1())

# convertRTFtoTXT("data", "TMP1-2024", "data/txt")
