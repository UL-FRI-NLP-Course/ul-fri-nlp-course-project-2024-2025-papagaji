from bs4 import BeautifulSoup
import pandas as pd 
import os
from os.path import isfile, join
from striprtf.striprtf import rtf_to_text
import re
import datetime

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
        date, time = self.data[1].split()
        date = date.split('-')
        time = time.split(':')
        return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
    def getA1(self): # isto kot Pomembno(?)
        return self.data[3]
    def getB1(self): # ostale novice združene
        return self.data[4]
    def getPomembno(self, title=False):
        return self.getCol(10, title)
    def getNesrece(self, title=False):
        return self.getCol(12, title)
    def getZastoji(self, title=False):
        return self.getCol(14, title)
    def getVreme(self, title=False):
        return self.getCol(16, title)
    def getOvire(self, title=False):
        return self.getCol(18, title)
    def getDela(self, title=False):
        return self.getCol(20, title)
    def getOpozorila(self, title=False):
        return self.getCol(22, title)
    def getMednarodno(self, title=False):
        return self.getCol(24, title)
    def getSplosno(self, title=False):
        return self.getCol(26, title)
    def getCol(self, i, title=False):
        if self.data[i] == "nan" or len(self.data[i]) < 5:
            return ""
        if title:
            return self.__addTitle(i)
        return self.data[i] + "\n"
    def getAll(self):
        return (self.getPomembno() + self.getNesrece() + self.getZastoji() + self.getVreme() + self.getOvire() + self.getDela() + self.getOpozorila() + self.getMednarodno() + self.getSplosno()).strip()
    def __addTitle(self, i):
        if self.data[i-1] != "nan":
            return self.data[i-1] + ": " + self.data[i]
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
    # date = re.search(r'\d{2}\.\s?\d{1,2}\.\s?\d{4}', head)
    # time = re.search(r'\d{1,2}\.\d{2}\s?', head)
    # if date is None or time is None:
    #     print(head)
    #     return
    # date = date.group(0).split(". ")
    # time = time.group(0).strip().split(".")
    pattern = r'(\d{1,2})\.?\s?(\d{1,2})\.?\s?(\d{4})\s+(\d{1,2})\s?[\.,:]\s?(\d{2})'
    match = re.search(pattern, head)
    if match:
        day, month, year, hour, minute = match.groups()
        outfile = f"{day.zfill(2)}-{month.zfill(2)}-{year}-{hour.zfill(2)}{minute}.txt"
        #print(outfile)
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, outfile), "w", encoding="utf-16") as out:
            out.write(txt)
    # else:
    #     print(head)

# pretvori celoten folder iz .rtf v .txt
def convertAllRTFtoTXT(indir, outdir):
    onlyfiles = [f for f in os.listdir(indir) if isfile(join(indir, f))]
    for file in onlyfiles:
        if file.endswith(".rtf"):
            convertRTFtoTXT(indir, file[:-4], outdir)


convertAllRTFtoTXT("data/Januar 2022", "data/txt")

# N = 1
# df = readRows('2024', N, 0)
# row = Row(df, 0)
# print(row.getAll())
