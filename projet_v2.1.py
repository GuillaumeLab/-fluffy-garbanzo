# Scraping Indeed

# Importation des librairies
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

# Préparation de la visualisation
plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'

# Importation du dataframe
annonces = pd.read_csv('annonces.csv',encoding='utf-8')

# Suppression de colonnes inutiles
annonces.drop(['index','estimated','linked','_id'], axis=1, inplace=True)

# On passe les colonnes interessantes en minuscules pour faciliter les regex
annonces['Title'] = annonces['Title'].str.lower() 
annonces['Details'] = annonces['Details'].str.lower()

# Data preprocessing : Expérience

# Nouvelle colonne 'Experience' à partir de 'Details'
annonces['Experience'] = annonces['Details'] 

# On extrait les 'expériences' en 'expérience' selon différentes syntaxes possibles
annonces['Experience'] = annonces['Experience'].str.replace("expérience","experience").replace("expériences","experience").replace("d'expérience","experience").replace("d'expériences","experience").replace("experiences","experience")
annonces['Experience'] = annonces['Experience'].str.replace("several","2").replace("plusieurs","2").replace("plusieurs années","2").replace("several years","2")
annonces['Experience'] = annonces['Experience'].str.replace("customer experience","").replace("online experience","").replace("user experience","")

# On remplace les durées en lettres par des digits
annonces['Experience'] = annonces['Experience'].str.replace("une","1").replace("un","1").replace("one","1").replace("deux","2").replace("trois","3").replace("quatre","4").replace("cinq","5").replace("six","6").replace("sept","7").replace("huit","8").replace("neuf","9").replace("dix","10").replace("quinze","15")
annonces['Experience'] = annonces['Experience'].str.replace("two","2").replace("three","3").replace("four","4").replace("five","5").replace("six","6").replace("seven","7").replace("eight","8").replace("nine","9").replace("ten","10").replace("fifteen","15")

#  Regex pour prendre tous les digits avant 'year/years/ans/an ...'
tmp = annonces['Experience'].str.extractall("([0-9]+)(?=\s(an |ans |année |années |years |year |ans\r\n|années\r\n|année\r\n|an\r\n|year\r\n|years\r\n|ans,|année,|an,|années,|years,|year;|years;|ans;|an;|année;|années;|year.|years.|ans.|an.|année.|années.))")
tmp[0]=tmp[0].astype("float")
# On elimine les valeurs suppérieures à 10 (hypothèse : les employeurs ne prennent pas plus de 11 ans d'expérience)
tmp[0]=tmp[0].loc[tmp[0]<11]  
tmp=tmp.groupby(level=0).max() #on garde la valeur maximum ()
annonces['Experience'] = tmp.groupby(tmp.index.get_level_values(0)).agg(list) #on réinsere les groupes dans le dataframe

# Data preprocessing : Type de poste

# on déclare une liste de mots clés pour recherche le type de poste dans annonces
type_poste =["directeur","directrice","manager","vp","svp","president","pdg","director","cto","chief","general manager","evp","executive","responsable région","chef","membre","board","direction","head","graduate","junior"]
# on appelle str.extract qui va se charger de reconnaitre les items de la liste
annonces['Seniority'] = annonces['Title'].str.extract("(" + "|".join(type_poste) +")", expand=False)


# Data preprocessing : Contrats

# on cherche les contrats dans ces colonnes avec une regex
# et on remplit une liste de contrats pour chaque annonce

def type_de_contrat(df):
    liste_contrats = []
    regex = r'(?:independent|contracts|contract|interim|internship|intership|permanent|short-term|short term|full-time|part-time|part time|full time|student|student job|student jobs|cdi|cdd|stage|alternance|apprentissage|professionnalisation|freelance|indépendant|independant)'
    for i in range(len(df)):
        l = re.findall(regex,str(df['Title' and 'Details'][i]))
        l = list(set(l))
        liste_contrats.append(l)
    return(liste_contrats)

