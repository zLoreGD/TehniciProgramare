# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
from __future__ import annotations

import time
from urllib.parse import urljoin
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10
SECURITY_HEADERS = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
)


def fetch(url: str, timeout: float = TIMEOUT) -> requests.Response:
    """Trimite o cerere GET și returnează obiectul Response."""
    return requests.get(url, timeout=timeout)


def get_status(path: str) -> int:
    """Returnează codul HTTP pentru o cale relativă la BASE_URL."""
    response = requests.get(urljoin(BASE_URL + "/", path.lstrip("/")), timeout=TIMEOUT)
    return response.status_code


def get_title(html: str) -> str | None:
    """Extrage și returnează titlul HTML; întoarce None dacă lipsește."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(" ", strip=True) if soup.title else None


def page_exists(url: str) -> bool:
    """Returnează True dacă serverul răspunde cu un cod de stare sub 400."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.status_code < 400
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Verifică o listă de căi și returnează o mapare cale–cod HTTP."""
    result = {}
    for path in paths:
        full_url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        try:
            response = requests.get(full_url, timeout=TIMEOUT)
            result[path] = response.status_code
        except requests.RequestException:
            result[path] = 0
        time.sleep(1)
    return result


def get_header(url: str, name: str, default: str | None = None) -> str | None:
    """Returnează valoarea unui antet HTTP sau valoarea default."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.headers.get(name, default)


def security_headers(url: str) -> dict[str, bool]:
    """Verifică prezența antetelor HTTP de securitate."""
    response = requests.get(url, timeout=TIMEOUT)
    return {name: bool(response.headers.get(name)) for name in SECURITY_HEADERS}


def score_headers(results: dict[str, bool]) -> str:
    """Returnează scorul antetelor de securitate în formatul X/5."""
    count = sum(bool(value) for value in results.values())
    return f"{count}/{len(SECURITY_HEADERS)}"


def fetch_robots(base: str) -> str | None:
    """Descarcă robots.txt; returnează None dacă nu există sau cererea eșuează."""
    url = urljoin(base.rstrip("/") + "/", "robots.txt")
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 404 or not response.text.strip():
            return None
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage doar valorile directivelor Disallow: din robots.txt."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        directive, value = line.split(":", 1)
        if directive.strip().lower() == "disallow":
            paths.append(value.strip())
    return paths


def response_times(*urls: str) -> list[dict[str, float | str]]:
    """Măsoară durata cererilor pentru URL-urile primite."""
    result = []
    for url in urls:
        full_url = urljoin(BASE_URL.rstrip("/") + "/", url.lstrip("/"))
        start = time.perf_counter()
        try:
            response = requests.get(full_url, timeout=TIMEOUT)
            response.raise_for_status()
            elapsed = time.perf_counter() - start
            result.append({"url": full_url, "secunde": round(elapsed, 6)})
        except requests.RequestException:
            elapsed = time.perf_counter() - start
            result.append({"url": full_url, "secunde": round(elapsed, 6)})
        time.sleep(1)
    return result


def log(message: str, **details: object) -> str:
    """Construiește un mesaj de jurnal cu detalii opționale."""
    extra = " ".join(f"{key}={value}" for key, value in details.items())
    return f"{message} {extra}".strip()


if __name__ == "__main__":
    print("fetch:", fetch(BASE_URL).status_code)
    print("get_status('/'): ", get_status("/"))
    print("get_status(123):")
    try:
        get_status(123)  # test negativ cerut în enunț
    except (AttributeError, TypeError) as exc:
        print("Argument invalid detectat:", type(exc).__name__)
    print("Titlu:", get_title(fetch(BASE_URL).text))
    print("Antete:", security_headers(BASE_URL))
    print("Scor:", score_headers(security_headers(BASE_URL)))
    print("Disallow:", disallowed_paths(fetch_robots(BASE_URL)))
    print("Timpi:", response_times("/", "/robots.txt"))
    print(log("verificat", url=BASE_URL, status=200))
