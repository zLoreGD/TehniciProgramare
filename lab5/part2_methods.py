# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def ex9():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("status_code:", response.status_code)
    print("ok:", response.ok)
    print("url:", response.url)
    print("encoding:", response.encoding)


def ex10():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    try:
        bad_response = requests.get(
            BASE_URL + "/this-page-does-not-exist",
            timeout=TIMEOUT,
        )
        bad_response.raise_for_status()
        print("Cererea a reușit.")
    except requests.HTTPError:
        print("Pagina nu a fost găsită sau serverul a returnat o eroare HTTP.")


def ex11():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    for key, value in response.headers.items():
        print(f"{key}: {value}")


def ex12():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.headers.get("Server", "lipsește"))
    print(response.headers.get("Content-Type", "lipsește"))
    # Numele antetelor HTTP nu depind de majuscule/minuscule.
    print(response.headers.get("content-type", "lipsește"))


def ex13():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    print("Cuvântul 'cyber' apare de", response.text.lower().count("cyber"), "ori.")


def ex14():
    from bs4 import BeautifulSoup
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.title.get_text(strip=True) if soup.title else "Titlul lipsește.")


def ex15():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    lines = response.text.splitlines()
    print("Număr de linii:", len(lines))
    print("Lungimea celei mai lungi linii:", max((len(line) for line in lines), default=0))


def ex16():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Conexiune securizată" if response.url.startswith("https://")
          else "Conexiune nesecurizată")


def ex17():
    response = requests.get("http://cybercor.org", timeout=TIMEOUT, allow_redirects=True)
    if response.history:
        print("Redirecționări:")
        for item in response.history:
            print(f"{item.status_code} | {item.url}")
    else:
        print("Nu au fost detectate redirecționări.")
    print(f"URL final: {response.url} | cod: {response.status_code}")


def ex18():
    get_response = requests.get(BASE_URL, timeout=TIMEOUT)
    head_response = requests.head(BASE_URL, timeout=TIMEOUT, allow_redirects=True)
    print("Lungime GET:", len(get_response.content))
    print("Lungime HEAD:", len(head_response.content),
          "(de regulă, HEAD nu returnează corpul paginii)")


def ex19():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    if response.cookies:
        for cookie in response.cookies:
            print(f"Cookie: {cookie.name} | secure={cookie.secure}")
    else:
        print("Nu a fost setat niciun cookie.")


def ex20():
    with requests.Session() as session:
        session.headers.update({"User-Agent": "WebLab-Gorceag Vlad"})
        response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
        response.raise_for_status()
        print("Antetele sesiunii:", session.headers)
        print("Antetele observate de server:", response.json())


if __name__ == "__main__":
    for exercise in (ex9, ex10, ex11, ex12, ex13, ex14, ex15, ex16, ex17, ex18, ex19, ex20):
        try:
            exercise()
        except (requests.RequestException, ValueError) as exc:
            print(f"Eroare în {exercise.__name__}: {exc}")
        time.sleep(1)
