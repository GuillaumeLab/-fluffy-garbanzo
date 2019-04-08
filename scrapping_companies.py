import pandas as pd 
print("scrapping companies")
annonces = pd.read_csv('df_new_pymongo_no_duplicate.csv',encoding='utf-8')

def generate_delay():
    """
    retourn un chiffre aléatoire suivant une distribution normal de moyenne 4 secondes et d'ecart-type de 0.8
    Ce chiffre aléatoire est le délai après chaque clique. Le but est de simuler le comportement d'un humain :
    un délai fixe peut attirer l'attention des contrôleurs, tout comme un délai aléatoire d'une distribution uniforme
    """
    mean = 4
    sigma = 0.8
    return np.random.normal(mean,sigma,1)[0]

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
from pymongo import MongoClient
client = MongoClient('localhost') #importe local host de mongodb
db = client.new_indeed_raw # connection à la base new_indeed_raw
companyk = db.companies # connection à la table companies
import pandas as pd
import datetime
browser = webdriver.Firefox()# ouverture browser

import time
import numpy as np

import pandas as pd
import datetime


 # Ce code va permettre de scrapper des infos sur les entreprises à partir du site "entreprises.lefigaro ". On utilise Duckduckgo ... 
 #...pour rechercher le nom de l'entreprise car moins protégé que google 
# connection à la table JobPosting
for idx, i in enumerate(annonces["Company"].loc[annonces["Company"].notnull()].unique()):  # pour toute les entreprises des jobposts scrappés ...
    if companyk.find_one({'company':"'"+i+"'"})==None:#qui ne sont pas dans la base de donnée....
        company_name = "'"+i+"'"#variable company entre guillemet pour éviter que duckduckgo nous renvoi des entreprises différentes
        try:
            browser.get("https://duckduckgo.com/?q="+company_name+"+%22entreprises.lefigaro.fr%22&t=h_&ia=web")#variable company entre guillemet pour éviter que duckduckgo nous renvoi des entreprises différentes
            browser.maximize_window()
            links = browser.find_elements_by_css_selector("a[class='result__a']")#on identifie les liens que duckduckgo propose
        except:
            print("could not find research")
            pass      
        try:
            links[0].click()#clique sur le premier lien de duckduckgo
            time.sleep(generate_delay())
        except:
            print("could not click on the link")
            pass
        try:
            industry = browser.find_element_by_class_name("openData").text #on prend toutes les infos : "open data"
        except:
            print("could not fetch industry")
            industry = np.nan
            pass
        time.sleep(generate_delay())
        try: #on essaye de les mettre dans la base de donnée
            companyk.insert_one({"company":company_name,"info":industry});
        except:
            print("could not uplaod")
            pass

        
    



  
