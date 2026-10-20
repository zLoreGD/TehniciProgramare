# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"

DEFAULT_HEADERS = {"User-Agent": "WebLab-Gorceag Vlad"}
TIMEOUT = 10  # secunde
import requests
import socket
from datetime import datetime
import ssl
import urllib
import json

def fetch(url:str,timeout = 10)->requests.Session:

    #response = requests.get(url,timeout=timeout)
    #return response.status_code
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    session.get(url,"/headers",timeout=timeout)
    return session.headers   
  
def fetch_robots(base:str)->str:
    robots = "/robots.txt"
    response = requests.get(base + robots)
    if response.text:
        return  response.text
    else:
        return "None"
def score_headers(results:list)->str:
    count = 0
    for result in results:
        if result['valoare'] == True:
            count += 1
    return f"{count}/5"

def get_status(url:str)->int:
    response = requests.get(BASE_URL + url)
    return response.status_code
def get_title(html:str):
    """Get the title from a page by getting text content from <title> tags."""
    findtext = html.find("<title>")
    endtext = html.find("</title>")
    title = html[findtext + len("<title>"):endtext]
    cleantitle = title.strip()
    print(cleantitle)
def security_headers(url:str)->list:
    headers_list = ["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options","X-Content-Type-Options","Referrer-Policy"]
    response = requests.get(url)
    result = []

    for i in range(len(headers_list)):
        if response.headers.get(headers_list[i]):
            result.append({
                "antet":headers_list[i],
                "valoare":True
                
            })
        else:
            result.append({
                "antet":headers_list[i],
                "valoare":False                
            })
    return result
def check_paths(base,paths:list)->list:
    result = []
    for i in range(len(paths)):
        response = requests.get(base + paths[i])
        result.append({
            "path":base + paths[i],
            "status_code":response.status_code,
            "checked_at":datetime.now().isoformat()
        })
    return result
def cert_days_left(hostname:str)->int:
    context = ssl.create_default_context()
    sock = socket.create_connection((hostname,443))
    ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
    value = ssl_sock.getpeercert()["notAfter"]
    return ssl.cert_time_to_seconds(value)
def resolve(hostname:str)->str:
    return socket.gethostbyname(hostname)


def dissalowed_paths(robots_text:str)->list:
    
    dissalowed = []
    if robots_text == "None":
        return [""]
    dissalow = robots_text.find("Disallow:")
    if dissalow != -1:
        for line in robots_text.splitlines():
            path = line[len("Disallow:"):].strip()
            dissalowed.append(path)
    return dissalowed




def split_links(links,domain)->tuple[list,list]:
    internal = []
    external = []
    for link in links:
        full_url = urllib.parse.urljoin(BASE_URL,link)
        link_domain = urllib.parse.urlparse(full_url).netloc

        if link_domain == domain:
            internal.append(link)
        else:
            external.append(link)
    return internal,external

    
def site_report(url:str):
    response = requests.get(BASE_URL + url)
    list_example = [
        "/about",
        "/contact",
        "https://google.com",
        "https://github.com/test"
    ]
    full_url = urllib.parse.urljoin(BASE_URL,url)
    link_domain = urllib.parse.urlparse(full_url).netloc
    links = split_links(list_example,link_domain)

    result = {
        "url":BASE_URL + url,
        "cod_stare":get_status(url),
        "titlu":get_title(BASE_URL+ url),
        "ip":resolve(link_domain),
        "lant":list(response.history),
        "scor":score_headers(security_headers(BASE_URL + url)),
        "days_left":cert_days_left(link_domain)/86400,
        "internal_count":len(links[0]),
        "external_count":len(links[1]),
        "disallowed":dissalowed_paths(fetch_robots(BASE_URL))
    }
    with open("report.json","w") as file:
        json.dump(dict(result),file,indent=2)

if __name__ == "__main__":
    print("Autotest:", get_status("/"))
    