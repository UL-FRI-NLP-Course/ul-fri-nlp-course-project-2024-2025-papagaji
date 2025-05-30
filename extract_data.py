import os
from os.path import isfile, join
from striprtf.striprtf import rtf_to_text
import re

def parseRTF(dir, filename):
    with open(os.path.join(dir, filename + ".rtf"), "r", encoding="utf-8") as f:
        rtf = f.read()
    txt = rtf_to_text(rtf)
    return txt

# ustvari nov .txt file iz .rtf
def convertRTFtoTXT(indir, infile, outdir):
    txt = parseRTF(indir, infile)
    head = txt.split("\n")[0]
    pattern = r'(\d{1,2})\.?\s?(\d{1,2})\.?\s?(\d{4})\s+(\d{1,2})\s?[\.,:]\s?(\d{2})'
    match = re.search(pattern, head)
    if match:
        day, month, year, hour, minute = match.groups()
        outfile = f"{day.zfill(2)}-{month.zfill(2)}-{year}-{hour.zfill(2)}{minute}.txt"
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, outfile), "w", encoding="utf-16") as out:
            out.write(txt)


# pretvori celoten folder iz .rtf v .txt
def convertAllRTFtoTXT(indir, outdir):
    onlyfiles = [f for f in os.listdir(indir) if isfile(join(indir, f))]
    for file in onlyfiles:
        if file.endswith(".rtf"):
            convertRTFtoTXT(indir, file[:-4], outdir)


dir = os.path.dirname(__file__) 
path1 = os.path.join(dir, "data/RTVSlo/Podatki - rtvslo.si")
path2 = os.path.join(dir, "data/txts")


for subdir, dirs, files in os.walk(path1):
    convertAllRTFtoTXT(subdir, path2)
