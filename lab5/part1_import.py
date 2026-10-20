# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
import requests as requests
"""
#ex 1
print("requests:", requests.__version__)
print("requests with urllib: ",requests_url.__version__)
"""

"""
#ex2
from requests import get
#metoda 1
code = requests.get(BASE_URL)
print("Codul de stare: ", code)
#metoda 2
code1 = get(BASE_URL)
print("Codul de stare (METODA 2): ", code1)
"""

"""
#ex 3
import requests as rq
website = rq.get(BASE_URL)
print(website)
"""


"""
#ex 4
import urllib.request as requests
with requests.urlopen(ECHO_URL) as response:
    status = response.status
    html_bytes = response.read()
    html_text = html_bytes.decode("utf-8")
print(status)
print(html_text[:200])
"""

#ex 5
#print(dir(requests))


"""
#ex 6
response = requests.get(BASE_URL,timeout=TIMEOUT)
print(response)
"""
"""
#ex 7
import time
start = time.perf_counter()
response = requests.get(BASE_URL)
end = time.perf_counter()
time_elapsed = end - start
print("Timpul necesar ca requestul sa dea raspuns", time_elapsed)
print("response elapsed:", response.elapsed)
"""

"""
#ex8
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
"""
