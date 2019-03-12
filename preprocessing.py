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
df['Experience'] = txt.str.extract("([0-9]+)(?=\s(an |ans |years |year ))", expand=False) #: extrait tous les nombresentre 0 et 9 
df['Experience']=df['Experience'].astype("float") #: converti les strings de nombre en chiffre
df['Experience']=df['Experience'].loc[df['Experience']<11] # élimine les l'expérience supérieure à 10 ans

""" possibilité d'amélioration 

df['Experience2'] = txt.str.extract("([^.?!;\r\n]*(?<=[.?\s!;\r\n])experience(?=[\s.?!;\r\n])[^.?!;\r\n]*[.?!;\r\n])", expand=False)# élimine les l'expérience supérieure à 10 ans
df['Experience2']
"""
