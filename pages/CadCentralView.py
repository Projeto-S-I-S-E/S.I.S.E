import streamlit as st
import Controllers.CentralController as CentralController
from models.Central import Central
from utils.utils import navegar_para

def renderizar_cadastro():

    central_id = st.session_state.get('central_id_editar', None)
    central_dados = None

    nome_inicial = ""
    usuario_inicial = ""

    if central_id:
        titulo_pagina = "Edição Central"
        central_dados = CentralController.SelecionarPorId(central_id)

        if central_dados:
            nome_inicial = central_dados['nome']
            usuario_inicial = central_dados['usuario']

    else:
        titulo_pagina = "Cadastro Central"

    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background-color: #6B8BB6;
            font-family: Arial;
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
                
        .stButton button{
            position: fixed;
            top: 2%;
            left: 2%;
            z-index: 1000;
            background-color: #446A8A;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;  
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

    if st.button("← Voltar para Lista"):
        if central_id:
            del st.session_state['central_id_editar']
        navegar_para('CENTRAL_LISTA')

    st.markdown(f'<h1 class="titulo">{titulo_pagina}</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        form_key = "editar-central" if central_id else "cadastrar-central"
        with st.form(key=form_key):

            nome = st.text_input("Nome:", value=nome_inicial, label_visibility="collapsed", placeholder="Nome:")
            usuario = st.text_input("Nome de usuário:", value=usuario_inicial, label_visibility="collapsed", placeholder="Nome de usuário:")
            senha = st.text_input("Senha:", label_visibility="collapsed", type="password", placeholder="Senha: (deixe em branco para não alterar)" if central_id else "Senha:")

            rotulo_botao = "Salvar" if central_id else "Cadastrar"
            botao = st.form_submit_button(rotulo_botao, use_container_width=True)

    if botao:
        if nome and usuario and (central_id or senha):

            if central_id:

                atualizar_central = Central(
                    id = central_id,
                    nome = nome,
                    usuario = usuario,
                    senha = None, 
                    status = central_dados['status']
                )

                if CentralController.Atualizar(atualizar_central, nova_senha=senha if senha else None):
                    st.success("Central atualizada com sucesso!")
                    del st.session_state['central_id_editar']
                    navegar_para('CENTRAL_LISTA')
                else:
                    st.error("Erro ao atualizar Central.")

            else:

                nova_central = Central(
                    id = None,
                    nome = nome,
                    usuario = usuario,
                    senha = senha,
                    status = 1
                )

                if CentralController.Adicionar(nova_central):
                    st.success("Central cadastrada com sucesso!")
                    navegar_para('CENTRAL_LISTA')
                else:
                    st.error("Erro ao cadastrar Central.")
        else:
            st.error("Por favor, preencha o Nome, Nome de Usuário e Senha (Senha é obrigatória no Cadastro).")