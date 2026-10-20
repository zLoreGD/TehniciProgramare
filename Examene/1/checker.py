import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    #"https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path)->str:
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    newhost = host.replace("/","")
    newpath = path.replace("/","")
    return f"https://{newhost}/{newpath}"


def is_https(url) -> bool:
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""

    response = requests.get(url)
    
    print("Status: ",response.status_code)
    print("Content-type:",response.headers['Content-Type'])



def check_site(url)->dict:
    """Returnează un dicționar cu: status, content_type, length, server."""
    response = requests.get(url,timeout=5)
    server = response.headers['Server']
    if server:
        server = response.headers['Server']
    else:
        server = "unknown"
    try:
        result = {
            "status":response.status_code,
            "content_type":response.headers['Content-Type'],
            "length":len(response.content),
            "server":server
        }
        return result
    except TimeoutError as e:
        return {
            "status":"None",
            "error":e
        }


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    
    functional_sites = []
    non_functional = []
    try:
        for sites in SITES:
            if requests.get(sites).status_code == 200:
                functional_sites.append(sites)
            else:
                non_functional.append(sites)
    except requests.exceptions.ConnectionError as e:
        print(e)

    print(f"Siteurile care au returnat codul 200: \n")
    for s in functional_sites:
        print(f"{s} -> 200 \n {len(requests.get(s).content)} octeti")
    #sorted = functional_sites.sort(key=len(requests.get(functional_sites).content))
    #print("Lista sortata: ")
    #for sort in sorted:
    #    print(f"{sort}\n")
    print(f"{len(functional_sites)} Site-uri au mers")
    print(f"{len(non_functional)} Site-uri nu au mers")
    
        




def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    response = requests.get(url, timeout=5)
    headers = response.headers

    present = []
    missing = []

    for sec_header in SECURITY_HEADERS:
        if sec_header in headers:
            present.append(sec_header)
        else:
            missing.append(sec_header)

    score = len(present) * 25

    return {
        "present": present,
        "missing": missing,
        "score": score
    }


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    attempts_used = 0

    for _ in range(attempts):
        attempts_used += 1

        try:
            response = requests.get(url, timeout=5)

            return {
                "status": response.status_code,
                "attempts": attempts_used
            }

        except requests.RequestException:
            continue

    return {
        "status": None,
        "attempts": attempts_used
    }