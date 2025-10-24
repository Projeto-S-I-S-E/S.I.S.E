import streamlit as st
import Controllers.LoginController as LoginController
import pages.ConCentralView as ConCentralView
import pages.CadCentralView as CadCentralView
import pages.ConRegionalView as ConRegionalView
import pages.CadRegionalView as CadRegionalView
import pages.ConPlantonistaView as ConPlantonistaView
import pages.CadPlantonistaView as CadPlantonistaView
import pages.CadUsuarioView as CadUsuarioView
import time
from pages.Dashboard import dashboard_por_cargo
from utils.utils import DASHBOARDS, navegar_para

st.set_page_config(
    page_title="S.I.S.E",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}        
    
    .stApp {
        background-color: #6B8BB6;
        font-family: Arial;
    }

    .stTextInput div[data-baseweb="input"]{
        border: none;
    }
    
    .stTextInput input {
        color: #000000;
        background-color: #D9D9D9;
        border: 1px solid #000000;
        border-radius: 7px;
    }
            
    .stTextInput input::-webkit-input-placeholder {
        color: #000000;
        opacity: 0.5;        
    }
            
    .stTextInput input::-moz-placeholder {
        color: #000000;
        opacity: 0.5;
    }
            
    .st-key-btn_cadastro div[data-testid="stButton"] button{
        position: absolute;
        background-color: #9c9a9a;
        color: white;
        border: 1px solid #000000;
        border-radius: 5px;
        font-size: 1.1em;
        width: 30%;
        margin-top: -88px;
        margin-left: 16px;
    }
            
    .stFormSubmitButton button{
        background-color: #446A8A;
        color: white;
        border: 1px solid #000000;
        border-radius: 5px;
        font-size: 1.1em;
        width: 30%;
        margin-top: 10px;
        margin-left: 216px;
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
        margin-top: -80px !important;
        margin-left: 40px !important;
        margin-bottom: 60px !important;
        font-size: 6em !important;
        letter-spacing: 0.2em;
        opacity: 0.75;
    }
            
    .caixa-login {
        position: absolute;
        background-color: #C8C0C0;
        border: 1px solid #000000;
        border-radius: 10px;
        padding: 130px;
        width: 430px;
        margin-top: -20px;
        margin-left: -60px;
    }
</style>
""", unsafe_allow_html=True)

if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'usuario_cargo_id' not in st.session_state:
    st.session_state['usuario_cargo_id'] = None
if 'usuario_nome' not in st.session_state:
    st.session_state['usuario_nome'] = None
if 'pagina_atual' not in st.session_state:
    st.session_state['pagina_atual'] = None

def entrar(cargo_id, nome_usuario):
    st.session_state['logado'] = True
    st.session_state['usuario_cargo_id'] = cargo_id
    st.session_state['usuario_nome'] = nome_usuario
    st.session_state['pagina_atual'] = DASHBOARDS.get(cargo_id)
    st.success("Login efetuado com sucesso!")
    time.sleep(1)
    st.rerun()

def renderizar_login():

    st.markdown('<div class="efeito-lateral-cima"></div>', unsafe_allow_html=True)
    st.markdown('<div class="efeito-lateral-baixo1"></div>', unsafe_allow_html=True)
    st.markdown('<div class="efeito-lateral-baixo2"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="titulo">S.I.S.E</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        
        with st.form(key="fazer-login"):
            st.markdown('<div class="caixa-login">', unsafe_allow_html=True)
            
            usuario = st.text_input("Nome de usuário/E-mail:", label_visibility="collapsed", placeholder="Nome de usuário/E-mail:")
            senha = st.text_input("Senha:", label_visibility="collapsed", type="password", placeholder="Senha:")

            botao = st.form_submit_button("Entrar", use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            if botao:
                cargo_id, nome_usuario = LoginController.AutenticarUsuario(usuario, senha)

                if cargo_id:
                    entrar(cargo_id, nome_usuario)
                else:
                    st.error("Nome de usuário ou senha incorretos.")

        if st.button("Cadastrar", key="btn_cadastro"):
            navegar_para('USUARIO_CADASTRO')

if st.session_state['pagina_atual'] == "USUARIO_CADASTRO":
    CadUsuarioView.renderizar_cadastro()

elif st.session_state['logado']:

    cargo_id = st.session_state['usuario_cargo_id']
    nome_usuario = st.session_state['usuario_nome']

    if st.session_state['pagina_atual'] in ["ADMIN_DASHBOARD", "CENTRAL_DASHBOARD", "PLANTONISTA_DASHBOARD"]:
        dashboard_por_cargo(cargo_id, nome_usuario)
        st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
        st.markdown(f'<p id="nome-perfil">Perfil {nome_usuario}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state['pagina_atual'] == "CENTRAL_LISTA":
        ConCentralView.renderizar_pagina()
        st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
        st.markdown(f'<p id="nome-perfil">Perfil {nome_usuario}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state['pagina_atual'] == "CENTRAL_CADASTRO":
        CadCentralView.renderizar_cadastro()
    elif st.session_state['pagina_atual'] == "REGIONAL_LISTA":
        ConRegionalView.renderizar_pagina()
        st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
        st.markdown(f'<p id="nome-perfil">Perfil {nome_usuario}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state['pagina_atual'] == "REGIONAL_CADASTRO":
        CadRegionalView.renderizar_cadastro()
    elif st.session_state['pagina_atual'] == "PLANTONISTA_LISTA":
        ConPlantonistaView.renderizar_pagina()
        st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
        st.markdown(f'<p id="nome-perfil">Perfil {nome_usuario}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state['pagina_atual'] == "PLANTONISTA_CADASTRO":
        CadPlantonistaView.renderizar_cadastro()

else:

    renderizar_login()