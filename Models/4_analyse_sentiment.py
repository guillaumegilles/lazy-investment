# -*- coding: utf-8 -*-

from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import urllib.request
import datetime
import mysql.connector


def insertion_bdd(nom_fichier_complet, mot_positif,mot_neutre, mot_negatif):
    
    connexion= mysql.connector.connect(host='127.0.0.1',
                             port='3308',         
                             user='root',
                             passwd='',
                             database='cac40',
                             )
    nom_fichier=(str(nom_fichier_complet).split("."))
    nom_fichier=nom_fichier[0]
    annee_fichier=nom_fichier[:4]
    libelle_entreprise=nom_fichier[5:]
    date_extraction = datetime.datetime.now()
    date_extraction=(date_extraction.strftime("%Y/%m/%d %H:%M:%S"))
    #print("Fin de traitement du fichier "+nom_fichier1+"("+str(round(temps_traitement,2))+" secondes). Le fichier comporte "+str(compteur)+" mots.("+str(nb_fichiers_traites)+"/"+str(nb_fichier_total)+" fichiers traités)")
    request = "INSERT INTO cac40 (Nom_fichier_PDF,Nom_Entreprise,Annee_Fichier,Date_Execution,Nombre_Mots,Mots_Positif,Mots_Neutre,Mots_Negatif) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    parametre=(nom_fichier,libelle_entreprise,annee_fichier,date_extraction,0,mot_positif,mot_neutre,mot_negatif)
    curseur = connexion.cursor()
    curseur.execute(request,parametre)
    connexion.commit()
    curseur.close()
        
def analyse_sentiment(nom_fichier,texte): 
        phrases = sent_tokenize(texte_fin, language='french')
        df = pd.DataFrame({'phrases': phrases},index = list(range(1,len(phrases)+1)))
        sid = SentimentIntensityAnalyzer()
        df['sentiments_Vader'] = df['phrases'].apply(lambda x: sid.polarity_scores(x))
        df_new = pd.concat([df.drop(['sentiments_Vader'], axis=1), df['sentiments_Vader'].apply(pd.Series)], axis=1)
        df_new.columns = ['phrases', 'negative', 'neutre', 'positive', 'sentiment_score']
        df_new.sentiment_score.mean()
        #df_new.to_csv("C:/Users/trimbuj/Desktop/test.csv", index=False)    
        nb_phrase_negative=0
        nb_phrase_positive=0
        nb_phrase_neutre=0
        for i in df_new.index:
            if(df_new["sentiment_score"][i]<0):
                nb_phrase_negative=nb_phrase_negative+1
            else:
                if(df_new["sentiment_score"][i]>0):
                        nb_phrase_positive=nb_phrase_positive+1
                else:
                    nb_phrase_neutre=nb_phrase_neutre+1
        print("Nombre de phrase positive : "+str((nb_phrase_positive)))
        print("Nombre de phrase négative : "+str(nb_phrase_negative))
        print("Nombre de phrase neutre : "+str(nb_phrase_neutre))
        insertion_bdd(nom_fichier,nb_phrase_positive,nb_phrase_neutre,nb_phrase_negative)
       
########################################################################################################################################

contenu_dossier_distant = urllib.request.urlopen('http://trimbtech.fr/CAC40_lazy_price/Fichiers_TXT_traites/').readlines()
for line in contenu_dossier_distant:
    pos1 = str(line).find('href="') 
    pos1 = str(line).find('href="') 
    pos2 = str(line).find('txt') 
    
    nom_fichier = line[pos1+(len(('href="'))-2):pos2+((len('txt')-2))]
    if(len(nom_fichier)>0):
        nom_fichier=nom_fichier.decode()
        print(nom_fichier)
        texte = urllib.request.urlopen('http://trimbtech.fr/CAC40_lazy_price/Fichiers_TXT_traites/'+nom_fichier).readlines()
        texte_fin=""
        for line in texte:    
            if(len(line)<200):   
                line=(line.decode('latin-1'))
                line2=(line)
                line2=line2.replace("\n",".")  
                texte_fin=texte_fin+(line2)
        analyse_sentiment(nom_fichier,texte_fin)

        
# A function to count the number of words in 'cleaned' financial reports

def number_words():
# Read the entire file as a single string
    with open ('blabla.txt', 'rt') as f:
        data = f.read()

# Split
word_count = len(data.split())

print(f"Le texte comporte {word_count} mots")
