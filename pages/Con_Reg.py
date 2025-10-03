import streamlit as st
import Controllers.RegionalController as RegionalController

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

    .barra-lista-item{
        width: 120%;
        height: 80px;
        border: 1px solid #000000;
        border-radius: 5px;
        background-color: #D9D9D9;
        display: flex;
        align-items: center;
        padding: 0 20px;
        margin-bottom: 15px;
    }

    .lista-titulo {
        font-size: 1.5em;
        font-weight: bold;
        color: #000000;
        flex-grow: 1;
    }

    .lista-botoes {
        display: flex;
        gap: 10px;
    }

    .botao-lista {
        background-color: #7B1A1E;
        border: 1px solid #440C0E;
        width: 25px;
        height: 25px;
        cursor: pointer;
        border-radius: 5px;
        color: white;
        display: inline-block;
        padding: 0;
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
        background-color: #D9D9D9;
        z-index: 1;
        clip-path: rect(0px 100% 100% 0px);
    }

    #nome-perfil{
        position: fixed;
        bottom: 0;
        right: 0;
        margin-right: 38% !important;
        margin-bottom: 0.5%;
        color: #000000;
        font-size: 1.3em !important;
        z-index: 2;
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
            
    #botaoNovaRegional{
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
        margin-left: 16% !important;
        color: #FFFFFF;
        font-size: 4em !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="barra-lateral"></div>', unsafe_allow_html=True)
st.markdown('<div class="barra-superior"></div>', unsafe_allow_html=True)
st.markdown('<button id="botaoSair" class="botao">Sair</button>', unsafe_allow_html=True)

st.markdown('<h1 class="titulo">Regionais:</h1>', unsafe_allow_html=True)
st.markdown('<button id="botaoNovaRegional" class="botao">Nova regional</button>', unsafe_allow_html=True)

lista_de_regionais = RegionalController.SelecionarNome()

st.markdown("""
<div style="
    padding-top: 15%; 
    margin-left: 16%;
    padding-right: 5%;
    height: calc(100hv - 200px);
    overflow-y: auto;">
""", unsafe_allow_html=True)

for regional in lista_de_regionais:
    st.markdown(f"""
        <div class="barra-lista-item">
            <span class="lista-titulo">{regional.nome}</span>
            <div class="lista-botoes">
                <button class="botao-lista" style="background-color: #446A8A; color: white; font-size: 1.2em; line-height: 1;">&#x270e</button>
                <button class="botao-lista" style="background-color: #7B1A1E; color: white; font-size: 1.2em; line-height: 1;">&#x2716;</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
st.markdown('<p id="nome-perfil">Perfil Administrador</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)