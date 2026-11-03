
#ex A1
import argparse, json, os


def citeste_linii(cale) -> list:
    with open(cale, encoding="utf-8") as f:
        liste = []
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                liste.append(line)
        return liste
 
cai = citeste_linii("/home/vlad/Desktop/Univer/tehniciprogramare/lab8/start/suid.txt")
print("linii SUID:", len(cai))


#Ex A2
def nume(cale)->list:
    return cale.rsplit('/',1)[-1]
    #print(cale.rsplit('/',1)[-1])
 
nume_unice = {nume(c) for c in cai}    # set comprehension
print("SUID distincte:", len(nume_unice))


#ex3
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale)->list[dict[str,any]]:
    cai = citeste_linii(cale)

    result = []
    for path in sorted(set(cai)):
        dictionar = {
            "cale": path,
            "nume":nume(path),
            "risc": "mare" if nume(path) in GTFO else "normal"
        }
        result.append(dictionar)
        print(nume(path))
    return result
    
 
suid = suid_constatari("/home/vlad/Desktop/Univer/tehniciprogramare/lab8/start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))

#ex4

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        # TODO: adauga {"user": user.strip(), "drept": drept.strip(),
        #   "risc": "mare" daca "NOPASSWD" in drept, altfel "normal"}
        result = {
            "user":user.strip(),
            "drept":drept.strip(),
            "risc":"mare" if "NOPASSWD" in drept else "normal"
        }
        out.append(result)
    return out
 
def cron_constatari(cale):
    # TODO: campuri = ln.split(); user = campuri[5];
    #   comanda = " ".join(campuri[6:]); dict cu user si comanda
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        result = {
            "user":campuri[5],
            "comanda": " ".join(campuri[6:])
        }
        out.append(result)
    return out
        
def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }
rezultate = enumereaza("/home/vlad/Desktop/Univer/tehniciprogramare/lab8/start")
print("\n=== SUID ===")
for item in rezultate["suid"]:
    print(item)

print("\n=== SUDO ===")
for item in rezultate["sudo"]:
    print(item)

print("\n=== CRON ===")
for item in rezultate["cron"]:
    print(item)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")
 
if __name__ == "__main__":
    main()