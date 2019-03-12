# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:07:18 2019

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

df.loc[:, 'experiences'] = ''
df['Details'] = df['Details'].str.lower()
#aa=df['Details'][501]
# pour extraire la formation: on crée la fonction niveau_etudes
def experiences(df):
    """ regex est le regex pour extraire les outils et langages demandés
    :qu'on cherche dans la colonne Details
    """
    exp=[]
    
    regex = r'(\d à \d ans|\d ans)'
    
    
    for i in range(0, len(df)):
        e = re.findall(regex,str(df['Details'][i]))
        e = list(set(e))
        exp.append(e)
    return(exp)
exp = experiences(df)

df["experiences"] = exp