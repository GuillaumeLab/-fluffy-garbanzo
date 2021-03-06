import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import datetime
from matplotlib import pyplot
#plt.figure(1,figsize=(10,10))

sns.set_style("whitegrid", {'axes.grid' : False})

annonces = pd.read_csv("df_pymongo_merged_preds.csv")


sns.set(style="darkgrid")
import seaborn as sns

#on plot la répartition des contrats 
cols = ["stage", "cdi", "cdd", "alternance", "freelance"]
results_set = [annonces["Details"].loc[annonces[col]==1].count() for col in cols]
df = pd.DataFrame({'results_set': results_set}, index=cols)
ax=df.plot.bar(rot=90,figsize = (15, 15))
ax.set_title('Nombre de contrat parmis les offres relevées')
fig = ax.get_figure()   
fig.savefig('contract_count.pdf',bbox_inches='tight', transparent=True, pad_inches=0)


#plot les salaires banlieu vs centre ville
annonces.groupby(['Inner_City',"Bassin_emploi"]).mean()['Salaires'].unstack().plot(kind="bar",title="les salaires selon la localité centre villes vs banlieu")
plt.rcParams['figure.figsize'] = (15,15)
plt.savefig('salaires_banlieu_villes.pdf')
#plot les salaires selon la ville et la seniorité
annonces.groupby(['Seniority_simplified',"Bassin_emploi"]).mean()['Salaires'].unstack().plot(kind="bar",title="les salaires selon la seniorité et la ville")
plt.rcParams['figure.figsize'] = (15,15)
plt.savefig('salaires_selon_villesetseniority.pdf',bbox_inches='tight', transparent=True, pad_inches=0)

#plot les salaires selon la ville et le rôle
annonces.groupby(['position',"Bassin_emploi"]).mean()['Salaires'].unstack().plot(kind="bar",title="les salaires selon la ville et le rôle")
plt.rcParams['figure.figsize'] = (15,15)
plt.savefig('salaires_selon_villesetrele.pdf',bbox_inches='tight', transparent=True, pad_inches=0)

#vertical
f, (ax3, ax4,ax6) = plt.subplots(3,figsize=(15,15))
sns.set(style="darkgrid")
ax3 =sns.countplot(ax=ax3,x="Bassin_emploi", hue="Niveau d'études", data=annonces)
ax3.set_title('niveau etude')
ax4 = sns.countplot(ax=ax4,x="position", data=annonces)
ax4.set_title('nombre de poste selon le rôle')
ax6 = sns.countplot(ax=ax6,x="Bassin_emploi", hue="position", data=annonces)
ax6.set_title('nombre de poste selon le rôle et la ville')#Paris has a lot more of analysts
f.savefig('vertical_subplots.pdf',bbox_inches='tight', transparent=True, pad_inches=0)

#Or horizontale
fig, axs = plt.subplots(ncols=3,figsize=(15,15))
sns.countplot(x='Bassin_emploi', hue="Niveau d'études", data=annonces, ax=axs[0])
sns.countplot(x='position', data=annonces, ax=axs[1])
sns.countplot(x='Bassin_emploi', hue='position', data=annonces, ax=axs[2])
plt.savefig('Bassin_emploi_etudes.pdf',bbox_inches='tight', transparent=True, pad_inches=0)

annonces.groupby(['true_date',"position"]).count()['Details'].unstack().plot(title="Number of offer per role")
plt.rcParams['figure.figsize'] = (15, 15)
plt.savefig('offer_position.pdf')
annonces.groupby(['true_date',"Bassin_emploi"]).count()['Details'].unstack().plot(title="Number of offer per city")
plt.rcParams['figure.figsize'] = (15,15)
plt.savefig('offer_city.pdf',bbox_inches='tight', transparent=True, pad_inches=0)

#plot sur les compétences

languages2 = [" r ","power query","unix","linux","json","golang","golearn","deap ","maple","julia","python","sql","nosql","git ","matlab","c\+\+?","scala","ruby","php","vba","javascript","java ","d3","sci-kit","scikit","keras","tensorflow","pytorch","pandas","numpy"," excel ","powerpoint","plotly","dash ","sas","spss","sk learn","ggplot2","rshiny","shiny","jupyter","networkx","selenium","beautifulsoup","rstudio","auto ml","c\+","tpot","sas","perl"] 
              
