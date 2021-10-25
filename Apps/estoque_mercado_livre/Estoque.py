#importando as bibliotecas
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas.core.frame import DataFrame
from stqdm import stqdm
import streamlit as st
import sqlite3
import base64




def app():
    # --- DATABASE -----
    #Criando o database/fazendo a conexão 
    conn = sqlite3.connect('streamlir-br-partners/Apps/estoque_mercado_livre/Data/Database.db')

    #Criando o cursor 
    c = conn.cursor()

    # --- LISTA --- 
    estoque = []

    # ----- FUNÇÕES ----- 

    def add_url(url):
        #Acrescentando o valor da url no sqlite 
        c.execute("INSERT INTO Urls(url) VALUES ('{}')".format(url))

        #Commit do database 
        conn.commit()

        #Printando o resultado 
        st.sidebar.write("A Url foi adicionada a base de dados")

    def download_file(dataset):
        csv = dataset.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="estoque.csv">Download csv file</a>'

        return st.markdown(href, unsafe_allow_html=True)

    def search_quantity():
        urls_values = c.execute("SELECT * FROM Urls")

        urls = urls_values.fetchall()

        for url in stqdm(urls):
            #Fazendo tempo 
            time.sleep(3)

            #Arrumando a url 
            url = url[1]
            url = url.replace(" ","")
            
            #Fazendo o response
            response = urlopen(url)
            html = response.read()

            #Criando o Beautiful Soap
            bs = BeautifulSoup(html, 'html.parser')

            #Fazendo o try
            try:
                ultimo = bs.find(class_='ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--SEMIBOLD').text
                estoque.append("1")
            except:
                try:
                    quant = bs.find(class_='ui-pdp-buybox__quantity__available').text
                    estoque.append(quant)
                except:
                    estoque.append("-")

        #Criando o dataset 
        Dataset = pd.DataFrame()

        #Colocando os valores dentro do dataframe 
        Dataset['Estoque'] = estoque

        #Arrumando os valores de estoque 
        Dataset['Estoque'] = Dataset['Estoque'].str.replace("(","")
        Dataset["Estoque"] = Dataset["Estoque"].str.replace(" disponíveis","")
        Dataset["Estoque"] = Dataset["Estoque"].str.replace(")","")

        #Fazendo o download 
        download_file(Dataset)    


    # ------ APLICATIVO ------- 
    #Escrevendo título 
    st.title("Estoque GoPro - Mercado Livre")

    search = st.button("Clique aqui para pegar o estoque")

    #Fazendo a procura pelas urls 
    if search:
        search_quantity()

    # ---- SIDEBAR ------ 
    #Título so sidebar
    st.sidebar.title("Acrescentar novas Urls")

    #Colocando o campo de texto no sidebar para input 
    new_url = st.sidebar.text_input("Coloque aqui a nova url")

    #Criando o botão para acrescentar a url 
    add_url_button = st.sidebar.button("Acrescentar Url")

    #Adicionando a nova url
    if add_url_button:
        add_url(new_url)

