# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
import requests

import urllib
import re
"""
#ex 35
result = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")

print(result.scheme)
print(result.netloc)
print(result.path)
print(result.query)
print(result.fragment)
"""

"""
#ex36
print(urllib.parse.urljoin(BASE_URL,"/about"))
print(urllib.parse.urljoin(BASE_URL,"contact.html"))
print(urllib.parse.urljoin(BASE_URL,"../index.html"))
"""



#ex37
def extract_links(html):
    result = re.findall(r'href="([^"]+)"', html)
    return result
#print(extract_links(requests.get(BASE_URL).text))

#ex38
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



"""
links = [
    "/about",
    "/contact",
    "https://google.com",
    "https://github.com/test"
]

print(split_links(links, "example.com"))
"""
"""
#ex39

from html.parser import HTMLParser
 
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
 
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            value = dict(attrs).get("src")
            if value:
                self.images.append(value)

imagefinder = ImageFinder()
#html = requests.get(BASE_URL).content
html = '''
<html>
    <img src="cat.jpg">
    <img src="/images/dog.png">
    <img src="bird.jpg">
</html>
'''
imagefinder.feed(html)
print(imagefinder.images)
"""

#ex40
import hashlib
"""
def page_fingerprint(url:str)-> hashlib.sha256:
    response = requests.get(BASE_URL,url)
    return hashlib.sha256(response.content).hexdigest()

print(page_fingerprint('about'))
"""
import json
#ex41
"""
response = requests.get(BASE_URL)
#scriere
with(open("headers.json","w")) as f: 
    json.dump(dict(response.headers),f,indent=2)
with(open("headers.json","r")) as f:
    print(json.load(f))
"""


#ex42
import socket
import ssl
import datetime
def resolve(hostname:str)->str:
    return socket.gethostbyname(hostname)
#print(resolve("cybercor.org"))

#ex43
def cert_days_left(hostname:str)->int:
    context = ssl.create_default_context()
    sock = socket.create_connection((hostname,443))
    ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
    value = ssl_sock.getpeercert()["notAfter"]
    return ssl.cert_time_to_seconds(value)
print(cert_days_left("cybercor.org"))