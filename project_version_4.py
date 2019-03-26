

# Importation des librairies
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

# Préparation de la visualisation
plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'

# Importation du dataframe
annonces = pd.read_csv('C:/Users/Administrateur/Documents/SIMPLONr/df_pymongo.csv',encoding='utf-8')

# Suppression de colonnes inutiles
annonces.drop(['index','estimated','linked','_id'], axis=1, inplace=True)

annonces = annonces.drop(annonces.index[8])#empty line
annonces = annonces.reset_index()

annonces = annonces[annonces["timestamp"].notna()]
annonces["timestamp"] = pd.to_datetime(annonces["timestamp"],infer_datetime_format=True)
annonces = annonces.reset_index()

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
        return 30*plus_remover(jobby[0]), unit_giver(jobby[1])
    
    return df["timestamp"] - df["Date"].apply(lambda x: time_diff(x[7:].split(" "))).apply(lambda x: pd.to_timedelta(x[0], unit=x[1]))

annonces["true_date"]=vraie_date(annonces)

# On passe les colonnes interessantes en minuscules pour faciliter les regex
annonces['Title'] = annonces['Title'].str.lower() 
annonces['Details'] = annonces['Details'].str.lower()



stri = ['internship','intership',"intern",'student','stage','permanent','full-time','cdi',"durée indeterminée",'contracts','contract','interim','short-term' ,"durée determinée", 'short term' ,'cdd''independent','interim','indépendant','independant',"freelance","freelancing"'student','alternance','apprentissage','professionnalisation','alternant']
stage = ['internship','intership',"intern",'student','stage']
cdi = ['permanent','full-time','cdi',"durée indeterminée"]
cdd = ['contracts','contract','interim','short-term' ,"durée determinée", 'short term' ,'cdd']
freelance = ['independent','interim','indépendant','independant',"freelance","freelancing"]
alternance = ['student','alternance','apprentissage','professionnalisation','alternant']


annonces["stage"]=annonces['Details'].str.extract("(" + "|".join(stage) +")")
annonces["stage"]=annonces["stage"].replace(stage,"1")
annonces["stage"]=annonces["stage"].fillna(0)
annonces["cdi"]=annonces['Details'].str.extract("(" + "|".join(cdi) +")")
annonces["cdi"]=annonces["cdi"].replace(cdi,"1")
annonces["cdi"]=annonces["cdi"].fillna(0)
annonces["cdd"]=annonces['Details'].str.extract("(" + "|".join(cdd) +")")
annonces["cdd"]=annonces["cdd"].replace(cdd,"1")
annonces["cdd"]=annonces["cdd"].fillna(0)
annonces["freelance"]=annonces['Details'].str.extract("(" + "|".join(freelance) +")")
annonces["freelance"]=annonces["freelance"].replace(freelance,"1")
annonces["freelance"]=annonces["freelance"].fillna(0)
annonces["alternance"]=annonces['Details'].str.extract("(" + "|".join(alternance) +")")
annonces["alternance"]=annonces["alternance"].replace(alternance,"1")
annonces["alternance"]=annonces["alternance"].fillna(0)


# Data preprocessing : Type de poste

# on déclare une liste de mots clés pour recherche le type de poste dans annonces
type_poste =["directeur","directrice","manager","vp","svp","president","pdg","director","cto","chief","general manager","evp","executive","responsable région","chef","membre","board","direction","head","graduate","junior"]
# on appelle str.extract qui va se charger de reconnaitre les items de la liste
annonces['Seniority'] = annonces['Title'].str.extract("(" + "|".join(type_poste) +")", expand=False)

executives =["chef",'cto','direction', 'executive','director',"manager",'directeur', 'head', 'chief','responsable région','vp']
junior =["junior",'graduate','stage','intern','internship','assistant','student']

annonces['Seniority_simplified']=annonces['Title'].str.extract("(" + "|".join(executives) +")", expand=False)
annonces['Seniority_simplified']=annonces['Seniority_simplified'].replace(executives,"executives")
annonces['Seniority_simplified'].loc[annonces['Seniority_simplified'].isnull()]=annonces['Title'].loc[annonces['Seniority_simplified'].isnull()].str.extract("(" + "|".join(junior) +")", expand=False)
annonces['Seniority_simplified']=annonces['Seniority_simplified'].replace(junior,"junior")

