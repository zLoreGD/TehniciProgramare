"""arsenal/privesc/enumerare.py - enumerare SUID / sudo / cron.

Rulare (din folderul lab8):
    python -m arsenal.privesc.enumerare start           # rezumat + salveaza enum.json
    python -m arsenal.privesc.enumerare start --json    # doar JSON curat pe stdout
"""
import argparse
import json
import os

# A3: executabile pentru care exista tehnici de escaladare (GTFOBins)
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def citeste_linii(cale) -> list:
    """A1: liniile curate din fisier (fara goluri si fara comentarii)."""
    with open(cale, encoding="utf-8") as f:
        linii = []
        for linie in f:
            linie = linie.strip()
            if linie and not linie.startswith("#"):
                linii.append(linie)
        return linii


def nume(cale) -> str:
    """A2: numele executabilului dintr-o cale ('/bin/cp' -> 'cp')."""
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale) -> list[dict]:
    """A3: lista de dictionare {cale, nume, risc}, fara duplicate."""
    rezultat = []
    for path in sorted(set(citeste_linii(cale))):
        rezultat.append({
            "cale": path,
            "nume": nume(path),
            "risc": "mare" if nume(path) in GTFO else "normal",
        })
    return rezultat


def sudo_constatari(cale) -> list[dict]:
    """A4: o linie 'user : drept' -> dict cu risc mare daca are NOPASSWD."""
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)          # despachetare in tuplu
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal",
        })
    return out


def cron_constatari(cale) -> list[dict]:
    """A4: o linie crontab -> user (campul 6) si comanda (restul)."""
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        out.append({
            "user": campuri[5],
            "comanda": " ".join(campuri[6:]),
        })
    return out


def enumereaza(d) -> dict:
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


def utilizatori_implicati(raport) -> set:
    """Multimea userilor din sudo REUNITA cu cei din cron."""
    useri_sudo = {c["user"] for c in raport["sudo"]}
    useri_cron = {c["user"] for c in raport["cron"]}
    return useri_sudo | useri_cron


def main():
    p = argparse.ArgumentParser(description="Enumerare SUID/sudo/cron")
    p.add_argument("capturi", help="folderul cu suid.txt, sudo.txt, crontab.txt")
    p.add_argument("--json", action="store_true", help="scoate doar JSON curat")
    a = p.parse_args()

    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    print("utilizatori implicati:", sorted(utilizatori_implicati(raport)))

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
