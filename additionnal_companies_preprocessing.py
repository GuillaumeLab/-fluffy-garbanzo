import pymongo
import pandas as pd
from pymongo import MongoClient
client = MongoClient()
db = client.new_indeed_raw
collection = db.companies
data = pd.DataFrame(list(collection.find()))

#on prends seulement les colonnes pertinentes
data = data.loc[9:]#on prends seulement les colonnes pertinentes
data = data.reset_index() #on reset l'index
data.to_csv('df_capital.csv', index=False, header=True)

info_corp = pd.read_csv('df_capital.csv',encoding='utf-8')
import re

#info_corp['Capital'] = info_corp['info'].str.extract("([^.?!;\r\n]*(?<=[.?\s!;\r\n])Capital \: (?=[\s.?!;\r\n])[^.?!;\r\n]*[.?!;\r\n])", expand=False)
for i in range(len(info_corp['info'])):
    info_corp['info'][i]=re.sub(r'(\d)\s+(\d)', r'\1\2', str(info_corp['info'][i]))

info_corp['Capital'] = info_corp['info'].str.extract("(Capital \: \d+)", expand=False) #on prend l'info Capital de l'entreprise
info_corp['Capital'] = info_corp['Capital'].str.extract("([0-9]+)").astype(float) 
info_corp['Capital'] 
info_corp['Chiffre']= info_corp['info'].str.extract("(Chiffre d\'affaires \d+)", expand=False) #on prend l'info Chiffre d'affaire de l'entreprise
info_corp['Chiffre'] = info_corp['Chiffre'].str.extract("([0-9]+)").astype(float)
info_corp['Chiffre']
info_corp['Activité'] = info_corp['info'].str.extract("((?<=\nActivité :).*(?=\.))", expand=False)#on prend l'info Activité de l'entreprise

info_corp['Activité'] = info_corp['info'].str.extract("((?<=\nActivité :).*(?=\.))", expand=False)  #on prend l'info code NAF / APE de l'entreprise
info_corp['Activité2'] = info_corp['info'].str.extract("((?<=NAF / APE :\r\n).*(?=\)))", expand=False)  
info_corp['Activité']

info_corp['Type'] = info_corp['info'].str.extract("((?<=Taille d\'entreprise :\r\n).*(?=\r\n))", expand=False) #on prend le type d'entreprise 

info_corp["Company"]=info_corp["company"] #on prend le type d'entreprise 
info_corp=info_corp.drop(["_id","index","company"],axis=1) #on prend le type d'entreprise
info_corp["Company"]=info_corp["Company"].str.replace("'", "")
#info_corp=info_corp.set_index('Company')

info_corp.to_csv('info_corp.csv', index=False, header=True)
