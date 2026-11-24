# arsenal/forensics/amprente.py - amprentele fisierelor dintr-un folder.
#
# Rulare:
#     python amprente.py                 # scaneaza probe/ de langa acest fisier
#     python amprente.py cale/folder     # scaneaza alt folder
import argparse
import hashlib
import os

AICI = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join(AICI, "probe")            # nu depinde de folderul curent

MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    """Tipul real dupa primii octeti (magic bytes)."""
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"       # dupa bucla: doar daca NICIO semnatura nu se potriveste


def amprenta_fisier(cale):
    with open(cale, "rb") as f:               # "rb": octeti, nu text
        date = f.read()
    return {
        "nume": os.path.basename(cale),
        "tip": tip(date[:8]),
        "sha256": hashlib.sha256(date).hexdigest()[:16],   # primele 16 caractere
    }


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
    parser.add_argument("folder", nargs="?", default=PROBE,
                        help="Directorul care trebuie scanat (implicit: probe/)")
    args = parser.parse_args()

    for fisier in scaneaza(args.folder):
        print(f"{fisier['nume']:14} {fisier['tip']:11} {fisier['sha256']}")


if __name__ == "__main__":
    main()