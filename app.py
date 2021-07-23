import streamlit as st 
from multiapp import MultiApp
from Apps import home
from Apps.estoque_mercado_livre import Estoque
from Apps.catalogo_ads import streamlit_catalogo_mercado_livre
from Apps.WhatsApp import whatsapp_sales

app = MultiApp()

st.title("Aplicativos da BR Partners")

app.add_app("Home", home.app)
app.add_app("Estoque", Estoque.app)
app.add_app("Anúncios catálogo", streamlit_catalogo_mercado_livre.app)
app.add_app("Vendas WhatsApp", whatsapp_sales.app)

app.run()