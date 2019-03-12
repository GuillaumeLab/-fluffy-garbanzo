#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:11:45 2019

@author: Celia
"""

import numpy as np
import pandas as pd
import re

df = pd.read_csv('df_pymongo.csv')
#on prends seulement les colonnes pertinents
#df = df.loc[41:]
#on reset l'index
#df = df.reset_index()
df.drop(['index'], axis=1, inplace=True)


def cleansal(lis):
    """cleans list of dirty salaries
    replace empty list with nan and  extracts salary
    IS USED IN FIND_SALARIES"""
    for i in range(len(lis)):
        if len(lis[i])==0:
            lis[i] = np.nan
        else:
            lis[i] = lis[i][0]
    return lis

def find_salaries(df, column):
    """trouve des salaires dans la colonne et dataframe entrees en parametres
    column doit etre un string
    renvoies une liste"""
    salaries = []
    regex = r'((?:Rémunération|Gratification|Salaire|Salary)?\s?:?\s?[0-9]*(?:.|,)[0-9]*(?:.|,)[0-9]*€?\s(?:(?:to|-|à)?\s?[0-9]*(?:.|,)[0-9]*(?:.|,)[0-9]*€?\s)?\s?(?:\/|par|per)\s?(?:mois|an|year|month))'
    for i in range(len(df)):
        l = re.findall(regex,df[column][i])
        salaries.append(l)
    salaries = cleansal(salaries) #on nettoie avec la fonction cleansal 
    return(salaries)
    
def intify_etc(sals):
    """paramètres : liste de salaires en forme de string
    cette fonction convertie toutes les phrases en ints: 
    remplace les salaires avec une moyenne si c'est une fourchette
    et avec une moyenne transformé en annuel s'il sagit d'une salaire par mois
    retourne une liste netoyée, prête à étre ajouté au dataframe :)) 
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
    return sals



#This is my main function that uses the other functions below. 
def add_salaries(df):
    sals = intify_etc(find_salaries(df, 'Title'))
    df['Salary'] = sals
    return df

add_salaries(df)

#number of salaries in the data 
nbsal = len(df) - df['Salary'].isna().sum()
#percent of salaries
percent = nbsal/len(df) *100