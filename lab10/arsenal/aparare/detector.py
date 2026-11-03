def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")

    return sorted(
        [(ip, n) for ip, n in counts.items() if n >= prag],
        key=lambda x: x[1],
        reverse=True
    )
 
from collections import Counter
c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
print(suspecti(c))
print(suspecti(c, prag=2))

import argparse
import json
from collections import Counter
from .parse_auth import citeste_esecuri


def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
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
            "suspecti": [
                {"ip": ip, "incercari": n}
                for ip, n in sus
            ]
        }

        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print(f"Esecuri de autentificare: {len(esecuri)}")
    print()

    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")

    print()
    print(f"Suspecti (prag {a.prag}):")

    for ip, n in sus:
        print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()