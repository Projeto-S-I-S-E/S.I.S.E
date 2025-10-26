import streamlit as st
from utils.utils import navegar_para, rota_cargo_dashboard

def renderizar_cadastro():
    
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
                
        .stMainBlockContainer div[data-testid="stVerticalBlockBorderWrapper"]{
            width: 90%;
        }
                
        .stForm{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 0;        
        }
                
        #nome-usuario{
            font-size: 2em;        
        }
                
        .stTextArea label[data-testid="stWidgetLabel"] div > p{
            font-size: 2em;        
        }
                
        .stTextArea div[data-baseweb="textarea"] div{
            background-color: #D9D9D9;
            color: black;
            border-radius: 3px;
            height: 400px;
        }
                
        .stTextArea div[data-baseweb="textarea"] div > textarea{
            color: black;
            font-size: 18px;
        }
                
        .st-key-botaoVoltar div[data-testid="stButton"] button{
            position: fixed;
            top: 0;
            left: 0;
            margin-top: 12%;
            margin-left: 5%;
            height: 50px;
            z-index: 10;
            background-color: #446A8A;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
            font-size: 1.1em;
            letter-spacing: 0.15em;
            cursor: pointer;
        }
                
        .st-key-FormSubmitter-cadastrar-solicitacao-Enviar > div{
            width: 100%;        
        }
                
        .stFormSubmitButton{
            display: flex;
            justify-content: center;
        }
                
        .stFormSubmitButton button{
            background-color: #446A8A;
            color: white;
            border-radius: 5px;
            border: none;
            font-size: 2em;
            width: 30%;
            height: 50px;
            margin-top: 5%;
            margin-left: 0;
            letter-spacing: 0.15em;
        }
    </style>
    """, unsafe_allow_html=True)

    rota_dashboard = rota_cargo_dashboard()

    if st.button("← Voltar para Tela Inicial", key="botaoVoltar"):
        if rota_dashboard:
            navegar_para(rota_dashboard)

    with st.form(key="cadastrar-solicitacao"):

        solicitacao = st.text_area("Descrição:")

        botao = st.form_submit_button("Enviar", use_container_width=True)