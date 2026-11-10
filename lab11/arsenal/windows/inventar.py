from dataclasses import dataclass, asdict
import json
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        for c in CAI_SUSPECTE:
            if c in self.cale:
                return True
            
        return False


SUSPECTE_ID = {4625, 1102, 7045}
 
@dataclass
class Eveniment:
    id: int; nivel: str; sursa: str; cont: str; mesaj: str

    def e_suspect(self):
        # TODO: True daca self.id in SUSPECTE_ID SAU self.nivel == "critical"
        for i in SUSPECTE_ID:
            if self.id == i or self.nivel == "critical":
                return True
            
        return False
 
p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)
print(p.e_suspect())
e = Eveniment(3120,"aloha","sursa","cont","asdasda")
e1 = Eveniment(3120,"critical","sursa","cont","asdasda")
e2 = Eveniment(4625,"aloha","sursa","cont","asdasda")
print(e.e_suspect())
print(e1.e_suspect())
print(e2.e_suspect())

def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]
def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]
 
procese = procese_din_json("/home/vlad/Desktop/Univer/tehniciprogramare/lab11/start/procese.json")
print("procese:", len(procese))
print("suspecte:", sum(1 for p in procese if p.e_suspect()))

@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
    
    def suspecte(self):
        suspecte = []
        for proces in procese:
            if proces.e_suspect():
                suspecte.append(proces)
        return suspecte
    def pe_user(self):
        # TODO: dict user -> lista de nume (foloseste setdefault)
        result = {

        }
        for p in procese:
            result.setdefault(p.user,[]).append(p.nume)
        return result
inv = Inventar.din_json("/home/vlad/Desktop/Univer/tehniciprogramare/lab11/start/procese.json")
print("procese:", len(inv))
for p in inv.suspecte():
    print(f"  [{p.pid}] {p.nume}  {p.cale}")
print(inv.pe_user())

from dataclasses import asdict
import argparse
import json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")

    suspecte = [p for p in inv.procese if p.e_suspect()]
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        rezultat = {
            "procese": [asdict(p) for p in suspecte],
            "evenimente": [asdict(e) for e in alarma]
        }

        print(json.dumps(rezultat, indent=4, ensure_ascii=False))

    else:
        print(f"Procese: {len(inv.procese)} | suspecte: {len(suspecte)}")

        for p in suspecte:
            print(f"   [{p.pid}] {p.nume} ({p.user}) {p.cale}")

        print(f"\nEvenimente: {len(ev)} | alarma: {len(alarma)}")

        for e in alarma:
            print(f"   {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()