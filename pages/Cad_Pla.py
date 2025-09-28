import streamlit as st
import Controllers.PlantonistaController as PlantonistaController
import models.Plantonista as plantonista

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
            
    .stFormSubmitButton button{
        background-color: #446A8A;
        color: white;
        border-radius: 5px;
        font-size: 1.1em;
        width: 25%;
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

st.markdown('<h1 class="titulo">Cadastro Plantonista</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])

regionais_data = PlantonistaController.SelecionarRegionalIdNome()

regionais_nome = [nome for idRegional, nome in regionais_data]
regionais_id = {nome: idRegional for idRegional, nome in regionais_data}

with col2:
    with st.form(key="cadastrar-plantonista"):

        nome_plantonista = st.text_input("Nome:", label_visibility="collapsed", placeholder="Nome:")
        nome_regiao = st.selectbox("Região de atuação:", regionais_nome, label_visibility="collapsed", index=None, placeholder="Região de atuação:")
        usuario = st.text_input("Nome de usuário:", label_visibility="collapsed", placeholder="Nome de usuário:")
        senha = st.text_input("Senha:", label_visibility="collapsed", type="password", placeholder="Senha:")

        botao = st.form_submit_button("Cadastrar", use_container_width=True)

if nome_regiao:
    id_regiao = regionais_id[nome_regiao]

if botao:
    plantonista.nome = nome_plantonista
    plantonista.regiao = id_regiao
    plantonista.usuario = usuario
    plantonista.senha = senha

    PlantonistaController.Adicionar(plantonista)
    st.sucess("Plantonista cadastrado com sucesso!")