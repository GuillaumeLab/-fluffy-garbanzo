# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:00:52 2019

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
# details correspond à la colonne Details
#details=df1['Details']

# ajouter une colonne niveau_etude
#df1.loc[:, 'typ_contrat'] = ''
df.loc[:, 'niv_etude'] = ''
#df1.loc[:, 'langages'] = ''


# pour extraire la formation: on crée la fonction niveau_etudes
def niveau_etudes(df):
    """ z est le regex pour extraire Bac+.., bac +..., Master
    qu'on va chercher dans la colonne Details
    """
    etude=[]
    z = re.compile(r'[bB]ac ?\+ ?\d?\/?\d?|Master')
    
    for i in range(len(df)):
        bac = re.findall(z,df['Details'][i])
        bac = list(set(bac))
        etude.append(bac)
    return(etude)
etude = niveau_etudes(df)

def eliminedoublons(liste):
    """ pour eliminer les doublons dans une même annonce, on crée la fonction
    eliminedoublons
    """
    r = []
    for elem in liste:
        if isinstance(elem, list):
            r2 = []
            for elem2 in elem:
                if elem2 not in r2:
                    r2.append(elem2)
            r.append(r2)
        else:
            r.append(elem)
    return r

etude_sansDoublons=eliminedoublons(etude)

df1["niv_etude"] = etude_sansDoublons


