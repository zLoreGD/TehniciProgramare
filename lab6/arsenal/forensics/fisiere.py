"""arsenal/forensics/fisiere.py - Lucrarea B: forensics pe fisiere + steganografie LSB.

Rulare (din folderul lab6):
    python -m arsenal.forensics.fisiere
"""
import io
import re
import zipfile
from pathlib import Path

from PIL import Image

AICI = Path(__file__).resolve().parent
PROBE = AICI / "probe"
TERMINATOR = b"\x00"


# B1 - magic bytes
def tip_real(cale) -> str:
    cap = Path(cale).read_bytes()[:8]
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


# B2 - strings
def siruri(cale, minim: int = 4) -> list:
    date = Path(cale).read_bytes()
    return [m.decode() for m in re.findall(rb"[ -~]{%d,}" % minim, date)]


# B3 - EXIF + GPS
def _grade(valori, ref) -> float:
    d, m, s = (float(x) for x in valori)
    dec = d + m / 60 + s / 3600
    return -dec if ref in ("S", "W") else dec


def exif_text(cale) -> dict:
    from PIL.ExifTags import TAGS
    exif = Image.open(cale).getexif()
    return {TAGS.get(k, k): v for k, v in exif.items()}


def gps(cale):
    """(latitudine, longitudine) in grade zecimale, sau None daca nu exista GPS."""
    bloc = Image.open(cale).getexif().get_ifd(34853)       # tag 34853 = GPSInfo
    if not bloc or 2 not in bloc or 4 not in bloc:
        return None
    return (_grade(bloc[2], bloc.get(1)), _grade(bloc[4], bloc.get(3)))


# B4 - file carving
def carving(cale, iesire=None):
    """Scoate arhiva ZIP lipita la coada unui fisier; intoarce {nume: continut}."""
    date = Path(cale).read_bytes()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None
    iesire = Path(iesire or AICI / "gasit.zip")
    iesire.write_bytes(date[i:])
    with zipfile.ZipFile(io.BytesIO(date[i:])) as z:
        return {nume: z.read(nume).decode("utf-8", errors="replace") for nume in z.namelist()}


# B5 / B6 - LSB
def _pixeli(img):
    return list(img.get_flattened_data()) if hasattr(img, "get_flattened_data") else list(img.getdata())


def ascunde(sursa, mesaj: bytes, destinatie):
    """Scrie `mesaj` (+ terminator) in bitul cel mai putin semnificativ al canalelor RGB."""
    img = Image.open(sursa).convert("RGB")
    biti = "".join(f"{x:08b}" for x in mesaj + TERMINATOR)
    canale = [c for px in _pixeli(img) for c in px]
    if len(biti) > len(canale):
        raise ValueError("mesaj prea lung pentru imagine")
    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & ~1) | int(bit)
    img.putdata([tuple(canale[i:i + 3]) for i in range(0, len(canale), 3)])
    img.save(destinatie)                                    # PNG: fara pierderi


def dezvaluie(cale) -> bytes:
    canale = [c for px in _pixeli(Image.open(cale).convert("RGB")) for c in px]
    rezultat = bytearray()
    for i in range(0, len(canale) - 7, 8):
        octet = int("".join(str(c & 1) for c in canale[i:i + 8]), 2)
        if octet == 0:
            break
        rezultat.append(octet)
    return bytes(rezultat)


def main():
    foto, ascuns = PROBE / "foto.jpg", PROBE / "ascuns.png"

    print("== B1: tipul real ==")
    for f in (foto, ascuns, PROBE / "mesaj.txt"):
        print(f"{f.name}: {tip_real(f)}")

    print("\n== B2: strings din ascuns.png ==")
    for s in siruri(ascuns):
        print(" ", s)

    print("\n== B3: EXIF si GPS din foto.jpg ==")
    for k, v in exif_text(foto).items():
        print(f"  {k} = {v}")
    lat, lon = gps(foto)
    print(f"  GPS: latitudine {lat:.4f}, longitudine {lon:.4f}")

    print("\n== B4: file carving din ascuns.png ==")
    for nume, continut in carving(ascuns).items():
        print(f"  {nume}: {continut.strip()}")

    print("\n== B5: ascund mesajul in stego.png ==")
    ascunde(foto, b"FLAG{ascuns_in_pixeli}", AICI / "stego.png")
    print("  scris:", AICI / "stego.png")

    print("\n== B6: dezvalui mesajul ==")
    print(" ", dezvaluie(AICI / "stego.png").decode())


if __name__ == "__main__":
    main()
