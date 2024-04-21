from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from zenrows import ZenRowsClient
import csv
import pandas


class Oglas:
    def __init__(self, ime_znamke, ime_modela, letnik_prve_registracije, prevozeni_kilometri, absolute_link_name, link_slike, cena, gorivo):
        self.ime_znamke = ime_znamke
        self.ime_modela = ime_modela
        self.letnik_prve_registracije = letnik_prve_registracije
        self.prevozeni_kilometri = prevozeni_kilometri
        self.absolute_link_name = absolute_link_name
        self.link_slike = link_slike
        self.cena = cena
        self.gorivo = gorivo
        
    def to_dict(self):
        dict = {'ad_link': self.absolute_link_name,
                'image_link': self.link_slike,
                'first_registry' : self.letnik_prve_registracije,
                'brand' : self.ime_znamke,
                'model' : self.ime_modela,
                'gas_type' : self.gorivo,
                'kilometers' : self.prevozeni_kilometri,
                'price' : self.cena}
        return dict
    
class Znamka:
    def __init__(self, ime):
        self.ime = ime
        self.modeli = []

class ModelGetter:
    def __init__(self):
        self.url = 'https://www.avto.net/'
    def extract_models(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        dropdownbox = driver.find_elements(By.TAG_NAME, value="Option")
        
        znamke = []
        with open("znamke2.txt", "r", encoding='utf-8') as file:
            for line in file.readlines():
                ime_znamke = line.strip()
                znamka = Znamka(ime_znamke)
                znamke.append(znamka)
                
                
                #go through dropbox option and find the right one
                i = 0
                print(ime_znamke)
                while i < len(dropdownbox):
                    if dropdownbox[i].text == ime_znamke:
                        dropdownbox[i].click()
                        try:
                            elements = driver.find_elements(By.CLASS_NAME, ime_znamke)
                        except:
                            print(ime_znamke, "!!!!!!!")
                        for element in elements:
                            try:
                                znamka.modeli.append(element.text.strip())
                            except:
                                print(ime_znamke, "!!!")

                        break
                    i += 1
        
        data = []
        for znamka in znamke:
            if len(znamka.modeli) == 0:
                data.append([znamka.ime, "prazno"])
            for model in znamka.modeli:
                data.append([znamka.ime, model])
                
        csv_file = 'znamke_modeli.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            
class AdScrapper:
    def __init__(self):
        self.baseurl = "https://www.avto.net/Ads/results_100.asp?oglasrubrika=1&prodajalec=2"
        self.znamke2modeli = {}
        
        csv_file = "znamke_modeli.csv"
        data = pd.read_csv(csv_file, header=None)
        for line in data.values:
            if line[0].lower() not in self.znamke2modeli:
                self.znamke2modeli[line[0].lower()] = [line[1].lower()]
            else:
                self.znamke2modeli[line[0].lower()].append(line[1].lower())
        
        
        
        
    def search_ads(self):
        
        client = ZenRowsClient("e84d7a689864106b340f78ba7c14eceb0a1dc706")
        response = client.get(self.baseurl)
        soup = BeautifulSoup(response.content, 'lxml')
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        class_name = "row bg-white position-relative GO-Results-Row GO-Shadow-B"
        oglasi_tags = soup.find_all('div', class_ = class_name)

        
        oglasi = []
        for oglas_tag in oglasi_tags:
            link = oglas_tag.findChild(attrs={'class': 'stretched-link'})
            relative_link_name = link.get('href')
            absolute_link_name = "https://avto.net" + relative_link_name[2:]
            
            naslov_oglasa = oglas_tag.findChild(attrs={'class': 'GO-Results-Naziv bg-dark px-3 py-2 font-weight-bold text-truncate text-white text-decoration-none'}).text.strip()
            naslov_oglasa = naslov_oglasa.split(" ")
            ime_znamke = naslov_oglasa[0].lower()
            ime_modela = naslov_oglasa[1].lower()
            i = 2
            
            if ime_znamke not in self.znamke2modeli:
                print("znamka ni v bazi")
            else:
                while ime_modela not in self.znamke2modeli[ime_znamke] and i < len(naslov_oglasa):
                    ime_modela += " " + naslov_oglasa[i].lower()
                    i +=1
                
            
            podatki = oglas_tag.findChildren(attrs={'class': 'd-none d-md-block pl-3'})
            prevozeni_kilometri = "0 km"
            gorivo = ""
            for podatek in podatki:
                if podatek.text == 'Prevoženih':
                    prevozeni_kilometri = podatek.findNext().text
                if podatek.text == 'Gorivo':
                    gorivo = podatek.findNext().text
                
            prevozeni_kilometri = prevozeni_kilometri.rstrip("km")
   
            letnik_prve_registracije = oglas_tag.findChild(attrs={'w-25 d-none d-md-block pl-3'}).findNext().text.strip()

            try:
                cena = int(''.join(oglas_tag.findChild(attrs={'class': 'GO-Results-Price-TXT-Regular'}).text.strip(" €").split(".")))
            except:
                #akcijska cena je drugače zapisana
                cena = int(''.join(oglas_tag.findChild(attrs={'class': 'GO-Results-Price-TXT-AkcijaCena'}).text.strip(" €").split(".")))
            
            slika_div = oglas_tag.findChild(attrs={'class': 'col-auto p-3 GO-Results-Photo'})
            slika = slika_div.findChild().findChild().findChild().get('src')
            
            
            print("znamka:", ime_znamke)
            print("model:", ime_modela)
            print("prevozeni kilometri", int(prevozeni_kilometri))
            print("cena", cena)
            print("registracija", letnik_prve_registracije)
            print("gorivo", gorivo)
            print("link", absolute_link_name)
            print("slika", slika)
            print("\n")

            
            oglas = Oglas(ime_znamke, ime_modela, letnik_prve_registracije, prevozeni_kilometri, absolute_link_name, slika, cena, gorivo)
            oglasi.append(oglas)
        
        return oglasi
        
        

if __name__ == '__main__':
    """needed just the first time, to get pairs of brands and models from the website"""
    #model_getter = ModelGetter()
    #model_getter.extract_models()
    
    ad_scrapper = AdScrapper()
    while True:
        oglasi = ad_scrapper.search_ads()
         
        data_dicts = []
        for oglas in oglasi:
            data_dict = oglas.to_dict()
            data_dicts.append(data_dict)
        
        
        #tldr: dictionary za vsak oglas od 100 najnovejših, v vsakem je tisto, kar si napisal
        print(data_dicts[0])
        time.sleep(60*10)
    
  
