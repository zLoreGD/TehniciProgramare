"""arsenal/aparare/parse_auth.py - esecurile de autentificare din auth.log.

Rulare (din folderul lab10):
    python -m arsenal.aparare.parse_auth start/auth.log
"""
import argparse
import re
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    """A1: (user, ip) pentru o linie 'Failed password', altfel None."""
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))


def citeste_esecuri(cale):
    """A2: lista de esecuri; robusta la randuri stricate si la fisier lipsa."""
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri


def pe_ip(esecuri):
    """A3: Counter al adreselor IP din esecuri."""
    return Counter(e["ip"] for e in esecuri)


def main():
    """A4: rezumatul pentru fisierul dat in linia de comanda."""
    p = argparse.ArgumentParser(description="Esecuri de autentificare din auth.log")
    p.add_argument("log", help="calea catre auth.log")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)

    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")


if __name__ == "__main__":
    main()
