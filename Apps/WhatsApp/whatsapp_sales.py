#Importando as bibliotecas 
import pandas as pd 
import streamlit as st 

def app():
    #Funções 
    def loading_input(file):
        #Lendo o input
        data = pd.read_csv(file, delimiter="\t", header = None, names = ["text"])

        #Arrumando o arquivo 
        data[['datetime_str','text_2']] = data['text'].str.split(" - ",1,expand=True)

        #Arrumando as horas 
        data['datetime_str'] = data['datetime_str'].str.partition(" ")[0]

        #Arrumando as datas 
        data['datetime'] = pd.to_datetime(data['datetime_str'], errors='coerce', dayfirst=True, yearfirst=False)

        #Arrumando texto e nome dos sellers 
        data[['sender','text_message']] = data['text_2'].str.split(": ",1,expand=True)
        data = data.dropna(subset=['text_message'])
        data = data.drop(columns=['text','text_2'])

        #Criando o dataset que será utilizado para captação
        data_right = data[data['text_message'].str.contains("/", na=False)]

        #Criando o dataset final com as datas certas 
        new = data_right[data_right['datetime'] >= pd.to_datetime(start)]
        new = new[new['datetime'] <= pd.to_datetime(end)]

        #dataset final 
        dataset_final = pd.DataFrame()

        #Arrumando o dataset final 
        dataset_final['Loja'] = new['text_message'].str.partition("/")[0]    
        dataset_final['Item'] = new['text_message'].str.partition("/")[2].str.partition("/")[0]
        dataset_final["Quantidade"] = new["text_message"].str.partition("/")[2].str.partition("/")[2]

        #Arrumando o index 
        dataset_final.reset_index(drop=True)

        #Pegando apenas numeros 
        dataset_final = dataset_final[dataset_final['Quantidade'].str.len() <= 3]

        #Arrumando o dado de quantidade
        dataset_final["Quantidade"] = dataset_final["Quantidade"].astype('int')

        #Arrumando os nomes do seller caso estejam diferentes 
        try:
            dataset_final["Loja"] = dataset_final["Loja"].str.replace("Zharer","ZAHER")
            dataset_final["Loja"] = dataset_final["Loja"].str.replace("Zharrer","ZAHER")
            dataset_final['Loja'] = dataset_final['Loja'].str.replace("Zaher", "ZAHER")
            dataset_final['Loja'] = dataset_final['Loja'].str.replace("Zhaer", "ZAHER")
            dataset_final['Loja'] = dataset_final['Loja'].str.replace("Vítor", "Vitor")
            dataset_final['Item'] = dataset_final['Item'].str.replace("Max", "MAX")        
        except:
            pass

        #Fazendo o groupby dos vendedores
        sellthru = dataset_final.groupby(['Loja','Item'])['Quantidade'].sum().reset_index()

        return sellthru

    #aplicativo 
    st.title("Pegando os dados de vendas dentro do WhatsApp")

    #Instruções 
    instrucoes = st.beta_expander("Como pegar o arquivo .txt")
    instrucoes.write("Entre na conversa no CELULAR e clique nos 3 pontinhos no lado superior direito da conversa. Clique em 'Mais' e depois em 'Exportar conversa' e clique na opção 'Sem mídia'")

    #Colocando as datas que a mensagens serão captadas 
    start = st.date_input('Coloque sua data Inicial')
    end = st.date_input("Coloque sua data Final")

    #Pegando o arquivo input do usuário 
    data_input = st.file_uploader("Importe o arquivo txt do WhatsApp")

    #Criando o botão para analisar a conversa 
    button = st.button("Pegar a quantidade de vendas")

    #Fazendo depois de clicar o botão 
    if button:
        #Fazendo a função 
        st.dataframe(loading_input(data_input))




