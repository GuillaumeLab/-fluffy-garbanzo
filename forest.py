import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
#set the random seed
np.random.seed(0)

df = pd.read_csv("/Users/Celia/Documents/simplon/MachineLearning/projet_indeed/df_pymongo_merged_with_companies.csv", encoding = 'utf8')

s = df['Salaires']
s.isnull().sum()
#13343 

#J'avais un problème avec l'accent et appostrophe dans 'niveau d'études' donc j'ai changé 
cols = list(df.columns)
print(cols[20])
cols[20] = 'Niveau etudes'

df.columns = cols
#Je garde que les colonnes utiles 
df = df[["Salaires","Experience","stage","cdi","cdd","freelance","alternance",
         "Bassin_emploi","Niveau etudes","langage","Seniority","Seniority_simplified","position",
         'python','java','javascript','c+','scala']]
#add in position !!!
#Je converti la colonne niveau d'étude en string pour pouvoir l'encoder
df['Niveau etudes'] = df['Niveau etudes'].astype(str)
#df = df.drop(df.index[8])#empty line
#df = df.drop(df.index[4])#empty line 
#df['Bassin_emploi'][9] = 'Paris' # Je remplace un 'ile de france' avec paris (reperé a la main)


######Pour remplir les nans de la colonne experience on va mettre la moyenne de chaque categorie "seniority"######
#Merci guillaume :p
#####FACULTATIVE PARCE QUE LE NOUVEAU DATASET EST DEJA TRAITÉ
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

#encoding the categorical data
df = pd.get_dummies(df)

#dropping empty columns
df = df.drop(["Niveau etudes_nan","Niveau etudes_8.0"], axis=1)
col_dict = {x: col for x, col in enumerate(df.columns)} 
df = df.drop(col_dict[32], 1) #seniority responsable région (only 1 value so drop it)

#on drop les nas 
dfnona = df.dropna()
#il reste 1059 lignes with chiffre and type
#2185 without
X = dfnona.iloc[:, 1:]
y = dfnona[["Salaires"]]


#split into train and test
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

#initialise the regressor
regressor = RandomForestRegressor(n_estimators=300, min_samples_split=2)
regressor.fit(X_train, y_train)

#predict
y_pred = regressor.predict(X_test)
pd.DataFrame(y_pred)

#on peut regarder les correlations (dunno if it's useful)
corr = X.corr()

###HOW TO EVALUATE DIS?
from sklearn import metrics

from sklearn.cross_validation import GridSearchCV
print(metrics.r2_score(y_test, y_pred))
print(metrics.mean_absolute_error(y_test, y_pred))
print(metrics.mean_squared_error(y_test, y_pred))
print(metrics.median_absolute_error(y_test, y_pred))
print(metrics.explained_variance_score(y_test, y_pred))

    
#predicting on all the dataset 
topred = df.iloc[:,1:]
topred.isnull().sum()
topred.fillna(0,inplace=True)

#create a list of predictions
salaire_forest = regressor.predict(topred)

#re import the dataset 
original = pd.read_csv("/Users/Celia/Documents/simplon/MachineLearning/projet_indeed/df_pymongo_merged_with_companies.csv", encoding = 'utf8')
#add the predictions
original['salaire_forest'] = salaire_forest

#export to csv
original.to_csv('df_pymongo_merged_preds.csv',encoding='utf8')
