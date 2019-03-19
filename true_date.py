# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:08:55 2019

@author: Hugh
"""
# Fonction vraie_date - Une fonction qui donne la vraie date de publication
# d'une offre d'emploi en prenant une ligne d'un df dont la
# colonne "Date" est en forme "Il y a..." et qui a une colonne "timestamp"
# Entrées: pd.DataFrame df
# Actions: Rien
# Sorties: pd.Series - une colonne avec le même nombre de lignes que df
def vraie_date(df):
    
    # Première fonction pour trouver l'unité de temps après "il y a"
    unit_dic = {"heure": "h", "jour":"D", "mois":"D", "minute":"m", "second":"second"}
    def unit_giver(jobby):
        temp = jobby
        for scale in unit_dic.keys():
            if scale in temp:
                temp = unit_dic[scale]
        return temp

    # Petite fonction pour enlever les symboles '+'
    def plus_remover(jobby):
        temp = jobby
        if "+" in temp:
            temp = temp[:-1]
        return pd.to_numeric(temp, errors='coerce')

    # Crée un tuple contenant les sorties des fonctions au-dessus pour
    # une ligne du dataset
    def time_diff(jobby):
        if "mois" not in jobby[1]:
            return plus_remover(jobby[0]), unit_giver(jobby[1])
        return plus_remover(30*jobby[0]), unit_giver(jobby[1])

    return df["timestamp"] - df["Date"].apply(lambda x: time_diff(x[7:].split(" "))).apply(lambda x: pd.to_timedelta(x[0], unit=x[1]))