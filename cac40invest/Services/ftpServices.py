#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 22:11:51 2022
Notre scripte ici consiste à transférer via la fonction FTP, 
des fichiers se trouvant sur unn serveur distant vers le serveur local
dans le dossier ../Fichiers txt du même racine que le projet.
Ces fichiers une fois téléchargés ils seront pretraités et déposés à nouveau 
sur le srveur distant
@author: djaffar
"""

from ftplib import FTP
import os


# Cette fonction permet de se connecter sur le serveur FTP distant
def ftpConnexion():
    # Se connecter sur le serveur distant
    ftp = FTP('ftp.cluster031.hosting.ovh.net')
    ftp.login('zulhfnp-djaffar', 'DjaCac40')
    ftp.encoding = "utf-8"
    etat = ftp.getwelcome()
    # Afficher un message de bien vévue du serveur
    print('Etat : ', etat)
    #print(ftp.dir())
    return ftp
'''
 Ici nous allons télécharger les fichiers txt du serveur distant
 pour le pré traitement
'''
def telechergerFichier():
    # Appele la fonction de connexion ftp
    ftp = ftpConnexion()
    # Se positionner au dossier contenant les documents à tranférer
    ftp.cwd('/Fichiers_TXT_traites/')
    
    # Recuperer les noms des fichiers du dossier courant
    filenames = ftp.nlst() # get filenames within the directory
    
    # Tranferer les tous les fichiers du dossier courant
    for filename in filenames:
        if filename.endswith('.txt'):
            localfile = f'{filename}'
            with  open("../Fichiers txt/"+localfile, 'wb') as file:
                ftp.retrbinary(f"RETR {localfile}", file.write)
    # Quiter le serveur FTP
    print("Fin de téléchargement ! ")
    ftp.quit()


'''
 Ici nous allons déposer les fichiers txt pré traités du serveur distant
'''
# Déposer les fichiers via FTP sur le serveur distant

# Appele la fonction de connexion ftp
def deposerFichier():
    ftp = ftpConnexion()
    #ftp.mkd("DIR_TEST1")
    # Se positionner sur le dossier distant de destination
    ftp.cwd('/Fichiers_TXT_traites/')
    # affecte à path le chemin relatif contenant les fichiers txt à transférer
    path = "../Fichiers txt/"
    os.chdir(path)
    dossier = os.listdir()
    for fichier in dossier:
        # Vérifier s'il s'agit bien de fichiet txt
        if fichier.endswith('txt'):
            # Recupère le dossier et le nom de fichier
            filename = f"{path}{fichier}"
            fichier = open(filename, 'rb')
            ftp.storbinary('STOR %s'%os.path.basename(filename), fichier, 1024)
           
    print(ftp.dir())
    # Quiter le serveur FTP
    replay = ftp.quit()
    print("Fin de dépot distant ! ")
    print(replay+" ! ")
    
