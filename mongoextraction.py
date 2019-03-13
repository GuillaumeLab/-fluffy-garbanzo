"""
Ce petit bout de code permet d'extraire la base de donnée brute et de la reformater.

"""
import pymongo
import pandas as pd
from pymongo import MongoClient
client = MongoClient()
db = client.JobPosting
collection = db.JobPostings
data = pd.DataFrame(list(collection.find()))

data = data.loc[41:]#on prends seulement les colonnes pertinentes
data = data.reset_index() #on reset l'index
data = data.drop(["DetailsLoc"],axis=1) #efface la colonne  DetailsLoc, qui ne servait qu'à checker les doublons pendant le scrapping
data.to_csv('df_pymongo.csv', index=False, header=True)
