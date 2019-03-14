import pandas as pd

"""
Ce code permet d'enlever les doublons sur un dataframe. Il est devenu inutile en semaine 2. Les doublons ne sont pas scrapés dans pymongo.

df = pd.read_csv('C:/Users/Administrateur/Documents/SIMPLONr/ml/annonces.csv', sep=',', encoding='utf-8' ) # ouvre le dataset dans la dataframe df
df = df.loc[~df.Details.duplicated()] #enlève les doublons
len(df) # compte le nombre de valeurs dédoublonnées 

"""
"""
Ce code permet de créer une nouvelle colonne "seniority" qui permet d'évaluer le statut hiérarchique du poste 
"""
df['Title'] = df['Title'].str.lower() # transforme la case du titre en minuscule
List_hier =["Directeur","directrice","manager","VP","SVP","president","PDG","Director","CTO","chief","General Manager","EVP","executive","responsable région","chef","membre","board","direction","head","graduate","junior"]
df['Seniority'] = df['Title'].str.extract("(" + "|".join(List_hier) +")", expand=False)  #extrait le titre correspondant à la List_hier (liste de titre hierarchique)


"""
Ce code permet de créer une nouvelle colonne "Experience" qui permet d'évaluer le l'expérience requise pour le poste
"""

import re
import pandas as pd 
df = pd.read_csv('C:/Users/Administrateur/Documents/SIMPLONr/df_pymongo.csv', sep=',', encoding='utf-8' )
df['Experience'] = df['Details'] #créé un nouvelle colonne Expérience à partir de détail
df['Experience'] = df['Experience'].str.lower() #transforme la case en minuscule
#le code suivant transforme les mots expériences, expérience (etc) en "experience"
df['Experience'] = df['Experience'].str.replace("expérience","experience").replace("expériences","experience").replace("d'expérience","experience").replace("d'expériences","experience").replace("experiences","experience")
#le code suivant efface les mots "customer/user experience (etc) 
df['Experience'] = df['Experience'].str.replace("customer experience","").replace("online experience","").replace("user experience","")
#le code suivant remplace les en lettre par des digits
df['Experience'] = df['Experience'].str.replace("une","1").replace("un","1").replace("one","1").replace("deux","2").replace("trois","3").replace("quatre","4").replace("cinq","5").replace("six","6").replace("sept","7").replace("huit","8").replace("neuf","9").replace("dix","10").replace("quinze","15")
df['Experience'] = df['Experience'].str.replace("two","2").replace("three","3").replace("four","4").replace("five","5").replace("six","6").replace("seven","7").replace("height","8").replace("nine","9").replace("ten","10").replace("fifteen","15")

#regex pour prendre tous lesdigits avant year
df['Experience'] = df['Experience'].str.extract("([1-9]+)(?=\s(an |ans |years |year ))", expand=False)
df['Experience']=df['Experience'].astype("float")#transforme les strings en float
df['Experience']=df['Experience'].loc[df['Experience']<11]#garde uniquement les chiffres en dessous de 11 (on assume que une entreprise ne demandera pas plus de 10 ans d'expérience dans un domaine)
df['Experience']
""" possibilité d'amélioration 

df['Experience2'] = txt.str.extract("([^.?!;\r\n]*(?<=[.?\s!;\r\n])experience(?=[\s.?!;\r\n])[^.?!;\r\n]*[.?!;\r\n])", expand=False)# élimine les l'expérience supérieure à 10 ans
df['Experience2']
"""



'''
LOCATION 
'''
#le code ci-dessous permet de déterminer le bassin d'emploi en se basant sur le mot clé recherché
df['Bassin_emploi']=df['Location'] #création de la colonne bassin d'emploi
#extraction de mot clé utilisé pour la recherche
df['Bassin_emploi']=df['url'].str.extract("(?<=&l=)(.*)(?=&start)", expand=False)
#reformater île de France 
df['Bassin_emploi']= df['Bassin_emploi'].replace("%C3%AEle%20de%20france","île de france")
df['Bassin_emploi']

#le code permet une nouvelle variable appellée inner_city
df['Location']=df['Location'].str.lower()#reformater la colonne location en minuscule 
Inner_City = ["75","bordeaux","paris","nantes","toulouse","lyon"]#definir liste de valeur qui sont théoriquement dans la ville même
df['Inner_City']=df['Location'].str.extract("(" + "|".join(Inner_City) +")", expand=False) #extrait les valeurs en centre villes 
df['Inner_City']=df['Inner_City'].replace(Inner_City,"Inner_City")#remplace les valeurs en centre villes
df['Inner_City']=df['Inner_City'].notnull()
df['Inner_City']*= 1
df['Inner_City']



# cette fonction permet de detecter la langue de l'offre (fr, not fr)

from langdetect import detect # import langdetect
def try_detect(cell):# fonction pour detecter la langue
    try:
        detected_lang = detect(cell)
    except:
        detected_lang = None 
    return detected_lang

# ça a pris 3 minutes pour 7000 lignes
df['langage'] = df["Details"].apply(try_detect) # applique la fonction 
df['langage'].loc[df['lang']=="fr"].count()  #nombre d'offre en français

#binarize en fr et non fr
df['langage']=df['langage'].loc[df['lang']=="fr"] 
df['langage']=df['langage'].notnull()
df['langage']*= 1