Big_data_providers = ["cloudera","aws","amazon","impala","dataiku","Zeppelin","graffana","tableau","qlik","spotfire","jira","confluence","bamboo","jenkins","ansible","tableau","power-bi","powerbi","power bi","qlikview","bigstep","denodo","informatica","azure","koverse","oracle","sap","platfora","zaloni","collibra","alation","mapr"," dataiku ","podium data","zeenea","ecl","flare","google visualization","tamr","saagie","zoomdata","looker","jethro","datameer","atscale","teradata","presto","vectorh","bigsql","Datanami","Dremio","olap cube","alteryx","birst","datawatch","domo","gooddata","looker","pyramidAnalytics","zoomdata","datawrapper","dwaas","redshift","bedrock","blazingdb ","druid","clickHouse","google big query","oryx","h20","photon ml","prediction.io","seldon","shogun","weka","algorithmia","algorithms.io","amazon ml","bigml"," dataRobot","fico","google prediction","haven ondemand","watson","plyrmr","mathmorks","beyondcore","bime","clearstory"," domo ","gooddata","inetsoft","infocaptor"," logi analytics","microstrategy","rpognoz"," qlik sense"," lumira","kafka","esri ","sisense","spotfire","thoughtspot","yellowfin","databricks","auto-model","datarobot","machine learning studio","purepredictive","predicsis","yottamine","ibm db2","infoworks","heka ","logstash ","kestrel","flume ","flink ","nfs","insightedge","streamanalytix","streamlio","streamsets","streamtools","talend","infoworks","insightedge","kx data","lightBend","heron"] 

Big_data_opensource= ["ubuntu","hive","spark","mongodb","apache", "mapreduce", "hadoop", "hdfs","cassandra", "hbase","ElasticSearch","neo4j", "mysql","github","gitlab","bitbucket","kibana", "ngrox", "StackOverflow","hortonworks","HBase", "couchdb", "postgres", "mammothdb","mariadb"] 

domain = ["dashboard"," de bord","data lake","datalake","back-end","front-end"," api","etl","data warehouse","statistics","statistique","physics","physique","predict","reporting","bigstep","réseaux de neurones","full stack"," governance"," Reporting","kpi"," Scripting"," unittest","testing","version control","Algorithmie","chatbots","chatbot"," scraping","scrapping","webscraping","wescrap","webscrapping","graph database","maths"," nlp"," machine learning","ml","deep learning"," Scrum","Kanban","agile"] 

Cloud_providers = ["containers","saas","paas","iaas","baas","datacenter","virtuozzo","tsuru ","kubernetes","activestate","apprenda","centurylink","cloudbees ","platform9 ","cloudify","atomia"," cisco"," metapod","cloudstack"," nutanix","openstack","omnistack"," vmware","zerostack","sddc ","avinetworks ","hyperscale ","dynatrace ","tibco","cloudyn ","engine yards","monitis ","xplenty","talend","moskitos","maestrano","azuqua","apppoint","adeptia","elastic.io","google cloud"," gridgrain","heroku","ibm bluemix","profitbricks","dokku","nginx "," deis","coreos"," ceph","docker","softlayer","digitalocean","joyent","linode"," rackspace","coreos","amazon web services","rancheros","snappy"," RedHat","mesosphere dcos","vmware","containers","openvz ","hypervisor","virtual machines","chroot","vmare","esxcitrix","xenserver","salesforce"] 

#plot de l'occurence et du salaire des langages
cols =[]
for i in languages2:
    if i in annonces.columns:
        cols.append(i)
        cols=list(set(cols))


#results_set1 = annonces.loc[annonces["position"]=="scientist"] #on choisi ici le type de rôle recherché 
results_set1 = annonces  #où on prend tous les rôles 
occurence = [results_set1["Details"].loc[results_set1[col]==1].count() for col in cols]
Salaires = [results_set1["Salaires"].loc[results_set1[col]==1].mean() for col in cols]
df1= pd.DataFrame({'occurence':occurence,'Salaires': Salaires,'skills': cols},index=cols)
df1 = df1.sort_values(by=['occurence']).tail(20)
ax3 = df1.plot.bar(rot=90,secondary_y="Salaires",figsize = (15, 15))
ax3.set_title('occurence et du salaire des langages')
fig = ax3.get_figure()   
fig.savefig('skills_count.pdf',bbox_inches='tight', transparent=True, pad_inches=0)



##plot de l'occurence et du salaire des compétences généralistes
cols =[]
for i in languages2:
    if i in annonces.columns:
        cols.append(i)
        cols=list(set(cols))


#results_set1 = annonces.loc[annonces["position"]=="analyst"] #on choisi ici le type de rôle recherché 
results_set1 = annonces  #où on prend tous les rôles 
occurence = [results_set1["Details"].loc[results_set1[col]==1].count() for col in cols]
Salaires = [results_set1["Salaires"].loc[results_set1[col]==1].mean() for col in cols]
df1= pd.DataFrame({'occurence':occurence,'Salaires': Salaires,'skills': cols},index=cols)
df1 = df1.sort_values(by=['occurence']).tail(20)
ax3 = df1.plot.bar(rot=90,secondary_y="Salaires",figsize = (15, 15))
ax3.set_title('l'occurence et du salaire des compétences généralistes')
fig = ax3.get_figure()   
fig.savefig('skills_salary.pdf',bbox_inches='tight', transparent=True, pad_inches=0)
