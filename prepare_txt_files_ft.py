import os
from striprtf.striprtf import rtf_to_text
import re

def parseRTF(dir, filename):
    with open(os.path.join(dir, filename), "r", encoding="utf-8") as f:
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