#Création de la variable des postes 

#Création des listes de postes analyste, scientist,bi,dev,architect
analyst = ["analyste","analyst","analytics","analyst","quantitative","quant","data","data base"]
scientist = ["scientist","sciences","science","scientifique","ia","artificielle","artificial","math","économiste","statisticien","doctorant","statistique","r&d","chercheur"]
Business_Intelligence = ["businessintelligence","business intelligence","bi","crm","consultant","erp"]
Developpeur = ["developpeur","devops","ingénieur","développeyur","software","développement","java","engineer","ingenieur","développeur","dev","codeur","intégrateur","integrateur"]
IT_architect = ["dba","sql","informatique","infrastructure","architect","architect","database","data base","base de donnée","base de données"]

#Création d'une colonne spécifique extractant info des titres basé sur les listes de postes
annonces["position"]=annonces['Title'].str.extract("(" + "|".join(analyst) +")")
annonces["position"]=annonces["position"].replace(analyst,"analyst")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Title'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(scientist) +")", expand=False)
annonces["position"]=annonces["position"].replace(scientist,"scientist")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Title'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(Business_Intelligence) +")", expand=False)
annonces["position"]=annonces["position"].replace(Business_Intelligence,"Business_Intelligence")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Title'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(Developpeur) +")", expand=False)
annonces["position"]=annonces["position"].replace(Developpeur,"Developpeur")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Title'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(IT_architect) +")", expand=False)
annonces["position"]=annonces["position"].replace(IT_architect,"IT_architect")

#recréation de nouvelles listes pour extraire info des details lorsque le titre était insuffisant. "bi" serait inadapté pour l'extraction dans la colonne details
analyst = ["analyste","analyst","analytics","analyst"]
scientist = ["scientist","scientifique","artificial","math","économiste","statisticien","doctorant","statistique"]
Business_Intelligence = ["businessintelligence","business intelligence","consultant"]
Developpeur = ["developpeur","devops","ingénieur","développeyur","chercheur","java","engineer","ingenieur","développeur","infrastructure","intégrateur","architect","integrateur"]

#Completion d'une colonne spécifique extractant info des details basés sur les nouvelles listes de postes
annonces["position"].loc[annonces["position"].isnull()]=annonces['Details'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(analyst) +")", expand=False)
annonces["position"]=annonces["position"].replace(analyst,"analyst")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Details'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(scientist) +")", expand=False)
annonces["position"]=annonces["position"].replace(scientist,"scientist")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Details'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(Business_Intelligence) +")", expand=False)
annonces["position"]=annonces["position"].replace(Business_Intelligence,"Business_Intelligence")
annonces["position"].loc[annonces["position"].isnull()]=annonces['Details'].loc[annonces["position"].isnull()].str.extract("(" + "|".join(Developpeur) +")", expand=False)
annonces["position"]=annonces["position"].replace(Developpeur,"Developpeur")

annonces["Title"].loc[annonces["position"].isnull()]

# Data preprocessing : Expérience

# Nouvelle colonne 'Experience' à partir de 'Details'
annonces['Experience'] = annonces['Details'] 

# On extrait les 'expériences' en 'expérience' selon différentes syntaxes possibles
annonces['Experience'] = annonces['Experience'].str.replace("expérience","experience").replace("expériences","experience").replace("d'expérience","experience").replace("d'expériences","experience").replace("experiences","experience")
annonces['Experience'] = annonces['Experience'].str.replace("several","2").replace("plusieurs","2").replace("plusieurs années","2").replace("several years","2")
annonces['Experience'] = annonces['Experience'].str.replace("customer experience","").replace("online experience","").replace("user experience","")

# On remplace les durées en lettres par des digits
annonces['Experience'] = annonces['Experience'].str.replace("une","1").replace("un","1").replace("one","1").replace("deux","2").replace("trois","3").replace("quatre","4").replace("cinq","5").replace("six","6").replace("sept","7").replace("huit","8").replace("neuf","9").replace("dix","10").replace("quinze","15")
annonces['Experience'] = annonces['Experience'].str.replace("two","2").replace("three","3").replace("four","4").replace("five","5").replace("six","6").replace("seven","7").replace("eight","8").replace("nine","9").replace("ten","10").replace("fifteen","15")

