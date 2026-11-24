# arsenal/forensics/amprente.py (DE REPARAT - contine 3 greseli)
# Ruleaza suita (pytest) in Lucrarea B: vei vedea testele picand. Repara pe rand,
# cate o greseala, pana la "3 passed". NU modifica testele si NU modifica probele.
import os, hashlib
import argparse
MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"          # greseala 1

print(tip(b"\x89PNG\r\n"), tip(b"%PDF-1.4"), tip(b"text"))

def amprenta_fisier(cale):
    with open(cale,"rb") as f:             # greseala 2
        date = f.read()
    return {"nume": os.path.basename(cale),
        "tip": tip(date[:8]),
        "sha256": hashlib.sha256(date).hexdigest()[:16]}   # greseala 3

print(amprenta_fisier("/home/vlad/Desktop/Univer/tehniciprogramare/lab13/probe/imagine.png"))
def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez

def main():
    parser = argparse.ArgumentParser(
        description="Scaneaza fisierele si calculeaza amprentele SHA256."
    )

    parser.add_argument("folder", help="Directorul care trebuie scanat")

    args = parser.parse_args()

    rezultate = scaneaza(args.folder)

    for fisier in rezultate:
        print(
            f"{fisier['nume']:14} "
            f"{fisier['tip']:11} "
            f"{fisier['sha256']}"
        )


if __name__ == "__main__":
    main()

