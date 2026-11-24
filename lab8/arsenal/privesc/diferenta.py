"""arsenal/privesc/diferenta.py - ce SUID a aparut fata de un sistem curat.

Rulare (din folderul lab8):
    python -m arsenal.privesc.diferenta
    python -m arsenal.privesc.diferenta start/baza_suid.txt start/suid.txt
"""
import argparse
from pathlib import Path

from .enumerare import GTFO, citeste_linii, nume

RADACINA = Path(__file__).resolve().parents[2]      # folderul lab8


def cai(fisier) -> set:
    """B1: MULTIMEA cailor din fisier."""
    return set(citeste_linii(fisier))


def noi_fata_de_baza(acum: set, baza: set) -> set:
    """B2: caile aparute fata de sistemul curat."""
    return acum - baza


def periculoase(noi: set) -> list:
    """B3: dintre cele noi, cele din dictionarul de risc (GTFO)."""
    return [c for c in sorted(noi) if nume(c) in GTFO]


def main():
    p = argparse.ArgumentParser(description="Diferenta SUID: curat vs acum")
    p.add_argument("baza", nargs="?", default=RADACINA / "start" / "baza_suid.txt")
    p.add_argument("acum", nargs="?", default=RADACINA / "start" / "suid.txt")
    a = p.parse_args()

    baza, acum = cai(a.baza), cai(a.acum)
    print("baza:", len(baza), " acum:", len(acum))

    noi = noi_fata_de_baza(acum, baza)
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    print("periculoase NOI:", periculoase(noi))


if __name__ == "__main__":
    main()
