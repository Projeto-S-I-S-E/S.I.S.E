import streamlit as st
from utils.utils import navegar_para

def dashboard_por_cargo(cargo_id):
    
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp{
            background-color: #6B8BB6;
            font-family: Arial;
        }
                
        .stMain div[data-testid="stMainBlockContainer"]{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
                
        .stMainBlockContainer div[data-testid="stVerticalBlock"]{
            width: 70%;
            display: flex;
            align-items: center;
        }
                
        .stButton button{
            background-color: #D9D9D9;
            color: black;
            width: 100%;
            height: 80px;
            border-radius: 3px;
            border: none;
            letter-spacing: 0.05em;
        }
                
        .stButton button > div > p{
            font-size: 2em;        
        }
    </style>
    """, unsafe_allow_html=True)

    if cargo_id == 4:

        if st.button("Nova Solicitação +", key="novaSolicitacao"):
            navegar_para('SOLICITACAO_CADASTRO')