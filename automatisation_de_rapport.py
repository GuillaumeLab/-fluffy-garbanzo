# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:41:07 2019
Updated on Tue Mar 12 12:15:00 2019

@author: Hugh - Team Elephant

Un programme pour écrire et produire les rapports automatisés vers les fichiers HTML
et PDF, puis les envoyer vers le recipient désiré.
Fonctions:  auto_prod_graphes, ecrit_html, ecrit_pdf, send_email.
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import yagmail
import keyring
import os
import datetime

# pd.DataFrame défaut: changeable
df = pd.read_csv("Position_Salaries.csv")

# Fonction: auto_prod_graphes
# Entrées:  pd.DataFrame df (de la BDD d'annonces);
#           String suffix (fin des noms de fichier pour les graphes).
# Actions:  Crée des figures en format .png pour chaque graphe nécessaire.
# Sortie:   Noms des fichiers des graphes en type 'list'
def auto_prod_graphes(df, suffix):
    
    graphs = []
    fig, ax = plt.subplots()
    ax = sns.barplot(df["Position"], df["Salary"])
    graphs.append("bar1-{}.png".format(suffix))
    fig.savefig("bar1-{}.png".format(suffix))
    graphs.append("bar2-{}.png".format(suffix))
    fig.savefig("bar2-{}.png".format(suffix))

    
    return graphs

# Fonction: ecrit_html
# Entrées:  String suffix (fin des noms de fichier pour les graphes).
# Actions:  Crée un fichier "Job_Market_Analysis_[suffix].html" pour le
#           rapport avec les graphes désirés.
# Sortie:   Nom de fichier du rapport HTML.
def ecrit_html(suffix):
    
    # Le code HTML doit avoir la forme du rapport voulu.
    html = """
    <!DOCTYPE html>
    <head>
    <title>A title of joy</title>
    </head>
    <body>
    <br><br><br>-----------------------<br><br><br>
    A body of joy... Here comes the science: <br/>
        
    <img src="bar1-{0}.png" alt="salary_graph">
    
    <br><br>
    
    <img src="bar2-{0}.png" alt="salary_graph">
    </body>
    """.format(suffix)
    
    # Nom du fichier = "Job_Market_Analysis_[date].html"
    file_name = "Job_Market_Analysis_{}.html".format(suffix)
    f = open("Job_Market_Analysis_{}.html".format(suffix),"w")
    f.write(html)
    f.close()
    
    return file_name

# Fonction: ecrit_pdf
# Entrées:  String suffix (fin des noms de fichier pour les graphes).
# Actions:  Crée un fichier "Job_Market_Analysis_[suffix].pdf" pour le
#           rapport avec les graphes désirés.
# Sortie:   Nom de fichier du rapport PDF.
def ecrit_pdf(suffix):
    
    # Le code LaTeX doit avoir la forme du rapport voulu.
    latex = """
    \\documentclass[]{article}
    
    \\addtolength{\\oddsidemargin}{-0.75in}
    \\addtolength{\\textwidth}{1.5in}
    \\addtolength{\\topmargin}{-0.75in}
    \\addtolength{\\textheight}{1.5in}
    
    \\usepackage{amsfonts}
    \\usepackage{amsmath}
    \\usepackage{amsthm}
    \\usepackage{txfonts} \\usepackage{pxfonts}
    \\usepackage{graphicx}
    
    \\title{This is a Test Heckle}
    \\author{Team Elephant in the Living Room}
    
    \\begin{document}
    
    \\maketitle
    
    \\begin{abstract}
    We're going to do some crazy shit!
    \\end{abstract}
    
    \\section{The Science}
    
    Look at this science!
    \\includegraphics{barplot1.png}
    
    \\end{document}
    """

    # Nom du fichier = "Job_Market_Analysis_[date].tex"
    g = open("Job_Market_Analysis_{}.tex".format(suffix),"w")
    g.write(latex)
    g.close()

    # Crée "Job_Market_Analysis_[date].pdf"
    os.system("pdflatex Job_Market_Analysis_{}.tex".format(suffix))
    
    return "Job_Market_Analysis_{}.pdf".format(suffix)

# Fonction: send_email
# Entrées:  String send_address, String recipient, String rec_address
#           *String attached
# Actions:  Envoie de l'adresse "send_address" de Team Elephant à l'adresse
#           gmail "rec_address" de "recipient" (le nom auquel le mail est 
#           adressé), avec les pièces jointes (facultatives).
# Sortie:   Rien
def send_email(send_address, recipient, rec_address, graphs, html, pdf):
    today= datetime.datetime.today().strftime("%d/%m/%Y")
    
    body = """
    {},
    
    Veuillez trouver ci-joint votre dernier rapport concernant les offres d'emploi qui vous intéressent.
    
    Bien cordialement,
    
    Team Elephant
    """.format(recipient) # Texte du mail
    
    subject = "Dev & Data Job Market Analysis - " + today
    
    attachments = graphs + [html, pdf]
    
    # Keyring doit contenir le mot de passe
    yag = yagmail.SMTP(send_address,
                       keyring.get_password("yagmail", send_address))
    
    yag.send(to=rec_address,
             subject=subject,
             contents=body,
             attachments=attachments)
    return

# Toutes les fonctions ensemble
# Fonction: everything
# Entrées:  pd.DataFrame df, String send_address, String recipient,
#           String rec_address, String suffix
# Action:   Prend le dataframe df des données, crée les graphes pertinents,
#           crée le rapport avec les graphes en formats HTML et PDF, et
#           envoie les résultats (tous avec la même suffixe) à rec_address
#           (l'adresse de recipient).
# Sortie:   Rien
# Défauts donnés avant...
send_address = "team.elephant.in.the.room@gmail.com"
rec_address = "team.elephant.in.the.room@gmail.com"
recipient = "Monsieur Fievet"
suffix = datetime.datetime.today().strftime("%d-%m-%Y")
def everything(df=df, send_address=send_address, recipient=recipient,
               rec_address=rec_address, suffix=suffix):
    
    send_email(send_address, recipient, rec_address,
               auto_prod_graphes(df, suffix), ecrit_html(suffix),
               ecrit_pdf(suffix))
    
    return