# on appelle la fonction qui extrait les contrats
c = type_de_contrat(annonces)
# on remplit une colonne 'Contrat' au propre dans le dataframe
c = np.array(c)
annonces["Contrat"] = c

# Data preprocessing : Salaires

# On nettoie les salaires et on remplace les valeurs vides par des nan
def cleansal(liste):
    for i in range(len(liste)):
        if len(liste[i])==0:
            liste[i] = np.nan
        else:
            liste[i] = liste[i][0]
    return liste

def trouver_salaires(df, colonne):
# on trouve des salaires dans 'colonne' et dans le dataframe entrés en paramètres
# 'colonne' doit etre une string sur laquelle on applique la regex
# on renvoie une liste 
    s = []
    regex = r'((?:Rémunération|Gratification|Salaire|Salary)?\s?:?\s?[0-9]*(?:.|,)[0-9]*(?:.|,)[0-9]*€?\s(?:(?:to|-|à)?\s?[0-9]*(?:.|,)[0-9]*(?:.|,)[0-9]*€?\s)?\s?(?:\/|par|per)\s?(?:mois|an|year|month) )'
    for i in range(len(df)):
        l = re.findall(regex,str(df[colonne][i]))
        s.append(l)
    s = cleansal(s) #on nettoie avec la fonction cleansal 
    return(s)
    
def intify_etc(sals):
    """ sals : liste de salaires en forme de string
    cette fonction convertie toutes les phrases en int's: 
    remplace les salaires avec une moyenne si c'est une fourchette
    et avec une moyenne transformé en annuel s'il sagit d'une salaire par mois
    retourne une liste nettoyée, prête à être ajoutée au dataframe :)) 
    """
    regex = '[0-9]*? ?[0-9]{3}'
    #for each line
    for i in range(len(sals)):
        #if it's not a nan
        if type(sals[i]) != float:
            #now we must separate per months from per year 
            #and fourchettes from non fourchettes
            if 'par an' in sals[i]:
                #print('par an')
                if '-' in sals[i]:
                    #print('fourchette')
                    frm = re.findall(regex,sals[i])[0]
                    to = re.findall(regex,sals[i])[1]
                    frm, to = frm.replace(' ',''), to.replace(' ','')#getting rid of space
                    frm, to = int(frm), int(to)#convert to int 
                    avg = (frm+to)/2 #calculate average
                    sals[i] = avg
                else:
                    #print('not fourchette')
                    sal = re.findall(regex,sals[i])[0]
                    sal=sal.replace(' ','')#get rid of space
                    sals[i] = int(sal)#convert to int
            elif 'par mois' in sals[i]:
                #print('par mois')
                if '-' in sals[i]:
                    #print('fourchette')
                    frm = re.findall(regex,sals[i])[0]
                    to = re.findall(regex,sals[i])[1]
                    frm, to = frm.replace(' ',''), to.replace(' ','')#get rid of the space
                    frm, to = int(frm), int(to)#converting to int
                    avg = (frm+to)/2#calculate average
                    par_an = avg*12#convert to yearly salary
                    sals[i] = par_an
                else:
                    #print('not fourchette')
                    sal = re.findall(regex,sals[i])[0]
                    sal = sal.replace(' ','')#get rid of space
                    sals[i] = int(sal)*12#convert to yearly salary
        elif type(sals[i]) == str:
            sals[i] = np.nan
    return sals

# on extrait les salaires 
s = intify_etc(trouver_salaires(annonces, 'Title'))
# on les ajoute dans une nouvelle colonne
annonces['Salaires'] = s


# Data preprocessing : Niveau d'études

# ajouter une colonne niveau_etude

def niveau_etudes(df):
    # z est la regex pour extraire Bac+.., bac +..., Master
    # qu'on va chercher dans la colonne Details
    etude=[]
    z = re.compile(r'bac ?\+ ?\d?\/?\d?|master')
    
    for i in range(len(df)):
        bac = re.findall(z,str(df['Details'][i]))
        bac = list(set(bac))
        etude.append(bac)
    return(etude)