#  Regex pour prendre tous les digits avant 'year/years/ans/an ...'
tmp = annonces['Experience'].str.extractall("([0-9]+)(?=\s(an |ans |année |années |years |year |ans\r\n|années\r\n|année\r\n|an\r\n|year\r\n|years\r\n|ans,|année,|an,|années,|years,|year;|years;|ans;|an;|année;|années;|year.|years.|ans.|an.|année.|années.))")
tmp[0]=tmp[0].astype("float")
# On elimine les valeurs suppérieures à 10 (hypothèse : les employeurs ne prennent pas plus de 11 ans d'expérience)
tmp[0]=tmp[0].loc[tmp[0]<11]  
tmp=tmp.groupby(level=0).max() #on garde la valeur maximum ()
annonces['Experience'] = tmp.groupby(tmp.index.get_level_values(0)).agg(list) #on réinsere les groupes dans le dataframe
annonces['Experience']=annonces['Experience'].astype(str).str.replace('\[|\]|\'', '') #on enleve les crochets


#je créé une classe mid entre junior et senior 
annonces["Seniority_simplified"]=annonces["Seniority_simplified"].fillna("mid")
#je remplace les valeurs nulles de expérience par la valeur "executuve","junior","mid"
annonces["Experience"].loc[annonces["Experience"].isnull()]=annonces['Seniority_simplified'].loc[annonces["Experience"].isnull()]
#je remplace les valeurs nulles de junior par "0"
annonces["Experience"].loc[annonces["Experience"]=="junior"]=annonces["Experience"].loc[annonces["Experience"]=="junior"].str.replace("junior","0")
#je remplace les valeurs excutives et mid par des nan
annonces["Experience"]=annonces["Experience"].replace(r'executives|mid', np.nan, regex=True)
#je remets les string en floats
annonces["Experience"]=annonces["Experience"].astype(float)

#je remplace les valeurs manquantes de l'expérience par la moyenne des de l'XP par la seniority simplified
for i in annonces["Seniority_simplified"].unique():
    annonces["Experience"].loc[annonces["Seniority_simplified"]==i] = annonces["Experience"].fillna(annonces["Experience"].loc[annonces["Seniority_simplified"]==i].mean())

#on converti les string en nan ou float
def replace(l):
    """Cette fonction prends en paramètres une liste ou series qui est composé de strings (soit 'nan' ou un nombre ex. '5.0')
    il retourne une liste avec soit des nans ou des floats
    on peut ajouter ensuite cette liste à notre dataframe"""
    l2 = [0 for x in range(len(l))]
    for i in range(len(l)):
        elt = l[i]
        if elt == 'nan':
            l2[i] = np.nan
        else:
            l2[i] = float(elt)
    return l2
#on applique au dataset 
annonces['Experience'] = replace(annonces['Experience'])
#type(annonces['Experience'][2]) #pour verifier que la fonction a fonctionnée - doit retourner un nan 

# Fonction prem_exp - Une fonction qui peut aider à remplir la colonne "Experience".
# Entrées: pd.DataFrame df
# Actions: Rien
# Sorties: pd.Series temp - une series avec le même index que df, dont les valeurs sont 1 si la colonne "Details" de df
# contient "première" ou "first experience", ou 0 sinon.
def prem_exp(df):
    vrai = (df["Details"].str.contains("première", regex=True)) | (df["Details"].str.contains("first experience", regex=True))
    temp = pd.Series(np.nan, df.index)
    temp.loc[vrai] = 1
    return temp

annonces["prem_exp"] = prem_exp(annonces)
annonces["Experience"] = np.nanmax(annonces[["prem_exp", "Experience"]], axis=1)
annonces = annonces.drop(columns=["prem_exp"])



# Data preprocessing : Type de poste

# on déclare une liste de mots clés pour recherche le type de poste dans annonces
type_poste =["directeur","directrice","manager","vp","svp","president","pdg","director","cto","chief","general manager","evp","executive","responsable région","chef","membre","board","direction","head","graduate","junior"]
# on appelle str.extract qui va se charger de reconnaitre les items de la liste
annonces['Seniority'] = annonces['Title'].str.extract("(" + "|".join(type_poste) +")", expand=False)



# Data preprocessing : Contrats

# on cherche les contrats dans ces colonnes avec une regex
# et on remplit une liste de contrats pour chaque annonce

