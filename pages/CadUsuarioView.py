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
            background-color: #6B8BB6;
            font-family: Arial;
        }
                
        .stMain div[data-testid="stMainBlockContainer"]{
            margin-left: 150px;
            max-width: 836px;        
        }
                
        .stForm {
            border: none;
            margin-left: -20%;
        }
        
        .stTextInput div[data-baseweb="input"]{
            width: 70%;
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
            top: 2%;
            left: 2%;
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
            font-size: 1.1em;
            width: 27%;
            margin-top: 5%;
            margin-left: 100%;
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

        .efeito-lateral-cima {
            position: fixed;
            top: 0;
            left: 0;
            width: 400px;
            height: 50vh;
            background-color: #FFFFFF;
            z-index: 1;
            clip-path: ellipse(80% 100% at 0% 70%);
            transform: scaleY(-1);
        }

        .efeito-lateral-baixo1 {
            position: fixed;
            top: 50%;
            left: 0;
            width: 265px;
            height: 50vh;
            background-color: #FFFFFF;
            z-index: 1;
            clip-path: ellipse(100% 100% at 0% 50%);
        }
            
        .efeito-lateral-baixo2 {
            position: fixed;
            top: 50%;
            left: 147px;
            width: 150px;
            height: 50vh;
            background-color: #6B8BB6;
            z-index: 1;
            clip-path: ellipse(100% 90% at 0% 80%);
            transform: scaleX(-1);
        }
                
        .titulo {
            color: #FFFFFF;
            text-align: center;
            margin-top: -100px !important;
            margin-left: 40px !important;
            margin-bottom: 30px !important;
            font-size: 4em !important;
            opacity: 0.5;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="efeito-lateral-cima"></div>', unsafe_allow_html=True)
    st.markdown('<div class="efeito-lateral-baixo1"></div>', unsafe_allow_html=True)
    st.markdown('<div class="efeito-lateral-baixo2"></div>', unsafe_allow_html=True)

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