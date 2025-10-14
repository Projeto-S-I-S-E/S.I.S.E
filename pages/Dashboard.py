import streamlit as st
import Controllers.DashboardAdmController as DashboardAdmController
import Controllers.DashboardCentralController as DashboardCentralController
import Controllers.DashboardPlantonistaController as DashboardPlantonistaController
import time

def navegar_para(chave_pagina):
    st.session_state['pagina_atual'] = chave_pagina
    st.rerun()

def dashboard_por_cargo(cargo_id, nome_usuario):
    
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

    if st.button("Sair", key="botaoSair", type="secondary"):
        st.session_state['logado'] = False
        st.session_state['usuario_cargo_id'] = None
        st.session_state['pagina_atual'] = None
        st.rerun()

    if cargo_id == 1:

        st.markdown('<div class="container-cards">', unsafe_allow_html=True)

        contagens = DashboardAdmController.ObterContagens()

        col_reg, col_cen, col_pla = st.columns(3)

        with col_reg:
            label_reg = f"Regionais\n\n{contagens['regionais']}"
            if st.button(label_reg, use_container_width=True, key="btn_reg"):
                navegar_para('REGIONAL_LISTA')

        with col_cen:
            label_cen = f"Centrais\n\n{contagens['centrais']}"
            if st.button(label_cen, use_container_width=True, key="btn_cen"):
                navegar_para('CENTRAL_LISTA')

        with col_pla:
            label_pla = f"Plantonistas\n\n{contagens['plantonistas']}"
            if st.button(label_pla, use_container_width=True, key="btn_pla"):
                navegar_para('PLANTONISTA_LISTA')

        st.markdown('</div>', unsafe_allow_html=True)

    elif cargo_id == 2:

        st.markdown('<div class="container-cards">', unsafe_allow_html=True)

        contagens_central = DashboardCentralController.ObterContagens(nome_usuario)

        col_reg, col_vazio, col_pla = st.columns(3)

        with col_reg:
            label_reg = f"Regionais\n\n{contagens_central['regionais']}"
            if st.button(label_reg, use_container_width=True, key="btn_reg"):
                navegar_para('REGIONAL_LISTA')

        with col_pla:
            label_pla = f"Plantonistas\n\n{contagens_central['plantonistas']}"
            if st.button(label_pla, use_container_width=True, key="btn_pla"):
                navegar_para('PLANTONISTA_LISTA')

        st.markdown('</div>', unsafe_allow_html=True)

    elif cargo_id == 3:

        solicitacoes = DashboardPlantonistaController.ObterSolicitacoes()

        st.markdown('<div style="padding-top: 20%; padding-left: 11.5%;">', unsafe_allow_html=True)

        cols_sol = st.columns(3)

        for i in range(6):
            with cols_sol[i % 3]:
                st.markdown(f"""
                <div style="background-color: #D9D9D9; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>Grave</strong><br>
                    Rua Pará, {i+1}<br>
                    Incêndio em fábrica...
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="barra-perfil">', unsafe_allow_html=True)
    st.markdown(f'<p id="nome-perfil">Perfil {nome_usuario}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)