def type_de_contrat(df):
    liste_contrats = []
    regex = r'(?:independent|contracts|contract|interim|internship|intership|permanent|short-term|short term|full-time|part-time|part time|full time|student|student job|student jobs|cdi|cdd|stage|alternance|apprentissage|professionnalisation|freelance|indépendant|independant)'
    for i in range(len(df)):
        l = re.findall(regex,str(df['Title' and 'Details'][i]))
        l = list(set(l))
        liste_contrats.append(l)
    return(liste_contrats)

# on appelle la fonction qui extrait les contrats
c = type_de_contrat(annonces)
# on remplit une colonne 'Contrat' au propre dans le dataframe
c = np.array(c)
annonces["Contrat"] = c

# Data preprocessing : Salaires

# On nettoie les salaires et on remplace les valeurs vides par des nan
def cleansal(liste):
    for i in range(len(liste)):
        if len(liste[i])==0:
            liste[i] = np.nan
        else:
            liste[i] = liste[i][0]
    return liste

def trouver_salaires(df, colonne):
# on trouve des salaires dans 'colonne' et dans le dataframe entrés en paramètres
# 'colonne' doit etre une string sur laquelle on applique la regex
# on renvoie une liste 
    s = []
    regex = r'((?:Rémunération|Gratification|Salaire|Salary)?\s?:?\s?[0-9]*(?:.|,)[0-9]*(?:.|,)[0-9]*€?\s(?:(?:to|-|à)?\s?[0-9]*(?:.|,)[0-9]*(?:.|,)[0-9]*€?\s)?\s?(?:\/|par|per)\s?(?:mois|an|year|month) )'
    for i in range(len(df)):
        l = re.findall(regex,str(df[colonne][i]))
        s.append(l)
    s = cleansal(s) #on nettoie avec la fonction cleansal 
    return(s)
    
