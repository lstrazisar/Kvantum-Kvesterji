from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import requests
import time

baseurl = "https://www.avto.net/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'}

r = requests.get(baseurl, headers=HEADERS)
soup = BeautifulSoup(r.content, 'lxml')

select_znamke = soup.find_all('select', attrs={'name': 'znamka'})
znamke = select_znamke
#print(select_znamke)
#print(type(select_znamke))


imena = []
for line in znamke[0]:
    #print(type(line))
    #print(line)
    
    ime = line.string
    if ime != '\n':
        imena.append(ime)
        print(ime)
    

