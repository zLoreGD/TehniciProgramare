"""arsenal/windows/inventar.py - procese si evenimente Windows ca obiecte.

Rulare (din folderul lab11):
    python -m arsenal.windows.inventar start
    python -m arsenal.windows.inventar start --json
"""
import argparse
import json
import os
from dataclasses import asdict, dataclass

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self) -> bool:
        """A2: True daca ruleaza dintr-un folder tipic pentru malware."""
        return any(c in self.cale for c in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self) -> bool:
        """A3: True daca id-ul e in SUSPECTE_ID SAU nivelul e 'critical'."""
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale) -> list:
    """A4: lista de Proces dintr-un fisier JSON."""
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]


def evenimente_din_json(cale) -> list:
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    """B1: clasa container pentru o lista de procese."""
    procese: list

    @classmethod
    def din_json(cls, cale):
        return cls(procese_din_json(cale))

    def __len__(self):
        return len(self.procese)

    def suspecte(self) -> list:
        """B2: procesele suspecte (din self.procese, nu dintr-o variabila globala)."""
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self) -> dict:
        """B2: dict user -> lista de nume de procese."""
        rezultat = {}
        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)
        return rezultat


def main():
    """B3: raportul (text sau JSON) din obiecte."""
    p = argparse.ArgumentParser(description="Inventar procese + evenimente Windows")
    p.add_argument("capturi", help="folderul cu procese.json si evenimente.json")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    inv = Inventar.din_json(os.path.join(a.capturi, "procese.json"))
    ev = evenimente_din_json(os.path.join(a.capturi, "evenimente.json"))

    suspecte = inv.suspecte()
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        rezultat = {
            "procese": [asdict(x) for x in suspecte],
            "evenimente": [asdict(e) for e in alarma],
        }
        print(json.dumps(rezultat, indent=4, ensure_ascii=False))
        return

    print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
    for x in suspecte:
        print(f"   [{x.pid}] {x.nume} ({x.user}) {x.cale}")

    print(f"\nEvenimente: {len(ev)} | alarma: {len(alarma)}")
    for e in alarma:
        print(f"   {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()
