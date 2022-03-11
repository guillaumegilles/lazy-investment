# -*- coding: utf-8 -*-
import os
#script pyhon permettant de comparer l'évolution du nb de mots pour une enterprise mais pour des années différentes à partir du fichier TXT liste_entreprise.txt
list_of_words=[]
file = open("C:/Users/trimbuj/Desktop/MASTER MIAGE/Projet de conception/test/liste_entreprise.txt", "r",encoding="utf-8")  
for line in file:
	list_of_words.append(line.split())
file.close()
for index, nom_fichier1 in enumerate(list_of_words):

	nom_fichier1=(list_of_words[index][0]).split("_")
	annee_fichier1=(list_of_words[index][0]).split("_")
	nb_mots1=(list_of_words[index][1]).split("_")
	compteur=index+1
	while compteur<len(list_of_words):
		if(nom_fichier1[1] in list_of_words[compteur][0]):
			nb_mots2=(list_of_words[compteur][1]).split("_")
			print("Nombre de mots fichier "+(list_of_words[index][0])+" : "+str(nb_mots1[0]))
			print("Nombre de mots fichier "+(list_of_words[compteur][0])+" : "+str(nb_mots2[0]))
			print("Difference de mots = "+str(int(nb_mots2[0])-int(nb_mots1[0])))
			pourcent=(float(nb_mots2[0])-float((nb_mots1[0])))/float((nb_mots1[0]))*100
			if(pourcent<0):
				print("Diminution de "+str(round(pourcent,2))+"% du nombre de mots")
			else: print("Augmentation de "+str(round(pourcent,2))+"% du nombre de mots")
			print("------------------------------------------------------------")
		compteur=compteur+1
