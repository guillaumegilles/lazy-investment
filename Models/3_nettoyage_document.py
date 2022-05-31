#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 12:04:32 2022
Ce scripte consiste à nettoyer  le document text. 
Il s'agit de tokennizer les sentence, mettre tous les mots en miniscule
lemmatizer, enlver les mots n'apportant pas de sens dans le document, supprimer les ponctuations etc..'
@author: djaffar
"""
  # Importe les librairies
#from connexionDatabase import parcourrir
import connexionDatabase as service
import ftpServices as ftpjob
import os
import spacy
from spacy_lefff import LefffLemmatizer, POSTagger
from spacy.language import Language


import pandas as pd
  
import nltk
import string

@Language.factory('french_lemmatizer')
def create_french_lemmatizer(nlp, name):
    return LefffLemmatizer(after_melt=True, default=True)

@Language.factory('melt_tagger')  
def create_melt_tagger(nlp, name):
    return POSTagger()
 

nlp = spacy.load('fr_core_news_sm')
nlp.add_pipe('melt_tagger', after='parser')
nlp.add_pipe('french_lemmatizer', after='melt_tagger')


nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

# Initialise 
french_stopwords = nltk.corpus.stopwords.words('french')

mots = set(line.strip() for line in open('../Models/dictionnaire.txt'))


#mots = set(nltk.corpus.words.words())
#lemmatizer = WordNetLemmatizer()
#lemmatizer = FrenchLefffLemmatizer()

def French_Preprocess_listofSentence(listofSentence):
    preprocess_list = []
    for sentence in listofSentence :
         sentence_w_punct = "".join([i.lower() for i in sentence if i not in string.punctuation])
         sentence_w_num = ''.join(i for i in sentence_w_punct if not i.isdigit())
         tokenize_sentence = nltk.tokenize.word_tokenize(sentence_w_num)
         words_w_stopwords = [i for i in tokenize_sentence if i not in french_stopwords]
         sentence_clean = ' '.join(w for w in words_w_stopwords  if w.lower() in mots or not w.isalpha())
         sentence_clean_nlp = nlp(sentence_clean)
         lemmatizer_doc = ' '.join(d._.lefff_lemma for d in sentence_clean_nlp)  
         preprocess_list.append(lemmatizer_doc)
    
    return preprocess_list

# Parcourt le document nettoyé pour affichage intégral
def docNettoye(docTokenize):
    elements = " "
    
    for elem in docTokenize:
        elements += elem + ' '
        
    return elements
   
        
# Affecte le document à nettoyer dans lst 

#Recupère le document mot par mot
def recuperDocMotParMot(liste):
    liste_des_mots = []
    for l in liste:
        liste_des_mots.append(l.strip())
        
    liste.close()
    return liste_des_mots 

"""############# Transfert des fichiers par FTP  (Download) #####################
   Ici nous appellons la fonction telechergerFichier() par le bais de ftpjob
   la fonction télécharge tous les fichiers txt depuis le dossirs distant 
   /Fichiers_TXT_traites/ du serveur 'ftp.cluster031.hosting.ovh.net'
   vers le dossiers local ../Fichiers txt/ de la racine du projet

"""
ftpjob.telechergerFichier()

# Appelle la fonction connexion_bd pour charger le chemin relatif contenant les fichies à ouvrir
#chemin = "../"+connexion_bd()
chemin = "../"+service.parcourrir()

# Changer le repertoir
os.chdir(chemin)


lst = [] 
# Entre dans le dossier pour parcourir tous les fichiers
for fiche in os.listdir():
    
    # Vérifie si l'extention du fichier est .txt
    if fiche.endswith('.txt'):
        fichier_du_dossier = f'{chemin}{fiche}'
        fichier = (open(fichier_du_dossier, "r", encoding="iso-8859-1")) 
        lst = recuperDocMotParMot(fichier)
        fichier.close()
        french_text = pd.DataFrame(lst, columns =['text'])
        french_preprocess_list = French_Preprocess_listofSentence(french_text['text'])
        # Convertit   french_preprocess_list en string
        french_preprocess_list = ''.join(str(elem) for elem in   french_preprocess_list)
       
        # Ouvre à nouveau le fichier en écriture et y affecté le contenu pré raité
        fichier_net = open(fichier_du_dossier, "w", encoding="iso-8859-1")
        #for  ligne in french_preprocess_list:
        fichier_net.write(french_preprocess_list)
        fichier_net.close()
        #lst1 = recuperDocMotParMot(fichier_net)
        #french_text = pd.DataFrame(lst1, columns =['text'])
        #french_preprocess_list = French_Preprocess_listofSentence(french_text['text'])
        #fichier_net1 = ' '.join(fichier_net)
        #fichier_net.write(french_preprocess_list)
        #fichier_net.write(' '.join(french_preprocess_list))
        print("************************************************************************\n")
        print('Voici le document de base : '+docNettoye(lst))
        print("\n")
        print("************************************************************************\n")
        print("Filename : ",f'{fiche}')
        print("\n")
        #print('Voici le document nettoyée : '+docNettoye((fichier_net1)))
        #print(fichier_net)
        print('Voici le document nettoyée : '+docNettoye(french_preprocess_list))
        print("\n")


"""################ Transfert des fichiers par FTP  (Uplaoad) #####################
    Ici nous appellons la fonction deposerFichier() par le bais de ftpjob
    la fonction déverse tous les fichiers txt néttoyés depuis le dossier local ../Fichiers txt
    vers le dossiers distant  /Fichiers_TXT_traites/ du serveur 'ftp.cluster031.hosting.ovh.net'


"""
ftpjob.deposerFichier()
