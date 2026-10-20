# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
import webtools
import argparse
import json
#webtools.get_title(webtools.fetch(BASE_URL).text)

#ex45
from webtools import get_title, security_headers
from webtools import DEFAULT_HEADERS
# Daca main.py de asemenea defineste get_Title(), functia locala va avea prioritate asupra get_title() care a fost importat
"""
print(DEFAULT_HEADERS)
print(webtools.fetch(BASE_URL))
"""

"""
#ex48
parser = argparse.ArgumentParser()
parser.add_argument("url",type=str)

args = parser.parse_args()

print(webtools.security_headers(args.url))
#print(args.url)
"""


#ex49
import csv
list =["/", "/robots.txt", "/sitemap.xml"]
print(webtools.check_paths(BASE_URL,list))

result = webtools.check_paths(BASE_URL,list)
fieldnames = result[0].keys()
with open("report.csv","w") as file:
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(result)

webtools.site_report("/")
