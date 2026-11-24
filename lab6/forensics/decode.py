"""arsenal/forensics/decode.py - Lucrarea A: decoder universal.

Rulare (din folderul lab6):
    python -m arsenal.forensics.decode "U2FsdXQ="
    python -m arsenal.forensics.decode arsenal/forensics/probe/mesaj.txt --fisier
    python -m arsenal.forensics.decode --demo        # A1-A6 pe fisierele din probe/
"""
import argparse
import base64
import binascii
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

AICI = Path(__file__).resolve().parent
PROBE = AICI / "probe"
FISA = AICI / "fisa.json"


# A2 - recunosti stratul dupa forma
def ghici_strat(s: str) -> str:
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"


# A3 - desfaci stratul recunoscut
def desfa(s: str):
    """Intoarce (strat, rezultat_bytes)."""
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s)
        if strat == "hex":
            return strat, bytes.fromhex(s)
        if strat == "url":
            return strat, unquote(s).encode()
    except (binascii.Error, ValueError):
        pass                      # forma seamana cu un strat, dar nu e valid
    return "necunoscut", s.encode()


def citibil(b: bytes) -> bool:
    """True daca toti octetii sunt in 32..126."""
    return all(32 <= c < 127 for c in b)


# A4 - straturi multiple intr-o bucla
def desface_complet(val: str, max_straturi: int = 8):
    """Desface straturile pana cand nu mai recunoaste niciunul.

    Intoarce (lista_straturi, rezultat_bytes). Nu se opreste la primul rezultat
    "citibil": un strat de base64 sau hex e si el text citibil.
    """
    straturi, clar = [], val.encode()
    for _ in range(max_straturi):
        strat, b = desfa(val)
        if strat == "necunoscut":
            break
        straturi.append(strat)
        clar = b
        if not citibil(b):
            break                 # date binare: nu mai pot fi tratate ca sir
        val = b.decode()
    return straturi, clar


# A5 - XOR cu cheie de un octet
def _scor(text: str) -> float:
    """Cat de mult seamana cu text omenesc: ponderea literelor, cifrelor si semnelor uzuale."""
    uzuale = set(" _{}.,!-'")
    return sum(c.isalnum() or c in uzuale for c in text) / len(text) if text else 0.0


def sparge_xor(date: bytes):
    """Cheile (0..255) care dau text citibil, cea mai probabila prima.

    Filtrul "toti octetii imprimabili" lasa mai multe chei candidat; le ordonam dupa
    cat de mult seamana rezultatul cu text, ca cheia buna sa fie prima.
    """
    candidati = [(k, bytes(b ^ k for b in date).decode()) for k in range(256)
                 if citibil(bytes(b ^ k for b in date))]
    return sorted(candidati, key=lambda kt: _scor(kt[1]), reverse=True)


# A6 - hash prin dictionar
def sparge_hash(tinta: str, cuvinte):
    """Cuvantul al carui md5 (32) / sha1 (40) / sha256 (64) e `tinta`, sau None."""
    algo = {32: hashlib.md5, 40: hashlib.sha1, 64: hashlib.sha256}.get(len(tinta))
    if algo is None:
        return None
    for cuv in cuvinte:
        cuv = cuv.strip()
        if algo(cuv.encode()).hexdigest() == tinta.lower():
            return cuv
    return None


def _demo():
    print("== A1: text si octeti ==")
    b = "Salut".encode()
    print(b, b[0], b.hex(), bytes.fromhex(b.hex()))

    print("\n== A2/A3: recunoastere si desfacere ==")
    print(ghici_strat("%2Fetc"), ghici_strat("48656c6c6f"), ghici_strat("U2FsdXQ="))
    print(desfa("%2Fetc"), desfa("48656c6c6f"))

    print("\n== A4: straturi multiple (probe/mesaj.txt) ==")
    mesaj = (PROBE / "mesaj.txt").read_text().strip()
    straturi, clar = desface_complet(mesaj)
    print("straturi:", " -> ".join(straturi))
    print("mesaj:", clar.decode())

    print("\n== A5: XOR cu cheie de un octet (probe/xor.bin) ==")
    candidati = sparge_xor((PROBE / "xor.bin").read_bytes())
    k, text = candidati[0]
    print(f"{len(candidati)} chei dau octeti imprimabili; cea mai probabila:")
    print(f"cheie: {k} (0x{k:02x})  {text}")

    print("\n== A6: hash prin dictionar (probe/hashuri.txt) ==")
    cuvinte = (PROBE / "wordlist.txt").read_text(encoding="latin1").splitlines()
    for tinta in (PROBE / "hashuri.txt").read_text().split():
        print(f"{tinta} -> {sparge_hash(tinta, cuvinte)}")

    print("\n== Challenge: base64 peste XOR ==")
    inner = base64.b64decode((PROBE / "challenge.bin").read_text().strip())
    k, text = sparge_xor(inner)[0]
    ok = hashlib.md5(text.encode()).hexdigest() in (PROBE / "challenge_hint.txt").read_text()
    print(f"cheie: {k} (0x{k:02x})  {text}  [md5 verificat: {ok}]")


# A7 - argparse, fisa JSON
def main():
    p = argparse.ArgumentParser(description="Decoder universal (base64 / hex / url)")
    p.add_argument("intrare", nargs="?", help="un sir sau (cu --fisier) o cale")
    p.add_argument("--fisier", action="store_true", help="citeste intrarea dintr-un fisier")
    p.add_argument("--demo", action="store_true", help="ruleaza exercitiile A1-A6")
    a = p.parse_args()

    if a.demo:
        _demo()
        return
    if a.intrare is None:
        p.error("da un sir sau --demo")

    if a.fisier:
        date = Path(a.intrare).read_bytes().decode("utf-8", errors="replace").strip()
    else:
        date = a.intrare

    straturi, clar = desface_complet(date)
    fisa = {
        "strat": " -> ".join(straturi) if straturi else "necunoscut",
        "rezultat": clar.decode("utf-8", errors="replace"),
    }
    FISA.write_text(json.dumps(fisa, indent=4, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(fisa, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
