# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
import hashlib
import json
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


def ex35(url: str = "https://cybercor.org/path?x=1#top") -> dict[str, str]:
    """Desparte un URL în componentele sale."""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
    }


def ex36(base: str = BASE_URL) -> list[str]:
    """Demonstrează construirea URL-urilor relative."""
    return [urljoin(base, "/about"), urljoin(base, "contact.html"),
            urljoin(base, "../index.html")]


def extract_links(html: str) -> list[str]:
    """Extrage linkurile href fără duplicate, păstrând ordinea."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(
        tag["href"].strip() for tag in soup.find_all("a", href=True)
        if tag["href"].strip()
    ))


def split_links(links: list[str], domain: str, base_url: str = BASE_URL) -> tuple[list[str], list[str]]:
    """Împarte linkurile în interne și externe după numele gazdei."""
    expected_host = urlparse(domain if "://" in domain else "https://" + domain).hostname
    internal, external = [], []
    for link in links:
        full_url = urljoin(base_url, link)
        host = urlparse(full_url).hostname
        (internal if host == expected_host else external).append(link)
    return internal, external


class ImageFinder(HTMLParser):
    """HTML parser care colectează valorile src ale elementelor img."""

    def __init__(self):
        super().__init__()
        self.images: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 a conținutului unei pagini."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


def save_headers(url: str, filename: str = "headers.json") -> dict[str, str]:
    """Salvează antetele paginii în JSON și returnează dicționarul."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    headers = dict(response.headers)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(headers, file, indent=2, ensure_ascii=False)
    return headers


def resolve(hostname: str) -> str:
    """Rezolvă numele de gazdă la o adresă IPv4."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează numărul aproximativ de zile până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
            cert = ssl_sock.getpeercert()
    expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    remaining = expiry - datetime.now(timezone.utc)
    return max(0, remaining.days)


if __name__ == "__main__":
    print("URL:", ex35())
    print("URL-uri:", ex36())
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    links = extract_links(response.text)
    internal, external = split_links(links, urlparse(response.url).hostname or "")
    print("Linkuri unice:", links)
    print("Interne/externe:", len(internal), len(external))

    parser = ImageFinder()
    parser.feed(response.text)
    assert isinstance(parser.images, list)
    print("Imagini:", parser.images)

    print("Amprentă:", page_fingerprint(BASE_URL))
    save_headers(BASE_URL)
    print("IP:", resolve("cybercor.org"))
    print("Zile până la expirare:", cert_days_left("cybercor.org"))
