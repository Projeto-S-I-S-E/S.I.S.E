import streamlit as st

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp{
        background-color: #6B8BB6;
        font-family: Arial;
    }
            
            
    .barra-lateral{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 11%;
        height: 95%;
        background-color: #DBE8EC;
        z-index: 1;
        clip-path: rect(0px 100% 100% 0px);
    }
            
    .barra-superior{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 13%;
        background-color: #DBE8EC;
        z-index: 1;
        clip-path: rect(0px 100% 100% 0px);
    }
            
    .barra-perfil{
        position: fixed;
        bottom: 0;
        left: 0;
        margin-left: 11.5%;
        width: 88%;
        height: 7%;
        border: 1px solid #000000;
        border-radius: 35px 35px 0px 0px;
        background-color: #DBE8EC;
        z-index: 1;
        clip-path: rect(0px 100% 100% 0px);
    }
            
    .botao{
        background-color: #446A8A;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1.1em;
        letter-spacing: 0.15em;
        z-index: 2;
    }
            
    #botaoSair{
        position: fixed;
        top: 0;
        right: 0;
        margin-top: 2%;
        margin-right: 5%;
        width: 80px;
        height: 40px;
    }
            
    #botaoNovoUsuario{
        position: fixed;
        top: 0;
        right: 0;
        margin-top: 10%;
        margin-right: 5%;
        height: 40px;
    }
            
    .titulo{
        position: fixed;
        top: 0;
        left: 0;
        margin-top: 7% !important;
        margin-left: 15% !important;
        color: #FFFFFF;
        font-size: 4em !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="barra-lateral"></div>', unsafe_allow_html=True)
st.markdown('<div class="barra-superior"></div>', unsafe_allow_html=True)
st.markdown('<button id="botaoSair" class="botao">Sair</button>', unsafe_allow_html=True)

st.markdown('<h1 class="titulo">Central:</h1>', unsafe_allow_html=True)
st.markdown('<button id="botaoNovoUsuario" class="botao">Novo usuário</button>', unsafe_allow_html=True)

st.markdown('<div class="barra-perfil"></div>', unsafe_allow_html=True)