#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:12:31 2019

@author: Celia
"""

import pandas as pd
import numpy as np

df = pd.read_csv("/Users/Celia/Documents/simplon/MachineLearning/projet_indeed/df_pymongo_new.csv", encoding = 'utf8')

df = df[["Salaires","Experience","stage","cdi","cdd","freelance","alternance","Bassin_emploi","study","langage","Seniority","Seniority_simplified"]]


df['study'] = df['study'].astype(str)
df = df.drop(df.index[8])#empty line
df = df.drop(df.index[4])#empty line 
df['Bassin_emploi'][9] = 'Paris' # Je remplace un 'ile de france' avec paris (reperé a la main)
#df = df.dropna(how='all')# drops rows with only nans 

######Pour remplir les nans de la colonne experience on va mettre la moyenne de chaque categorie "seniority"######
#Merci guillaume :p
#je créé une classe mid entre junior et senior 
df["Seniority_simplified"]=df["Seniority_simplified"].fillna("mid")
#je remplace les valeurs nulles de expérience par la valeur "executuve","junior","mid"
df["Experience"].loc[df["Experience"].isnull()]=df['Seniority_simplified'].loc[df["Experience"].isnull()]
#je remplace les valeurs nulles de junior par "0"
df["Experience"].loc[df["Experience"]=="junior"]=df["Experience"].loc[df["Experience"]=="junior"].str.replace("junior","0")
#je remplace les valeurs excutives et mid par des nan
df["Experience"]=df["Experience"].replace(r'executives|mid', np.nan, regex=True)
#je remets les string en floats
df["Experience"]=df["Experience"].astype(float)
#je remplace les valeurs manquantes de l'expérience par la moyenne des de l'XP par la seniority simplified
for i in df["Seniority_simplified"].unique():
    df["Experience"].loc[df["Seniority_simplified"]==i] = df["Experience"].fillna(df["Experience"].loc[df["Seniority_simplified"]==i].mean())

df = pd.get_dummies(df)
    
df = df.drop(["study_nan","study_1.0","study_8.0"], axis=1)
col_dict = {x: col for x, col in enumerate(df.columns)} 
df = df.drop(col_dict[29], 1)

dfnona = df.dropna()
X = dfnona.iloc[:, 1:]
y = dfnona[["Salaires"]]
y=y.astype('int')

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print(metrics.r2_score(y_test, y_pred))#-0.0473397092158
print(metrics.mean_absolute_error(y_test, y_pred))#7853.55989583
print(metrics.mean_squared_error(y_test, y_pred))#157532208.216
print(metrics.median_absolute_error(y_test, y_pred))#5000.0
print(metrics.explained_variance_score(y_test, y_pred))#-0.0466804236211