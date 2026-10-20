s = "Salut"
b = s.encode()
print(b,b[0])
print(b.hex())
print(bytes.fromhex(b.hex()))



import re
def ghici_strat(s)->str:
    # TODO: daca are %xx -> "url"
    if re.search(r'%[0-9a-fA-F]{2}',s):
        return "url"
    # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        return "hex"
    # TODO: daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r'[A-Za-z0-9+/=]+', s):
        return "base64"
    
    return "necunoscut"
print(ghici_strat("%2Fetc"))   # url
print(ghici_strat("48656c6c6f"))  # hex


import base64
from urllib.parse import unquote
def desfa(s):
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    #   base64 -> base64.b64decode(s)
    #   hex    -> bytes.fromhex(s)
    #   url    -> unquote(s).encode()
    # intoarce (strat, rezultat_bytes)
    rezultat_bytes = b""
    if strat == "base64":
        rezultat_bytes = base64.b64decode(s)
    if strat == "hex":
        rezultat_bytes = bytes.fromhex(s)
    elif strat == "url":
        rezultat_bytes = unquote(s).encode()
    
    return strat, rezultat_bytes
print(desfa("%2Fetc"))   # url
print(desfa("48656c6c6f"))  # hex


def citibil(b):
    # TODO: True daca toti octetii sunt 32..126

    return all(32 <= c < 127 for c in b)
 
val = "NTM1OTU3NTk="
for _ in range(8):
    strat, b = desfa(val)
    # TODO: daca citibil(b): opreste si tipareste
    #       altfel val = b.decode(); continua
    if citibil(b):  
        print(b.decode())
        break
    else:
        val = b.decode()

date = open("forensics/probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    # TODO: daca citibil(clar):
    #       print("cheie:", k, clar.decode())
    if citibil(clar):
        print('cheie: ',k, clar.decode())


import hashlib
tinta = open("forensics/probe/hashuri.txt").readline().strip()
print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
for cuv in open("forensics/probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()
    # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
    #       == tinta: print("gasit:", cuv); break
    if hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit",cuv)
        break
"""
import argparse, json
p = argparse.ArgumentParser()
p.add_argument("intrare")          # sir sau cale
p.add_argument("--fisier", action="store_true")
a = p.parse_args()
# TODO: daca a.fisier, citeste octetii din cale;
#       altfel trateaza intrarea ca sir
# TODO: salveaza {strat, rezultat} in
#       arsenal/forensics/fisa.json
# teste/test_decode.py
if a.fisier:
    with open(a.intrare,"r") as f:
        date = f.read()
else:
    date = a.intrare.encode()
strat, rezultat_bytes = desfa(date)

rezultat = {
    "strat": strat,
    "rezultat": rezultat_bytes.decode("utf-8", errors="replace")
}

with open("forensics/fisa.json", "w", encoding="utf-8") as f:
    json.dump(rezultat, f, indent=4, ensure_ascii=False)
"""

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    # TODO: daca cap incepe cu b"%PDF" -> "pdf"
    #       b"\x89PNG" -> "png" ; b"\xff\xd8" -> "jpeg"
    #       b"PK\x03\x04" -> "zip/docx"
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()
print(tip_real("forensics/probe/foto.jpg"))
import re
date = open("forensics/probe/ascuns.png", "rb").read()
# TODO: for m in re.findall(rb"[ -~]{4,}", date):
#           print(m.decode())
# cauta un indiciu: o cale, un mesaj, un nume de fisier
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())



from PIL import Image
from PIL.ExifTags import TAGS
exif = Image.open("forensics/probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
# TODO: ia blocul GPS (tag 34853) si tipareste
#       latitudinea si longitudinea


date = open("forensics/probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
# TODO: daca i != -1:
#   open("gasit.zip","wb").write(date[i:])
#   print("arhiva extrasa de la octetul", i)
# apoi dezarhiveaza si vezi ce era inauntru
if i != -1:
    open("gasit.zip","wb").write(date[i:])
    print('arhiva extrasa de la octetul', i)

from PIL import Image
img = Image.open("forensics/probe/foto.jpg").convert("RGB")
px = list(img.get_flattened_data())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = list(px)
# TODO: pentru fiecare bit, ia un canal si pune
#   canal = (canal & ~1) | int(bit)
# TODO: img.putdata(px_nou); img.save("stego.png")
for i, bit in enumerate(biti):
    pixel_index = i // 3
    canal_index = i % 3

    if pixel_index >= len(px_nou):
        break

    pixel = list(px_nou[pixel_index])
    canal = pixel[canal_index]

    pixel[canal_index] = (canal & ~1) | int(bit)
    px_nou[pixel_index] = tuple(pixel)

img.putdata(px_nou)
img.save("stego.png")

px = list(Image.open("stego.png").convert("RGB").get_flattened_data())
biti = ""

for r, g, b in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)


octeti = []

for i in range(0, 22 * 8, 8):
    octet = int(biti[i:i+8], 2)
    octeti.append(octet)

mesaj = bytes(octeti).decode("utf-8")
print(mesaj)
