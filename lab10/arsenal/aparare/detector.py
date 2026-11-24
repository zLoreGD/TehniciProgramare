"""arsenal/aparare/detector.py - detector de brute force.

Rulare (din folderul lab10):
    python -m arsenal.aparare.detector start/auth.log
    python -m arsenal.aparare.detector start/auth.log --prag 2 --json
"""
import argparse
import json
from collections import Counter

from .parse_auth import citeste_esecuri


def suspecti(counts, prag=10):
    """B1: [(ip, n)] cu n >= prag, in ordine descrescatoare."""
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return sorted(
        [(ip, n) for ip, n in counts.items() if n >= prag],
        key=lambda x: x[1],
        reverse=True,
    )


def main():
    p = argparse.ArgumentParser(description="Detector de brute force")
    p.add_argument("log", help="calea catre auth.log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": [{"ip": ip, "incercari": n} for ip, n in sus],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print(f"Esecuri de autentificare: {len(esecuri)}\n")
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")
    print(f"\nSuspecti (prag {a.prag}):")
    for ip, n in sus:
        print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
