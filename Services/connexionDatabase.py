

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 20:05:05 2022

@author: djaffar
"""
import ntpath
from datetime import date
import spacy
import mysql.connector as mc

nlp = spacy.load("fr_core_news_sm")


# Connecte  à la base de donées
def  connexion_bd():
    try:
        #connexion au base de données
        db = mc.connect(
              host='localhost',
              user = 'cac40',
              password = 'C@c40invest2022',
              database = 'cac40invest',
           )
        print("Connection réussie !")
        return db
        
    except mc.Error as err:
        # Rollback in case there is any error
          print(err)
          db.rollback()
          db.close()
    
        
# Parcourrir la table documents pour recupérer le premier chemin relatif Fichiers txt/
def parcourrir():
    # Appelle la fonction permettant la connexion à la base de données
    db = connexion_bd()
    #créer un curseur de base de données pour effectuer des opérations SQL
    curseur = db.cursor()
    #exécuter le curseur avec la méthode execute() et transmis la requête SQL
    sql = ("SELECT nomFichier, path FROM documents LIMIT 1")
    curseur.execute(sql)
    #récupèrer toutes les lignes de la dernière instruction exécutée.
    result = curseur.fetchall()
    liste = []
    for line in result:
        liste =  line[1]
    return liste
    db.close()
    curseur.close()

""" Cette partie est en cours de développement """
# Ajouter les informations d'un fichier dans la table documents 
def enregistrerFichier(document):
    # Enregistre les informations du fichier dans la base de données
    dir_path = "Fichiers txt/"
    file_path = "Fichiers txt/testo"
    nomFichier = ntpath.basename(file_path)
    # Appelle la fonction permettant la connexion à la base de données
    db = connexion_bd()
    #créer un curseur de base de données pour effectuer des opérations SQL
    curseur = db.cursor()
    infoFichier = (nomFichier, "Entreprise testo", date.fromisoformat('2015-01-28'), dir_path)
    #exécuter le curseur avec la méthode execute() et transmis la requête SQL
    sql = (" INSERT INTO documents(nomFichier, nomEntreprise, datePublication, path)  VALUES (%s, %s,%s, %s) ")
    curseur.execute(sql, infoFichier)
    db.commit()
    print("enregistrement effectué !")
    print(curseur.rowcount, " lignes insérées") 
    #fermeture de la connexion à la base de données
    db.close()
    curseur.close()
