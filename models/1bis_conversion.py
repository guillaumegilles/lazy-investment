#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Script python permettant de r�cuperer des fichiers pdf contenus dans un dossier
#Pour ensuite extraire uniquement les textes (sans tableau et sans image) dans un document texte
#Le  fichier texte est ensuite plac� dans un r�pertoire destination
#Pour chaque fichier l'ann�e, le nom de l'entreprise et le nombre de mots est renseign� dans le fichier liste_enterprise.txt (pour pouvoir comparer les diff�rentes ann�es)
#Pour chaque fichier les informations sont ins�rer dans une table MYSQL
import os
import fonction as fn
import time
import datetime
'''import mysql.connector'''
import html2text
var_html = html2text.HTML2Text()
var_html.ignore_links = True
"""
connexion = mysql.connector.connect(host='146.59.209.152',
                             user='zulhfnptrimbuj',
                             password='JaJa1503',                             
                             database='cac40',
                            )"""
liste_mots=[]
#A COMPLETER  : liste de mots contenu dans les fichiers textes lors de l'export � supprimer lors de l'export dans le fichier texte de destination
mots_a_retirer=['�','*','','o','(cid:1)','(cid:2)','(cid:132)','(cid:129)','(i)','(ii)','(iii)','(iv)','I','II','III','IV','V']
balise_a_retirer=['writing-mode:lr-tb;','textbox']
mot_positif=['bénéfice', 'bénéfices','Bénéfices','Bénéfice',]
nb_fichiers_traites=0
#path_source_pdf="C:/Users/trimbuj/Desktop/MASTER MIAGE/Projet de conception/Rapports Annuels CAC40"
#path_destination_txt="C:/Users/trimbuj/Desktop/MASTER MIAGE/Projet de conception/test/";
path_source_pdf="http://trimbtech.fr/CAC40_lazy_price/Fichiers_PDF/"
path_destination_txt="http://trimbtech.fr/CAC40_lazy_price/Fichiers_TXT/"



if os.path.exists(path_destination_txt+'liste_entreprise.txt'):
    os.remove(path_destination_txt+"liste_entreprise.txt")
#file = open("http://trimbtech.fr/CAC40_lazy_price/Fichiers_TXT/liste_entreprise.txt", "w+",encoding="utf-8")  
for path1, subdirs1, files1 in os.walk(path_source_pdf):
    nb_fichier_total=len(os.listdir(path_source_pdf))
    for name1 in files1:
        start=time.time()
        chemin_complet=(os.path.join(path1,name1))
        f_txt1= os.path.basename(chemin_complet)
        f_txt1=(f_txt1.split("."))
        nom_fichier1=f_txt1[0]
        annee_fichier1=nom_fichier1[:4]
        libelle_entreprise1=nom_fichier1[5:]
        texte_converti=fn.convert_pdf(chemin_complet, "html", "utf-8", "")
        file = open(path_destination_txt+nom_fichier1+".txt","w+", encoding="utf-8")
        texte_converti=texte_converti.decode('utf-8')
        file.write((texte_converti))
        file.close
        #fin conversion du fichier pdf en txt
        benef=0
        texte=""
        compteur=0
        # on ouvre � nouveau le fichier texte pour supprimer les mots � enlever
        file2 = open(path_destination_txt+nom_fichier1+".txt","r+", encoding="utf-8")
        for line in file2:
            
            
            nb_dans_chaine=0
            
            liste_mots=line.split()
            for mots in liste_mots:
                    if(len(mots)<2):#on ne compte pas les espaces et les mots � une lettre
                        compteur=compteur-1
                    if(mots in mots_a_retirer):#on supprime les mots contenus dans la listes des mots � retirer
                        liste_mots.remove(mots)
                        line=line.replace(mots,'')
                    if(mots.isdigit()):
                        nb_dans_chaine=nb_dans_chaine+1
                    if(mots in balise_a_retirer):
                        line=line.replace(mots,'')
                    if(mots in mot_positif):
                        benef=benef+1
            line=var_html.handle(line) # on eneleve les balises html du texte
            liste_mots=line.split()
            if(nb_dans_chaine<4) and (((len(liste_mots))>5) and (len(liste_mots)!=0)):#seul les phrases de plus de 5 mots sont conserv�s (pour �viter les tableaux):         
                compteur=compteur+len(liste_mots)
                texte=texte+line.lstrip()
                  
        file2.close
        file2 = open(path_destination_txt+nom_fichier1+".txt","w+", encoding="utf-8")
        file2.write(texte) #on r��crit dans le fichier texte le texte propre sans tableau, sans image et mots sp�ciaux
        file2.close
        

        nb_fichiers_traites=nb_fichiers_traites+1         
        end=time.time()
        temps_traitement=end-start
        file2 = open(path_destination_txt+"liste_entreprise.txt","a+", encoding="utf-8")
        file2.write(nom_fichier1+" "+str(compteur)+"\n")
        file2.close
        
        date_extraction = datetime.datetime.now()
        date_extraction=(date_extraction.strftime("%Y/%m/%d %H:%M:%S"))
        print("Fin de traitement du fichier "+nom_fichier1+"("+str(round(temps_traitement,2))+" secondes). Le fichier comporte "+str(compteur)+" mots.("+str(nb_fichiers_traites)+"/"+str(nb_fichier_total)+" fichiers traités)")
"""request = "INSERT INTO CAC (Nom_fichier_PDF,Nom_Entreprise,Annee_Fichier,Date_Execution,Temps_Execution,Nombre_Mots,Mot_Positif,Chiffre_Affaire) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        parametre=(nom_fichier1,libelle_entreprise1,annee_fichier1,date_extraction,round(temps_traitement,2),compteur,benef,0)
        curseur = connexion.cursor()
        curseur.execute(request,parametre)
        connexion.commit()
        curseur.close()
"""
