from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
browser = webdriver.Firefox()
#browser = webdriver.Firefox(executable_path='C:/path/to/geckodriver.exe') #au cas où geckdriver.exe n'est pas dans le path ni au même endroit
browser.get('https://www.indeed.fr/emplois?q=%22Intelligence+Artificielle%22+OR+DATA+OR+IA+OR+AI+OR+%22machine+learning%22+OR+%22donn%C3%A9e%22+OR+%22donn%C3%A9es%22+OR+BI+OR+%22intelligence%22&l=France')
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

time.sleep(generate_delay())
time.sleep(generate_delay())
time.sleep(generate_delay())
time.sleep(generate_delay())


import time
from random import choice as rchoice
import random
import pandas as pd 
pages2 = "&start="+str(pagination.counter)+"0"
df_indeed = pd.DataFrame({'Title' : [],'Details' : [],'Link' : [],'Company' : [],'Location' : []})
city = ["Lyon","Toulouse","Nantes","Bordeaux"]
words = ["clk"]
count=0
condition = " or ".join("contains(@href, '%s')" % word for word in words)
choice = "île de france"
keyword="data OR developeur"

actions = ActionChains(browser)
def loop(choice,count):
    count += 1
    pages2 = "&start="+str(pagination.counter)+"0"
    browser.get("https://www.indeed.fr/emplois?q="+str(keyword)+"&l="+str(choice)+str(pages2))
    randompage = [19]#randompage is a random number to state the number of links openened per city
    number = [i for i in range(random.choice(randompage))] #number also decide of the number of iterations
    time.sleep(generate_delay())
    linkswith_duplicates = browser.find_elements_by_xpath("//a[%s]" % condition)
    links = browser.find_elements_by_class_name('jobtitle')
    for i in range(len(links)):
        while number != []:
            choice_num = random.choice(number)#choice_num prend un le nom d'une numbre entre 0 et 15 pour éviter d'ouvrir les pages l'une après l'autre
            number.remove(choice_num)
            i = choice_num
            scraping_(i,choice,pages2)
            #except:
                 #print('error on something undefined')
                 #browser.back()
                 #time.sleep(generate_delay())
                 #pass
                
        #browser.get("https://www.indeed.fr/emplois?q=%22Intelligence+Artificielle%22+OR+DATA+OR+IA+OR+AI"+str(choice))
        pagination(choice,count)
        time.sleep(generate_delay())



#Def de la fonction pour écrire le texte dans le field recherche
def pagination(choice,count):
    """entree : il prend count en entrée. Count est une variable qui prend qiu est égale sortie """
    time.sleep(generate_delay())
    pagination.counter += 1
    print("counter pagination!"+str(pagination.counter))
    pages2 = "&start="+str(pagination.counter)+"0"
    print("my count var is "+str(count))
    while count<99:
        count += 1
        try:
            browser.get("https://www.indeed.fr/emplois?q="+str(keyword)+"&l="+str(choice)+str(pages2))
            print(choice)
        except:
            browser.get("https://www.indeed.fr/emplois?q="+str(keyword)+"&l="+str(choice)+str(pages2))
            print("error on pagination function")
            time.sleep(generate_delay())
        loop(choice,count)   #repart sur la fonction initiale
    switch_city(count)#repart sur la fonction initiale
    

def switch_city(count):
    count = 0 #reset the var count to 0 
    choice = random.choice(city)#choice prend un le nom d'une ville dans la liste de villes 
    time.sleep(generate_delay())
    print(choice)
    city.remove(choice)# efface la ville selectionnée de la liste
    time.sleep(generate_delay())
    loop(choice,count)   #repart sur la fonction initiale

#Def de la fonction scraping
def scraping_(i,choice,pages2):
    time.sleep(generate_delay())
    links = browser.find_elements_by_class_name('jobtitle')
    try:
        browser.execute_script("arguments[0].scrollIntoView();", links[i])
        browser.execute_script("window.scrollBy(0, -250);")
    except:
        print("could not find the link to scroll")
        pass
    try:
        links[i].click()
    except:
        print("could not click on the link")
        browser.get("https://www.indeed.fr/emplois?q="+str(keyword)+"&l="+str(choice)+str(pages2))
        time.sleep(generate_delay())
        pass
    time.sleep(generate_delay())
    links = browser.find_elements_by_class_name('jobtitle')
    print(links[i].text)
    try:
        links[i].click()
    except:
        print("could not click on the link")
        time.sleep(generate_delay())
        pass
    linked = links[i].text
    time.sleep(generate_delay())
    try:
        Title = browser.find_element_by_xpath('//*[@id="vjs-header-jobinfo"]')
    except:
        print("could not fetch header")
        pass
    try:
        Company = browser.find_element_by_xpath('//*[@id="vjs-cn"]')
    except:
        print("could not fetch company")
        pass
    try:
        Location = browser.find_element_by_xpath('//*[@id="vjs-loc"]')
    except:
        print("could not fetch location")
        pass
    try:
        Details = browser.find_element_by_xpath('//*[@id="vjs-content"]')
    except:
        print("could not fetch role description")
        pass
    time.sleep(generate_delay())
    df_indeed.loc[scraping_.counter]=[Title.text,Details.text,linked,Company.text,Location.text]
    df_indeed.to_csv('df_indeed2.csv', index=False, header=True)
    print("counter"+str(scraping_.counter))
    scraping_.counter += 1
    browser.back()
    time.sleep(generate_delay())


    
def main():
    scraping_.counter = 0
    pagination.counter = 0
    while pages2 != "&start="+str(99)+"0":
        loop(choice,count)
    search_city()
    

main()   
