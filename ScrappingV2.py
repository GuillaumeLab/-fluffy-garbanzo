"""
Ce code permet de scrapper le site cible en utilisant urllib, selenium et beautiful soup
Il est toujours en développement. L'idée est de l'optimiser et de construire des classes. Nous venons de changer la méthoe de scraping en utilisant urllib et beautifulsoup 
"""
import time
from random import choice as rchoice
import random
import pandas as pd 
from bs4 import BeautifulSoup
import urllib
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import numpy as np
import time
from random import choice as rchoice
import random
import pandas as pd 
browser = webdriver.Firefox() #ouvre une instance selenium 
client = MongoClient('localhost')#ouvre mongodb
db = client.JobPosting
JobPosting = db.JobPosting #connection avec la table jobposting 

browser.get('https://www.indeed.fr/') #connection à indeed
browser.maximize_window()#passe l'instance selenium en plein écran


def generate_delay():
    """
    retourn un chiffre aléatoire suivant une distribution normal de moyenne 4 secondes et d'ecart-type de 0.8
    Ce chiffre aléatoire est le délai après chaque clique. Le but est de simuler le comportement d'un humain :
    un délai fixe peut attirer l'attention des contrôleurs, tout comme un délai aléatoire d'une distribution uniforme
    """
    mean = 4
    sigma = 0.8
    return np.random.normal(mean,sigma,1)[0]



time.sleep(generate_delay())  #attente que l'instance selenium s'ouvre
timestamp = datetime.datetime.today().strftime('%Y-%m-%d') #définition du timestamp qui sera utilisé dans le jour du scraping

#Définition du dataframe
df_indeed = pd.DataFrame({'Title' : [],'Details' : [],'Link' : [],'Company' : [],'Location' : [],'Estimated Salary' : [],'date' : [],'timestamp' : [],'detailslocconcat' : [],"url": [],"Bassin":[]}) 

 
city = ["Lyon","Toulouse","Nantes","Bordeaux"]#définition de la liste de ville cible
words = ["clk","vjs=3"]#les liens href contiennent ces deux expression 
condition = " or ".join("contains(@href, '%s')" % word for word in words) 
count=1 #ce compteur permettra de changer la ville après 90 pages
choice = "Paris" #choix de la ville 
keyword='javascript OR angular OR bootstraps OR css OR java' #mots clés utilisés pour la recherche
#estimated = " €40%C2%A0000" #utilisation potentielle de la fonction "chercher par salaires" de indeed
estimated = "" #non utilisation pour le moment
actions = ActionChains(browser) #déclaration de selenium scroller 


#Def de la fonction pour écrire le texte dans le field recherche
def pagination(choice,count,pages2):
    """Entrée: la fonction prend 3 paramètres en entrée:
    Parameter choice: il s'agit de la ville. La fonction utilise la ville lors de la déclaration du website
    Parameter count : le compteur va déclencher la fonction switch_city à partir de l'incrémentation 89
    Parameter page2 :  le compteur utilise la variable page2, qui sera incrémentée 
    Action : Cette fonction sert à choisir la page de recherche
    Output : changement de la page de recherche. Déclenchement de la fonction city_switch sur la 90ème page 
    """
    pagination.counter += 1  #incrémentation du compteur de la fonction
    print("counter pagination!"+str(pagination.counter)) #incrémentation du compteur de la fonction
    pages2 = "&start="+str(pagination.counter)+"0" # page output
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2) #website
    print("my count var is "+str(count)) 
    while count<90: 
        count += 1 
        try:
            browser.get(website)
            print(choice)
        except:
            browser.get(website)
            print("error on pagination function")
            time.sleep(generate_delay())
        randomize_click(choice,count)   #repart sur la fonction initiale
    switch_city(count)#repart sur la fonction initiale
    



def randomize_click(choice,count):
    """Entrée: la fonction prend 2 paramètres en entrée:
    Parameter choice: il s'agit de la ville. La fonction utilise la ville lors de la déclaration du website
    Parameter count : la fonction prend le paramètre count [mais ne l'utilise pas ]
    
    Action : Cette fonction sert à choisir aléatoirement le lien sur lequel cliquer pour reproduire le comportement d'un humain 
    Output : la fonction va renvoyer la variable i qui sera utilisée lors du scraping 
    """
    pages2 = "&start="+str(pagination.counter)+"0"
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2)
    try: 
        browser.get(website) #reload le site 
        links = list(set(browser.find_elements_by_xpath("//a[%s]" % condition))) #définit la liste d'élements
    except:#si ça ne marche, il y a peut-être un pop up. pour l'instant on passe en attendant de trouver une solution
        time.sleep(generate_delay())
        pass
    randompage = [len(links)]#cela permet de quantifier le nombre de liens 
    number = [i for i in range(random.choice(randompage))] # créé la liste de ville
    for i in range(len(links)):
        while number != []:
            choice_num = random.choice(number)#choice_num prend un le nom d'une numbre entre 0 et 15 pour éviter d'ouvrir les pages l'une après l'autre
            number.remove(choice_num)
            i = choice_num #choice_num prend un le nom d'une numbre entre 0 et 15 pour éviter d'ouvrir les pages l'une après l'autre
            scraping_jobpost(i,choice,pages2)
        pagination(choice,count,pages2)




