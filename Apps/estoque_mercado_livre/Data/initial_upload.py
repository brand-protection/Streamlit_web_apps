#Bibliotecas 
import sqlite3 
import pandas as pd


#Criando conexão com o databse 
database = sqlite3.connect("C:/Users/pedro/Documents/FIVE-C/Streamlit/Apps/estoque_mercado_livre/Data/Database.db")

#Criando o cursor
c =  database.cursor()

#criando a tabela para colocar os dados 
c.execute("CREATE TABLE IF NOT EXISTS Urls(url_id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(1000));")

#Abrindo o arquivo 
dataset = pd.read_excel("C:/Users/pedro/Documents/FIVE-C/Streamlit/Apps/estoque_mercado_livre/Data/Urls.xlsx")

#Colocando os dados dentro da tabela 
for url in dataset['Url']:
    c.execute("INSERT INTO urls(url) VALUES ('{}')".format(url))

#Commit databse 
database.commit()

#Fechando database 
c.close()
database.close()

