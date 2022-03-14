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

mots = set(line.strip() for line in open('../Modele/dictionnaire.txt'))


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
    
    for el in docTokenize:
        elements += el + ' '
        
    return elements
   
        
# Affecte le document à nettoyer dans lst 

#Recupère le document mot par mot
def recuperDocMotParMot(liste):
    liste_des_mots = []
    for l in liste:
        liste_des_mots.append(l.strip())
        
    liste.close()
    return liste_des_mots 


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
        fichier = (open(fichier_du_dossier, "r", encoding="UTF-8")) 
        lst = recuperDocMotParMot(fichier)
        french_text = pd.DataFrame(lst, columns =['text'])
        french_preprocess_list = French_Preprocess_listofSentence(french_text['text'])
        print("************************************************************************\n")
        print('Voici le document de base : '+docNettoye(lst))
        print("\n")
        print("************************************************************************\n")
        print("\n")
        print('Voici le document nettoyée : '+docNettoye(french_preprocess_list))
        print("\n")