def switch_city(count):
    """Entrée: la fonction prend 3 paramètres en entrée:
    Parameter choice: il s'agit de la ville. La fonction utilise la ville lors de la déclaration du website
    Parameter count : le compteur va déclencher la fonction switch_city à partir de l'incrémentation 89
    Parameter page2 :  le compteur utilise la variable page2, qui sera incrémentée 
    Action : Cette fonction sert à choisir la page de recherche
    Output : changement de la page de recherche. Déclenchement de la fonction city_switch sur la 90ème page 
    """
    count = 0 #reset the var count to 0 
    choice = random.choice(city)#choice prend un le nom d'une ville dans la liste de villes 
    time.sleep(generate_delay())
    print(choice)
    city.remove(choice)# efface la ville selectionnée de la liste
    randomize_click(choice,count)  #repart sur la fonction initiale

#Def de la fonction scraping
def scraping_jobpost(i,choice,pages2):
    """Entrée: la fonction prend 3 paramètres en entrée:
    Parameter choice: il s'agit de la ville. La fonction utilise la ville lors de la déclaration du website
    Parameter i : le numéro aléatoire du lien défini dans la fonction randomize click 
    Parameter page2 :  le compteur utilise la variable page2, qui sera incrémentée 
    Action : Cette fonction sert à scraper l'information et à ajouter les données dans la base de données, si l'info n'est pas présente
    """
    time.sleep(generate_delay())
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2) #website
    links = list(set(browser.find_elements_by_xpath("//a[%s]" % condition)))
    linko = links[i]
    yourUrl = linko.get_attribute("href")
    print(yourUrl)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(yourUrl, headers = headers)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, from_encoding=page.info().get_param('charset'))
    time.sleep(generate_delay())
    
    try:
        linked = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})
    except:
        print("could not click on the link")
        linked=np.nan
        pass
    try:
        Date = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})
    except:
        print("could not fetch header")
        Date=np.nan
        pass
    try:
        Title = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})[1]
    except:
        print("could not fetch header")
        Title=np.nan
        pass
    
    try:
        Company = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})
    except:
        print("could not fetch company")
        Company = np.nan
        pass
        
    try:
        Location = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})
    except:
        print("could not fetch location")
        Location = np.nan
        pass
    try:
        Details = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})
    except:
        print("could not fetch role description")
        Details = np.nan
        pass
    try:
        DetailsLoc = soup.findAll("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"})
    except:
        print("could not concat")
        DetailsLoc = np.nan
        pass
    try:
        Bassin = choice
    except:
        print("could not concat")
        DetailsLoc = np.nan
        pass
    #try:
        #if db.JobPostings.find_one({'DetailsLoc': DetailsLoc})==None:
            #db.JobPostings.insert_one({"Title":Title,"Details":Details,"linked":linked,"Company":Company,"Location":Location,"estimated":estimated,"Date":Date,"timestamp":timestamp,"DetailsLoc":DetailsLoc,"url":url});
    #except:
        #print("could not upload data or already there")
    url = browser.current_url
    time.sleep(generate_delay())
    df_indeed.loc[scraping_jobpost.counter]=[Title,Details,linked,Company,Location,estimated,Date,timestamp,DetailsLoc,url,Bassin]
    df_indeed.to_csv('df_indeed1.csv', index=False, header=True)
    print("counter"+str(scraping_jobpost.counter))
    scraping_jobpost.counter += 1 





def set_up_counters():
    """Input : no inputs

    Action : cette fonction défini les compteurs. Cela permet de reprendre sur la bonne page si la connection internet a été coupée ( et la bonne colonne du dataframe si besoin)
    Output :les compteurs pagination et srapping jobposts sont ici definis.la fonction utilise "emporte" count et choice dans la fonction randomize_click (certainement effacé lors de la prochaine version)
    """ 
    pagination.counter = 0
    scraping_jobpost.counter = 0
    pages2 = "&start="+str(pagination.counter)+"0"
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2)
    randomize_click(choice,count)


set_up_counters()
