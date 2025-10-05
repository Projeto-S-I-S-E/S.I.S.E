import streamlit as st
import Controllers.DashboardAdmController as DashboardAdmController

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
            
    div[data-testid="column"] > div > div > [data-testid="stButton"] button {
        width: 200px; 
        height: 150px;
        border: 1px solid #000000;
        border-radius: 5px;
        background-color: #D9D9D9; 
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 10px;
        font-size: 2.5em;
        font-weight: bold;
        color: #000000;
        white-space: pre-wrap;
    }

    .container-cards {
        margin-left: 11.5%;
        margin-right: 5%;
        margin-top: 25%;
        width: 83.5%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="barra-lateral"></div>', unsafe_allow_html=True)
st.markdown('<div class="barra-superior"></div>', unsafe_allow_html=True)
st.markdown('<button id="botaoSair" class="botao">Sair</button>', unsafe_allow_html=True)

def redirect_to(page_name):
    url_destino = f"/{page_name.replace('pages/', '').replace('.py', '')}"

    redirect_script = f"""
        <meta http-equiv="refresh" content="0; url={url_destino}">
    """
    st.markdown(redirect_script, unsafe_allow_html=True)

contagens = DashboardAdmController.ObterContagens()

st.markdown('<div class="container-cards">', unsafe_allow_html=True)

col_cen, col_pla, col_reg = st.columns(3)

with col_cen:
    label_cen = f"Centrais\n\n{contagens['centrais']}"
    if st.button(label_cen, use_container_width=True, key="btn_cen"):
        redirect_to('pages/Con_Cen.py')

with col_pla:
    label_pla = f"Plantonistas\n\n{contagens['plantonistas']}"
    if st.button(label_pla, use_container_width=True, key="btn_pla"):
        redirect_to('pages/Con_Pla.py')

with col_reg:
    label_reg = f"Regionais\n\n{contagens['regionais']}"
    if st.button(label_reg, use_container_width=True, key="btn_reg"):
        redirect_to('pages/Con_Reg.py')

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
st.markdown('<p id="nome-perfil">Perfil Administrador</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)