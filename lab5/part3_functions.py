# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
import time
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
import requests

#ex21
def fetch(url:str,timeout = 10)->requests.Response:
    response = requests.get(url,timeout=timeout)
    return response.status_code 
#print(fetch(BASE_URL))

#ex22
def get_status(url:str)->int:
    response = requests.get(BASE_URL + url)
    return response.status_code
"""
time.sleep(1)
print(get_status("/"))
time.sleep(1)
print(get_status("/robots.txt"))
time.sleep(1)
print(get_status("/sitemap.xml"))
"""

#ex23
"""
print(fetch(BASE_URL))
print(fetch(BASE_URL,3))
"""

#ex24
def get_title(html:str):
    """Get the title from a page by getting text content from <title> tags."""
    findtext = html.find("<title>")
    endtext = html.find("</title>")
    title = html[findtext + len("<title>"):endtext]
    cleantitle = title.strip()
    print(cleantitle)
"""
response = requests.get(BASE_URL)
html_text = response.text
get_title(html_text)
"""

#ex27
def page_exists(url:str)->bool:
    try:
        response = requests.get(url)
        if response:
            return True
    except requests.RequestException:
        return False
"""
print(page_exists(BASE_URL))
print(page_exists("https://this-domain-does-not-exist.invalid"))
"""

#ex28
def check_paths(base,paths:list)->list:
    result = []
    for i in range(len(paths)):
        response = requests.get(base + paths[i])
        result.append({
            "path":base + paths[i],
            "status_code":response.status_code
        })
    return result
"""
list =["/", "/robots.txt", "/sitemap.xml"]
result = check_paths(BASE_URL,list)
print(result)
"""

#ex29
def get_header(url:str, name:str, default="lipseste")->requests.head:
    response = requests.get(url)
    if response.headers.get("name",name):
        return response.headers

#print(get_header(BASE_URL,"Server"))


#ex 30
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

#print(security_headers(BASE_URL))
#ex 31
def score_headers(results:list)->str:
    count = 0
    for result in results:
        if result['valoare'] == True:
            count += 1
    return f"{count}/5"
#print(score_headers(security_headers(BASE_URL)))

#ex 32
def fetch_robots(base:str)->str:
    robots = "/robots.txt"
    response = requests.get(base + robots)
    if response.text:
        return  response.text
    else:
        return "None"

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

"""
print(fetch_robots(BASE_URL))
print(dissalowed_paths(fetch_robots(BASE_URL)))
"""
#ex 33
def response_times(*urls:str)->list:

    result = []
    for url in urls:
        response = requests.get(BASE_URL + url)
        result.append({
            "url":url,
            "secunde":response.elapsed.seconds
        })
    return result

#print(response_times("/","/robots.txt"))

#ex 34

def log(message:str,**details)->str:
    final_string = f"{message}"
    for key,value in details.items():
        final_string += f" {key} : {value}"
    return final_string
#print(log("verificat", url=BASE_URL, status=200))