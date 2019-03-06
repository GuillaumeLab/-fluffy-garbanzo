import pandas as pd
dataframe3 = pd.read_csv('C:/Users/Administrateur/Documents/SIMPLONr/ml/annonces.csv', sep=',', encoding='utf-8' )
dataframe3 = dataframe3.loc[~dataframe3.Details.duplicated()]
len(dataframe3)
