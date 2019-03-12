# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:26:21 2019

@author: Administrateur
"""

import re
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
import seaborn as sns

# 1/ Importer le dataset et
#df = pd.read_csv('annonces.csv')
df = pd.read_csv('df_pymongo.csv')

# les données commencent à la 32 ème ligne
df=df.loc[32:]
df=df.reset_index()
# compter le nbre de nans 
nbr_nan=df.isnull().sum()


# ajouter une colonne niveau_etude
#df1.loc[:, 'typ_contrat'] = ''
#df.loc[:, 'niv_etude'] = ''
df.loc[:, 'langages'] = ''
df['Details'] = df['Details'].str.lower()

# pour extraire la formation: on crée la fonction niveau_etudes
def langages_pro(df):
    """ regex est le regex pour extraire les outils et langages demandés
    :qu'on cherche dans la colonne Details
    """
    langage=[]
    
    regex = r'(?:R |python|sql|nosql|mysql|matlab|c\+\+?|scala|ruby|php|vba|machine learning|javascript|java|hadoop|spark|mongodb\
              |cassandra|nlp|maths|statistics|statistique|physics|physique|qlikview|sci-kit learn|pandas|numpy\
              |excel|powerpoint|kpi|dashboard|qlikview|d3|sas|spss\
              |api|nlp|physics|scikit-learn|)'
   # z = re.compile(r'[bB]ac ?\+ ?\d?\/?\d?|Master')
    
    for i in range(0, len(df)):
        L = re.findall(regex,str(df['Details'][i]))
        L = list(set(L))
        langage.append(L)
    return( langage)
langage = langages_pro(df)

df["langages"] = langage