def intify_etc(sals):
    """ sals : liste de salaires en forme de string
    cette fonction convertie toutes les phrases en int's: 
    remplace les salaires avec une moyenne si c'est une fourchette
    et avec une moyenne transformé en annuel s'il sagit d'une salaire par mois
    retourne une liste nettoyée, prête à être ajoutée au dataframe :)) 
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
                    try:
                        sal = re.findall(regex,sals[i])[0]
                        sal=sal.replace(' ','')#get rid of space
                        sals[i] = int(sal)#convert to int
                    except:
                        print("WARNING "+str(sals[i]))
                        sals[i]=np.nan
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
                    try:
                        sal = re.findall(regex,sals[i])[0]
                        sal=sal.replace(' ','')#get rid of space
                        sals[i] = int(sal)*12#convert to yearly salary
                    except:
                        print("WARNING "+str(sals[i]))
                        sals[i]=np.nan
                    #print('not fourchette')
        elif type(sals[i]) == str:
            sals[i] = np.nan
    return sals

# on extrait les salaires 
s = intify_etc(trouver_salaires(annonces, 'Title'))
# on les ajoute dans une nouvelle colonne
annonces['Salaires'] = s


# Data preprocessing : Niveau d'études

# ajouter une colonne niveau_etude

def niveau_etudes(df):
    # z est la regex pour extraire Bac+.., bac +..., Master
    # qu'on va chercher dans la colonne Details
    etude=[]
    z = re.compile(r'bac ?\+ ?\d?\/?\d?|master')
    
    for i in range(len(df)):
        bac = re.findall(z,str(df['Details'][i]))
        bac = list(set(bac))
        etude.append(bac)
    return(etude)

# on appelle la fonction qui traite le niveau d'études
annonces["Niveau d'études"] = niveau_etudes(annonces)
# on clean la colonne niveau d'étude
annonces["Niveau d'études"]=annonces["Niveau d'études"].astype(str).str.replace("master","5").replace("bac","").replace("+","")
listetude = ["1","2","3","4","5","6","7","8"]

multi_index_study = annonces["Niveau d'études"].astype(str).str.extractall("(" + "|".join(listetude) +")")
annonces["Niveau d'études"]=multi_index_study.groupby(level=0).max()



# Data preprocessing : Location

# le code ci-dessous permet de déterminer le bassin d'emploi en se basant sur le mot clé recherché
annonces['Bassin_emploi'] = annonces['Location'] #création de la colonne bassin d'emploi
# extraction de mot clé utilisé pour la recherche
annonces['Bassin_emploi'] = annonces['url'].str.extract("(?<=&l=)(.*)(?=&start)", expand=False)
# reformater île de France 
annonces['Bassin_emploi'] = annonces['Bassin_emploi'].replace("%C3%AEle%20de%20france","île de france")

# le code permet une nouvelle variable appellée inner_city
annonces['Location'] = annonces['Location'].str.lower()#reformater la colonne location en minuscule 
Inner_City = ["75","bordeaux","paris","nantes","toulouse","lyon"]#definir liste de valeur qui sont théoriquement dans la ville même
annonces['Inner_City'] = annonces['Location'].str.extract("(" + "|".join(Inner_City) +")", expand=False) #extrait les valeurs en centre villes 
annonces['Inner_City'] = annonces['Inner_City'].replace(Inner_City,"Inner_City")#remplace les valeurs en centre villes
annonces['Inner_City'] = annonces['Inner_City'].notnull()
annonces['Inner_City'] *= 1

# Cette fonction permet de detecter la langue de l'offre (fr, not fr)

from langdetect import detect # import langdetect

def try_detect(cell):# fonction pour detecter la langue
    try:
        detected_lang = detect(cell)
    except:
        detected_lang = None 
    return detected_lang

# ça a pris 3 minutes pour 7000 lignes
annonces['langage'] = annonces["Details"].apply(try_detect) # applique la fonction 
annonces['langage'].loc[annonces['langage']=="fr"].count()  #nombre d'offre en français

#binarize en fr et non fr
annonces['langage'] = annonces['langage'].loc[annonces['langage']=="fr"] 
annonces['langage'] = annonces['langage'].notnull()
annonces['langage'] *= 1

# Data preprocessing : Compétences 

# on extrait les compétences spécifiques avec une regex
def langages_pro(df):
    # on cherche dans la colonne 'Details'
    langage=[]
    regex = r'(?: r |python|sql|nosql|mysql|matlab|c\+\+?|scala|ruby|php|vba|machine learning|ml|javascript|java|hadoop|spark|mongodb\
              |cassandra|nlp|maths|statistics|statistique|physics|physique|tableau|power-bi|powerbi|power bi|qlikview|sci-kit|scikit|keras|tensorflow|pytorch|deep learning|pandas|numpy|excel |powerpoint|kpi|dashboard|qlikview|sas|spss|api|nlp|physics|sk learn|ggplot2\
              hbase|mongodb|cassandra|hbase|rstudio|ElasticSearch|neo4j|kibana|d3|Zeppelin|graffana|Rshiny|shiny|Jupyter|Tableau|Qlik|Spotfire|dataiku|StackOverflow|JIRA|Bitbucket|Confluence|Bamboo|Github|GitLab|Jenkins|Ansible|Scrum|Kanban)'
    
    for i in range(0, len(df)):
        L = re.findall(regex,str(df['Details'][i]))
        L = list(set(L))
        langage.append(L)
    return(langage)

annonces["Langages"] = langages_pro(annonces)

#On transforme les skills (appellées ici langage) en one hot encoded 
annonces['Langages']=annonces['Langages'].astype(str).str.replace('\[|\]|\'', '')
annonces['Langages']=annonces['Langages'].str.replace(' ', '')
annonces= pd.concat([annonces, annonces.Langages.str.get_dummies(sep=',')], axis=1)

annonces.to_csv('df_pymongo_new.csv', index=False, header=True)
# Correction des salaires outliers (à partir de 200000€ / an) on divise par 12
mask = annonces['Salaires'] >= 200000
m = annonces[mask]
print(m)
for i in m.index.values:
    annonces['Salaires'][i] = int(annonces['Salaires'][i]/12)

# on plot les salaires
plt.scatter(annonces.index.values,annonces['Salaires'],color='r')
plt.title('Salaire (€ brut/an) ')
plt.xlabel('index')
plt.ylabel('Salaire')
plt.show()



# enlever crochets dans les colonnes
annonces['Contrat']=annonces['Contrat'].astype(str).str.replace('\[|\]|\'', '')
annonces["Niveau d'études"]=annonces["Niveau d'études"].astype(str).str.replace('\[|\]|\'', '')   
annonces['Langages']=annonces['Langages'].astype(str).str.replace('\[|\]|\'', '')
