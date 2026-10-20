# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
import requests

"""
#ex 9
response = requests.get(BASE_URL)
print(response.status_code) #atribut
print(response.ok) #atribut
print(response.url) #atribut
print(response.encoding) #atribut
"""

"""
#ex 10
response = requests.get(BASE_URL)
response.raise_for_status()

try:
    response1 = requests.get(BASE_URL + "/this-page-does-not-exist")
    response1.raise_for_status()
    print("lucreaza")
except requests.HTTPError:
    print("un mesaj prietenos")
"""

"""
#ex11
response = requests.get(BASE_URL)
for key,value in response.headers.items():
    print(f"{key}:{value}")
"""

"""
#ex12
response = requests.get(BASE_URL)
server = response.headers.get("Server","lipsește")
content = response.headers.get("Content-Type","lipsește")
content2 = response.headers.get("content-type")
print(server)
print(content)
print(content2)
"""

"""
#ex13
response = requests.get(BASE_URL)
print("Cyber este intalnit de: ", response.text.lower().count("cyber"), " ori.")
"""


"""
#ex14
response = requests.get(BASE_URL)
findtext = response.text.find("<title>")
endtext = response.text.find("</title>")

title = response.text[findtext + len("<title>"):endtext]

cleantitle = title.strip()
print(cleantitle)
"""



"""
#ex15
response = requests.get(BASE_URL)
site_lines = response.text.splitlines()
max_string = max(site_lines,key=len)
line_count = 0
for lines in site_lines:
    line_count += 1
print(line_count)
print("Lungimea celei mai lungi linii: ", len(max_string))
"""

"""
#ex16
response = requests.get(BASE_URL)
if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")
"""


"""
#ex17
non_secure = "http://cybercor.org"
response = requests.get(non_secure)
if response.history:
    print("Redirect: ")
    for raspuns in response.history:
        print(f"codul de stare {raspuns.status_code} | current url: {raspuns.url}")
else:
    print("Redirecturi nu sunt.")

print(f"Url-ul si codul final: {response.status_code} | cod: {response.url}")
"""

"""
#ex18
response1 = requests.get(BASE_URL)
response2 = requests.head(BASE_URL)
print(f"Lungimea folosind .get() {len(response1.content)}")
print(f"Lungimea folosind .head() {len(response2.content)}")
"""

"""
#ex19
response = requests.get(BASE_URL)
if response.cookies:
    for cookie in response.cookies:
        print(f"Cookie gasit: {cookie.name} | {cookie.secure}")
else:
    print("Nici un cookie setat.")
"""

"""
#ex20
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Gorceag Vlad"})
session.get(ECHO_URL,"/headers",)
print(session.headers)
"""


