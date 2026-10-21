# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
from __future__ import annotations

import hashlib
import json
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Gorceag Vlad"}
SECURITY_HEADER_NAMES = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
)


def fetch(url: str, timeout: float = TIMEOUT) -> requests.Response:
    """Trimite o cerere GET și întoarce obiectul Response."""
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)


def get_status(path: str) -> int:
    """Returnează codul HTTP pentru o cale relativă la site-ul de bază."""
    if not isinstance(path, str):
        raise TypeError("path trebuie să fie un șir de caractere")
    url = urljoin(BASE_URL.rstrip("/") + "/", path.lstrip("/"))
    return fetch(url).status_code


def get_title(html: str) -> str | None:
    """Extrage titlul din HTML și îl returnează; None dacă lipsește."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(" ", strip=True) if soup.title else None


def page_exists(url: str) -> bool:
    """Indică dacă URL-ul răspunde cu un cod HTTP sub 400."""
    try:
        return fetch(url).status_code < 400
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list[str]) -> dict[str, dict[str, object]]:
    """Verifică fiecare cale și returnează datele într-un dicționar."""
    results: dict[str, dict[str, object]] = {}
    for path in paths:
        url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        try:
            response = fetch(url)
            results[path] = {
                "url": url,
                "status_code": response.status_code,
                "checked_at": datetime.now().isoformat(timespec="seconds"),
            }
        except requests.RequestException as exc:
            results[path] = {
                "url": url,
                "status_code": None,
                "error": str(exc),
                "checked_at": datetime.now().isoformat(timespec="seconds"),
            }
        time.sleep(1)
    return results


def get_header(url: str, name: str, default: str | None = None) -> str | None:
    """Returnează valoarea antetului cerut."""
    response = fetch(url)
    response.raise_for_status()
    return response.headers.get(name, default)


def security_headers(url: str) -> dict[str, bool]:
    """Returnează un dicționar cu prezența antetelor de securitate."""
    response = fetch(url)
    return {name: bool(response.headers.get(name)) for name in SECURITY_HEADER_NAMES}


def score_headers(results: dict[str, bool]) -> str:
    """Calculează scorul antetelor prezente, de forma X/5."""
    return f"{sum(bool(v) for v in results.values())}/{len(SECURITY_HEADER_NAMES)}"


def fetch_robots(base: str) -> str | None:
    """Descarcă robots.txt; None dacă nu există conținut disponibil."""
    url = urljoin(base.rstrip("/") + "/", "robots.txt")
    try:
        response = fetch(url)
        if response.status_code == 404 or not response.text.strip():
            return None
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage numai valorile directivelor Disallow:."""
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


def response_times(*urls: str) -> list[dict[str, float | str | None]]:
    """Măsoară durata fiecărei cereri cu perf_counter."""
    results = []
    for item in urls:
        url = urljoin(BASE_URL.rstrip("/") + "/", item.lstrip("/"))
        start = time.perf_counter()
        try:
            response = fetch(url)
            status = response.status_code
        except requests.RequestException:
            status = None
        results.append({
            "url": url,
            "status_code": status,
            "seconds": round(time.perf_counter() - start, 6),
        })
        time.sleep(1)
    return results


def log(message: str, **details: object) -> str:
    """Formatează un mesaj de jurnal cu detalii opționale."""
    suffix = " ".join(f"{key}={value}" for key, value in details.items())
    return f"{message} {suffix}".strip()


def extract_links(html: str) -> list[str]:
    """Extrage linkurile href unice din elementele a."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(
        item["href"].strip() for item in soup.find_all("a", href=True)
        if item["href"].strip()
    ))


def split_links(links: list[str], domain: str, base_url: str = BASE_URL) -> tuple[list[str], list[str]]:
    """Împarte linkurile în interne și externe folosind hostname-ul."""
    expected_host = urlparse(domain if "://" in domain else "https://" + domain).hostname
    internal, external = [], []
    for link in links:
        full_url = urljoin(base_url, link)
        host = urlparse(full_url).hostname
        (internal if host == expected_host else external).append(link)
    return internal, external


class ImageFinder(HTMLParser):
    """Colectează căile src din etichetele img."""

    def __init__(self):
        super().__init__()
        self.images: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


def page_fingerprint(url: str) -> str:
    """Calculează amprenta SHA-256 a conținutului paginii."""
    response = fetch(url)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


def save_headers(url: str, filename: str = "headers.json") -> dict[str, str]:
    """Salvează antetele HTTP în fișier JSON."""
    response = fetch(url)
    response.raise_for_status()
    headers = dict(response.headers)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(headers, file, indent=2, ensure_ascii=False)
    return headers


def resolve(hostname: str) -> str:
    """Rezolvă hostname-ul la o adresă IPv4."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Calculează zilele întregi rămase până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
            cert = ssl_sock.getpeercert()
    expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    return max(0, (expiry - datetime.now(timezone.utc)).days)


def site_report(url: str = BASE_URL, filename: str = "report.json") -> dict[str, object]:
    """Generează și salvează un raport bazat pe pagina reală."""
    # Acceptă atât un URL complet, cât și o cale relativă.
    target_url = urljoin(BASE_URL.rstrip("/") + "/", url.lstrip("/")) if "://" not in url else url
    response = fetch(target_url)
    response.raise_for_status()
    final_url = response.url
    parsed = urlparse(final_url)
    hostname = parsed.hostname or ""

    links = extract_links(response.text)
    internal, external = split_links(links, hostname, final_url)
    robots = fetch_robots(f"{parsed.scheme}://{parsed.netloc}")

    report = {
        "url": target_url,
        "final_url": final_url,
        "cod_stare": response.status_code,
        "titlu": get_title(response.text),
        "ip": resolve(hostname) if hostname else None,
        "lant": [
            {"url": item.url, "cod_stare": item.status_code}
            for item in response.history
        ],
        "antete_securitate": security_headers(final_url),
        "scor": score_headers(security_headers(final_url)),
        "days_left": cert_days_left(hostname) if hostname else None,
        "internal_count": len(internal),
        "external_count": len(external),
        "disallowed": disallowed_paths(robots),
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    return report
