import mysql.connector
import yfinance as yf
from datetime import date


connexion_compo = mysql.connector.connect(host='127.0.0.1',
                               port='3308',
                             user='root',
                             passwd='',
                             database='cac40'
                             )

today = date.today()
cursor = connexion_compo.cursor()
cursor.execute("SELECT Ticker,Nom_Entreprise FROM compositions_cac40")
liste_ticker = cursor.fetchall()

for ticker in liste_ticker:
    nom_entreprise=""
    ticker_courant=(ticker[0]+".PA")
    #recuperer cotation
    #dataDF = data.history(interval='1mo', start='2008-1-1', end=today)
    
    data = yf.download(ticker_courant, group_by="ticker", interval='1mo', start="2008-1-1",end=today)    
    nom_entreprise=ticker[1].replace(" ","_")
    nom_entreprise=nom_entreprise.replace("'","")
    nom_entreprise=nom_entreprise.replace(".","")
    #print(data)
    #cursor.execute("CREATE TABLE "+nom_entreprise+" (Date_Mois VARCHAR(255) PRIMARY KEY, Open FLOAT, High FLOAT,Low FLOAT, Close FLOAT, Adj_Close FLOAT, Volume FLOAT)")
    date_prec=0
    
    for label, row in data.iterrows():
       date_courante=label.strftime('%Y_%m') 
       if( date_prec !=  date_courante):
           date_prec=date_courante
           
           print(date_courante)
           if(str(row['Open'])=="nan"):
               row['Open']=-1
           if(str(row['High'])=="nan"):
               row['High']=-1
           if(str(row['Low'])=="nan"):
               row['Low']=-1
           if(str(row['Close'])=="nan"):
               row['Close']=-1
           if(str(row['Adj Close'])=="nan"):
               row['Adj Close']=-1
           if(str(row['Volume'])=="nan"):
               row['Volume']=-1
           
           request = "INSERT INTO "+nom_entreprise+" (Date_Mois,Open,High,Low,Close,Adj_Close,Volume) VALUES ('"+(date_courante)+"',"+str(row['Open'])+","+str(row['High'])+","+str(row['Low'])+","+str(row['Close'])+","+str(row['Adj Close'])+","+str(row['Volume'])+")"
           cursor.execute(request)
connexion_compo.close()
cursor.close()