# on appelle la fonction qui traite le niveau d'études
annonces["Niveau d'études"] = niveau_etudes(annonces)

# Data preprocessing : Location

# le code ci-dessous permet de déterminer le bassin d'emploi en se basant sur le mot clé recherché
annonces['Bassin_emploi'] = annonces['Location'] #création de la colonne bassin d'emploi
# extraction de mot clé utilisé pour la recherche
annonces['Bassin_emploi'] = annonces['url'].str.extract("(?<=&l=)(.*)(?=&start)", expand=False)
# reformater île de France 
annonces['Bassin_emploi'] = annonces['Bassin_emploi'].replace("%C3%AEle%20de%20france","île de france")

# le code permet une nouvelle variable appellée inner_city
annonces['Location'] = annonces['Location'].str.lower()#reformater la colonne location en minuscule 
Inner_City = ["75","bordeaux","paris","nantes","toulouse","lyon"]#definir liste de valeur qui sont théoriquement dans la ville même
annonces['Inner_City'] = annonces['Location'].str.extract("(" + "|".join(Inner_City) +")", expand=False) #extrait les valeurs en centre villes 
annonces['Inner_City'] = annonces['Inner_City'].replace(Inner_City,"Inner_City")#remplace les valeurs en centre villes
annonces['Inner_City'] = annonces['Inner_City'].notnull()
annonces['Inner_City'] *= 1

# Cette fonction permet de detecter la langue de l'offre (fr, not fr)

from langdetect import detect # import langdetect

def try_detect(cell):# fonction pour detecter la langue
    try:
        detected_lang = detect(cell)
    except:
        detected_lang = None 
    return detected_lang

# ça a pris 3 minutes pour 7000 lignes
annonces['langage'] = annonces["Details"].apply(try_detect) # applique la fonction 
annonces['langage'].loc[annonces['langage']=="fr"].count()  #nombre d'offre en français

#binarize en fr et non fr
annonces['langage'] = annonces['langage'].loc[annonces['langage']=="fr"] 
annonces['langage'] = annonces['langage'].notnull()
annonces['langage'] *= 1

# Data preprocessing : Compétences 

# on extrait les compétences spécifiques avec une regex
def langages_pro(df):
    # on cherche dans la colonne 'Details'
    langage=[]
    regex = r'(?:R|python|sql|nosql|mysql|matlab|c\+\+?|scala|ruby|php|vba|machine learning|javascript|java|hadoop|spark|mongodb\
              |cassandra|nlp|maths|statistics|statistique|physics|physique|qlikview|sci-kit learn|pandas|numpy\
              |excel|powerpoint|kpi|dashboard|qlikview|d3|sas|spss\
              |api|nlp|physics)'
    
    for i in range(0, len(df)):
        L = re.findall(regex,str(df['Details'][i]))
        L = list(set(L))
        langage.append(L)
    return(langage)

annonces["Langages"] = langages_pro(annonces)


# Correction des salaires outliers (à partir de 200000€ / an) on divise par 12
mask = annonces['Salaires'] >= 200000
m = annonces[mask]
print(m)
for i in m.index.values:
    annonces['Salaires'][i] = int(annonces['Salaires'][i]/12)

# on plot les salaires
plt.scatter(annonces.index.values,annonces['Salaires'],color='r')
plt.title('Salaire (€ brut/an) ')
plt.xlabel('index')
plt.ylabel('Salaire')
plt.show()

# enlever crochets dans les colonnes
annonces['Contrat']=annonces['Contrat'].astype(str).str.replace('\[|\]|\'', '')
annonces["Niveau d'études"]=annonces["Niveau d'études"].astype(str).str.replace('\[|\]|\'', '')   
annonces['Languages']=annonces['Languages'].astype(str).str.replace('\[|\]|\'', '')

annonces['Experience']=annonces['Experience'].astype(str).str.replace('\[|\]|\'', '')
