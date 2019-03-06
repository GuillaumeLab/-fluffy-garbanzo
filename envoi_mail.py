# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:58:28 2019

@author: Hugh

Un algo qui prend notre adresse mail (sender), l'adresse de CEO Fievet
(recipient), et le dernier rapport (report), et envoie un e-mail avec report de
sender vers recipient.
"""

import yagmail
import keyring
import os
import datetime

def send_email(sender, recipient, report):
    today= datetime.datetime.today().strftime("%d/%m/%Y")
    
    body = """
    Monsieur Fievet,
    
    Veuillez trouver ci-joint votre dernier rapport concernant les offres d'emploi qui vous intéressent.
    
    Bien cordialement,
    
    Team Elephant
    """
    subject = "Dev & Data Job Market Analysis - " + today
    
    yag = yagmail.SMTP(sender,
                       keyring.get_password("yagmail", sender))
    
    yag.send(to=recipient,
             subject="Team Elephant vous souhaite un bon lundi !",
             contents=body,
             attachments=report)
    return