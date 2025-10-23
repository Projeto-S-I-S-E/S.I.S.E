import streamlit as st
import Controllers.RegionalController as RegionalController
from models.Regional import Regional
from utils.utils import navegar_para

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
            max-width: 860px;        
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
            letter-spacing: 0.15em;
        }
                
        .stFormSubmitButton button{
            background-color: #446A8A;
            color: white;
            border-radius: 5px;
            border: none;
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
            margin-left: 60px !important;
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
        navegar_para('REGIONAL_LISTA')

    st.markdown('<h1 class="titulo">Cadastro Regional</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])

    centrais_data = RegionalController.SelecionarCentralIdNome()
    servicos_data = RegionalController.SelecionarServicoIdNome()

    centrais_nomes = [nome for idCentral, nome in centrais_data]
    servicos_nomes = [nome for idServico, nome in servicos_data]
    centrais_id = {nome: idCentral for idCentral, nome in centrais_data}
    servicos_id = {nome: idServico for idServico, nome in servicos_data}


    with col2:
        with st.form(key="cadastrar-regional"):
            
            nome_regional = st.text_input("Nome:", label_visibility="collapsed", placeholder="Nome:")
            nome_central = st.selectbox("Central", centrais_nomes, label_visibility="collapsed", index=None, placeholder="Central:")
            nome_servico = st.selectbox("Serviço", servicos_nomes, label_visibility="collapsed", index=None, placeholder="Serviço:")
            cidade = st.text_input("Cidade:", label_visibility="collapsed", placeholder="Cidade:")
            
            botao = st.form_submit_button("Cadastrar", use_container_width=True)

    if nome_central:
        id_central = centrais_id[nome_central]

    if nome_servico:
        id_servico = servicos_id[nome_servico]

    if botao:
        if nome_regional and id_central and id_servico and cidade:

            nova_regional = Regional(
                id = None,
                nome = nome_regional,
                central = id_central,
                servico = id_servico,
                cidade = cidade,
                status = 1
            )

            RegionalController.Adicionar(nova_regional)
            st.success("Regional cadastrada com sucesso!")
            navegar_para('REGIONAL_LISTA')
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")