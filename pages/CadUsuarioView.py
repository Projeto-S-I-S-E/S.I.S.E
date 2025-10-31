import streamlit as st
import Controllers.UsuarioController as UsuarioController
from models.Usuario import Usuario
from utils.utils import Sair
import time
import re

def validar_email(email):
    return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def renderizar_cadastro():

    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            width: 608px;
            height: 1080px;
            background-color: #6B8BB6;
            font-family: Arial;
        }
                
        .stMain div[data-testid="stMainBlockContainer"]{
            margin-top: 110px;
            max-width: 736px;        
        }
                
        .stForm {
            border: none;
        }
        
        .stTextInput div[data-baseweb="input"]{
            width: 100%;
            border: none;        
        }

        .stTextInput input{
            color: #000000;
            background-color: #D9D9D9;
            border: 1px solid #000000;
            border-radius: 7px;
            z-index: 2;
        }
                
        .stTextInput input::-webkit-input-placeholder {
            color: #000000;
            opacity: 0.5;        
        }
                
        .stTextInput input::-moz-placeholder {
            color: #000000;
            opacity: 0.5;
        }
                
        .st-key-voltarLogin div[data-testid="stButton"] button{
            position: fixed;
            top: 8%;
            left: 4%;
            width: 210px;
            z-index: 1000;
            background-color: #446A8A;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
            letter-spacing: 0.15em;
        }
                
        .stFormSubmitButton button{
            background-color: #446A8A;
            color: white;
            border-radius: 5px;
            border: none;
            font-size: 2em;
            width: 30%;
            margin-top: 5%;
            margin-left: 190px;
            letter-spacing: 0.15em;
        }
                
        .stSelectbox div[data-baseweb="select"] > div{
            background-color: #D9D9D9;
        }
                
        .stSelectbox div[data-baseweb="select"]{
            width: 70%;
            z-index: 2;
        }
                
        .stSelectbox div[data-baseweb="select"] > div > div > div{
            color: #000000;
            opacity: 0.5;
        }

        .stSelectbox svg{
            color: #000000;
            opacity: 0.5;
        }
                
        .titulo {
            color: #FFFFFF;
            text-align: center;
            margin-top: -100px !important;
            margin-left: 20px !important;
            margin-bottom: 30px !important;
            font-size: 4em !important;
            opacity: 0.5;
        }
                
        .barra-topo{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 5%;
            border: 1px solid #000000;
            border-radius: 0px 0px 35px 35px;
            background-color: #D9D9D9;
            z-index: 1;
            clip-path: rect(0px 100% 100% 0px);
        }
                
        .barra-baixo{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 5%;
            border: 1px solid #000000;
            border-radius: 35px 35px 0px 0px;
            background-color: #D9D9D9;
            z-index: 1;
            clip-path: rect(0px 100% 100% 0px);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="barra-topo"></div>', unsafe_allow_html=True)

    if st.button("← Voltar para Login", key="voltarLogin"):
        Sair()

    st.markdown('<h1 class="titulo">Cadastro Usuário</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        with st.form(key="cadastrar-usuario"):

            nome = st.text_input("Nome completo:", label_visibility="collapsed", placeholder="Nome:")
            email = st.text_input("Email:", label_visibility="collapsed", placeholder="Email:")
            telefone = st.text_input("Telefone:", label_visibility="collapsed", placeholder="Telefone (com DDD):")
            senha = st.text_input("Senha:", label_visibility="collapsed", type="password", placeholder="Senha:")
            confirmar_senha = st.text_input("Confirmar Senha:", label_visibility="collapsed", type="password", placeholder="Confirmar Senha:")

            botao = st.form_submit_button("Cadastrar", use_container_width=True)

    st.markdown('<div class="barra-baixo"></div>', unsafe_allow_html=True)

    if botao:

        telefone_limpo = re.sub(r'\D', '', telefone)

        if not nome or not email or not telefone or not senha or not confirmar_senha:
            st.error("Por favor, preencha todos os campos obrigatórios.")
            return
        
        if senha != confirmar_senha:
            st.error("A senha e a confirmação de senha não coincidem.")
            return
        
        if not validar_email(email):
            st.error("Por favor, insira um endereço de e-mail válido.")
            return
        
        if not (10 <= len(telefone_limpo) <= 11):
            st.error("Número de telefone inválido. O DDD e o número devem ter entre 10 e 11 dígitos no total.")
            return

        novo_usuario = Usuario(
            id = None,
            nome = nome,
            email = email,
            senha = senha,
            telefone = telefone_limpo,
            status = 1
        )

        if UsuarioController.Adicionar(novo_usuario):
            st.success("Cadastro realizado com sucesso! Você será redirecionado para o login.")
            time.sleep(1)
            Sair()
        else:
            st.error("Erro ao realizar cadastro. Tente novamente.")