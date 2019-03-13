import time
from random import choice as rchoice
import random
import pandas as pd 
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
browser = webdriver.Firefox()
import datetime
import numpy as np
client = MongoClient('localhost')
db = client.JobPosting
JobPosting = db.JobPosting

browser.get('https://www.indeed.fr/')
browser.maximize_window()
import numpy as np

def generate_delay():
    """
    retourn un chiffre aléatoire suivant une distribution normal de moyenne 4 secondes et d'ecart-type de 0.8
    Ce chiffre aléatoire est le délai après chaque clique. Le but est de simuler le comportement d'un humain :
    un délai fixe peut attirer l'attention des contrôleurs, tout comme un délai aléatoire d'une distribution uniforme
    """
    mean = 4
    sigma = 0.8
    return np.random.normal(mean,sigma,1)[0]

#browser.set_window_size("3024", "3024")
time.sleep(generate_delay())
time.sleep(generate_delay())
timestamp = datetime.datetime.today().strftime('%Y-%m-%d')
import time
from random import choice as rchoice
import random
import pandas as pd 
df_indeed = pd.DataFrame({'Title' : [],'Details' : [],'Link' : [],'Company' : [],'Location' : [],'Estimated Salary' : [],'date' : [],'timestamp' : [],'detailslocconcat' : [],"url": []})
city = ["Lyon","Toulouse","Nantes","Bordeaux"]
words = ["clk"]
count=0
condition = " or ".join("contains(@href, '%s')" % word for word in words)
choice = "Nantes"
keyword='javascript OR angular OR bootstraps OR css OR java'
#estimated = " €40%C2%A0000"
estimated = ""
actions = ActionChains(browser)


#Def de la fonction pour écrire le texte dans le field recherche
def pagination(choice,count,pages2):
    """Input
    Parameter:
    Parameter:
    Output
    """
    pagination.counter += 1
    print("counter pagination!"+str(pagination.counter))
    pages2 = "&start="+str(pagination.counter)+"0"
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2)
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
    """Input : this function takes count as an input. It opens a link taking pages2 as an input
    Parameter:
    Parameter:
    Output : 
    """
    pages2 = "&start="+str(pagination.counter)+"0"
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2)
    browser.get(website)
    links = browser.find_elements_by_class_name('jobtitle')
    randompage = [len(links)]#randompage is a random number to state the number
    number = [i for i in range(random.choice(randompage))] #number also decide of the number of iterations
    linkswith_duplicates = browser.find_elements_by_xpath("//a[%s]" % condition)
    for i in range(len(links)):
        while number != []:
            choice_num = random.choice(number)#choice_num prend un le nom d'une numbre entre 0 et 15 pour éviter d'ouvrir les pages l'une après l'autre
            number.remove(choice_num)
            i = choice_num
            scraping_jobpost(i,choice,pages2)
            #except:
                 #print('error on something undefined')
                 #browser.back()
                 #time.sleep(generate_delay())
                 #pass
                
        #browser.get("https://www.indeed.fr/emplois?q=%22Intelligence+Artificielle%22+OR+DATA+OR+IA+OR+AI"+str(choice))
        pagination(choice,count,pages2)




def switch_city(count):
    """Input
    Parameter:
    Parameter:
    Output
    """
    count = 0 #reset the var count to 0 
    choice = random.choice(city)#choice prend un le nom d'une ville dans la liste de villes 
    time.sleep(generate_delay())
    print(choice)
    city.remove(choice)# efface la ville selectionnée de la liste
    randomize_click(choice,count)   #repart sur la fonction initiale

#Def de la fonction scraping
def scraping_jobpost(i,choice,pages2):
    """Input
    Parameter:
    Parameter:
    Output
    """ 
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2)
    browser.set_window_size("3024", "3024")
    links = browser.find_elements_by_class_name('jobtitle')
    try:
        browser.execute_script("arguments[0].scrollIntoView();", links[i])
        browser.execute_script("window.scrollBy(0, -250);")
    except:
        print("could not find the link to scroll")
        pass
    try:
        links[i].click()
        time.sleep(generate_delay())
    except:
        try:
            browser.get(website)
            time.sleep(generate_delay())
            links = browser.find_elements_by_class_name('jobtitle')
            links[i].click()
            time.sleep(generate_delay())
        except:
            print("could not click on the link")
            pass
    #print(links[i].text)
    try:
        linked = links[i].text
    except:
        print("could not click on the link")
        linked=np.nan
        pass
    try:
        Date = browser.find_element_by_class_name('date').text
    except:
        print("could not fetch header")
        Date=np.nan
        pass
    try:
        Title = browser.find_element_by_xpath('//*[@id="vjs-header-jobinfo"]').text
    except:
        print("could not fetch header")
        Title=np.nan
        pass
    
    try:
        Company = browser.find_element_by_xpath('//*[@id="vjs-cn"]').text
    except:
        print("could not fetch company")
        Company = np.nan
        pass
        
    try:
        Location = browser.find_element_by_xpath('//*[@id="vjs-loc"]').text
    except:
        print("could not fetch location")
        Location = np.nan
        pass
    try:
        Details = browser.find_element_by_xpath('//*[@id="vjs-content"]').text
    except:
        print("could not fetch role description")
        Details = np.nan
        pass
    try:
        DetailsLoc = Details+Location+Title
    except:
        print("could not concat")
        DetailsLoc = np.nan
        pass
    url = browser.current_url
    time.sleep(generate_delay())
    df_indeed.loc[scraping_jobpost.counter]=[Title,Details,linked,Company,Location,estimated,Date,timestamp,DetailsLoc,url]
    df_indeed.to_csv('df_indeed1.csv', index=False, header=True)
    try:
        if db.JobPostings.find_one({'DetailsLoc': DetailsLoc})==None:
            db.JobPostings.insert_one({"Title":Title,"Details":Details,"linked":linked,"Company":Company,"Location":Location,"estimated":estimated,"Date":Date,"timestamp":timestamp,"DetailsLoc":DetailsLoc,"url":url});
    except:
        print("could not upload data or already there")
    print("counter"+str(scraping_jobpost.counter))
    scraping_jobpost.counter += 1 
    browser.back()




def set_up_counters():
    """Input
    Parameter:
    Parameter:
    Output
    """ 
    pagination.counter = 0
    scraping_jobpost.counter = 0
    pages2 = "&start="+str(pagination.counter)+"0"
    website = "https://www.indeed.fr/emplois?q="+str(keyword)+str(estimated)+"&l="+str(choice)+str(pages2)
    randomize_click(choice,count)


set_up_counters()
