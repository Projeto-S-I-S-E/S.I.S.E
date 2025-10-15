import streamlit as st

def navegar_para(chave_pagina):
    st.session_state['pagina_atual'] = chave_pagina
    st.rerun()

def Sair():
    if 'logado' in st.session_state:
        st.session_state['logado'] = False
        
    if 'usuario_cargo_id' in st.session_state:
        del st.session_state['usuario_cargo_id']
    if 'usuario_nome' in st.session_state:
        del st.session_state['usuario_nome']
    
    st.session_state['pagina_atual'] = None
    st.rerun()