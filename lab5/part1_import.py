# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
import time
import urllib.request
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def ex1():
    # requests este o bibliotecă externă; urllib.request face parte din biblioteca standard.
    print("requests:", requests.__version__)
    print("urllib.request:", urllib.request.__name__)


def ex2():
    from requests import get
    response1 = requests.get(BASE_URL, timeout=TIMEOUT)
    response2 = get(BASE_URL, timeout=TIMEOUT)
    print("Metoda 1:", response1.status_code)
    print("Metoda 2:", response2.status_code)


def ex3():
    import requests as rq
    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)


def ex4():
    with urllib.request.urlopen(ECHO_URL, timeout=TIMEOUT) as response:
        print("Cod de stare:", response.status)
        html_text = response.read().decode("utf-8", errors="replace")
        print(html_text[:200])


def ex5():
    print("requests are", len(dir(requests)), "atribute disponibile.")
    print("Exemple:", [name for name in dir(requests) if not name.startswith("_")][:15])


def ex6():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response)


def ex7():
    start = time.perf_counter()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    elapsed = time.perf_counter() - start
    print(f"Timp total măsurat: {elapsed:.4f} secunde")
    print(f"Timpul cererii raportat de requests: {response.elapsed.total_seconds():.4f} secunde")


def ex8():
    try:
        import bs4
        print("beautifulsoup4 instalat:", bs4.__version__)
    except ImportError:
        print("Instalați modulul cu: python -m pip install beautifulsoup4")


if __name__ == "__main__":
    for exercise in (ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8):
        try:
            exercise()
        except requests.RequestException as exc:
            print(f"Eroare HTTP în {exercise.__name__}: {exc}")
        time.sleep(1)
