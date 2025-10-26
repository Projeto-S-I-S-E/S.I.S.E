import streamlit as st
import Controllers.LoginUsuarioController as LoginUsuarioController
import pages.CadUsuarioView as CadUsuarioView
import time
from pages.DashboardUsuario import dashboard_por_cargo
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
        width: 608px;
        height: 1080px;
        background-color: #6B8BB6;
        font-family: Arial;
    }
            
    .stForm {
        margin-top: 60px;
        border: none;
    }
            
    .stElementContainer div[data-testid="stTextInput"]{
        margin-left: 102px;
        margin-right: 112px;
    }
            
    .st-key-usuario div[data-testid="stTextInput"]{
        margin-top: 30px;
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
        position: fixed;
        bottom: 0;
        left: 0;
        background-color: #D9D9D9;
        color: #605252;
        border: none;
        font-size: 4em;
        letter-spacing: 0.15em;
        width: 97%;
        margin-left: 9px;
        margin-bottom: 5px;
        z-index: 2;
    }
            
    .stFormSubmitButton button{
        background-color: #446A8A;
        color: white;
        border: 1px solid #000000;
        border-radius: 5px;
        border: none;
        font-size: 2em;
        letter-spacing: 0.15em;
        width: 20%;
        margin-top: 30px;
        margin-left: 325px;
    }
            
    .titulo {
        color: #FFFFFF;
        text-align: center;
        margin-top: -20px !important;
        margin-left: 45px !important;
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
        margin-top: 20px;
        margin-left: 55px;
    }
            
    #nome-usuario{
        position: fixed;
        display: flex;
        justify-content: center;
        width: 100%;
        top: 0;
        right: 0;
        margin-top: 0.5%;
        color: #636060;
        z-index: 2;
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

    st.markdown('<div class="barra-topo"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="titulo">S.I.S.E</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        
        with st.form(key="fazer-login"):
            st.markdown('<div class="caixa-login">', unsafe_allow_html=True)
            
            usuario = st.text_input("E-mail:", label_visibility="collapsed", placeholder="E-mail:", key="usuario")
            senha = st.text_input("Senha:", label_visibility="collapsed", type="password", placeholder="Senha:")

            botao = st.form_submit_button("Entrar", use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            if botao:
                cargo_id, nome_usuario = LoginUsuarioController.AutenticarUsuario(usuario, senha)

                if cargo_id:
                    entrar(cargo_id, nome_usuario)
                else:
                    st.error("Nome de usuário ou senha incorretos.")

    if st.button("Cadastrar-se", key="btn_cadastro"):
        navegar_para('USUARIO_CADASTRO')

    st.markdown('<div class="barra-baixo"></div>', unsafe_allow_html=True)

if st.session_state['pagina_atual'] == "USUARIO_CADASTRO":
    CadUsuarioView.renderizar_cadastro()

elif st.session_state['logado']:

    cargo_id = st.session_state['usuario_cargo_id']
    nome_usuario = st.session_state['usuario_nome']

    if st.session_state['pagina_atual'] in ["USUARIO_TELA"]:
        dashboard_por_cargo(cargo_id)
        st.markdown(f'<div class="barra-topo"><p id="nome-usuario">{nome_usuario}</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="barra-baixo"></div>', unsafe_allow_html=True)

else:

    renderizar_login()