import streamlit as st

st.markdown("""
<style>
    .stApp {
        background-color: #6B8BB6;
        font-family: Arial;
    }      
    
    .stTextInput input {
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
            
    .stButton button{
        background-color: #446A8A;
        color: white;
        border: 1px solid #000000;
        border-radius: 5px;
        font-size: 1.1em;
        width: 30%;
        margin-top: 10px;
        margin-left: 240px;
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
        width: 450px;
        margin-top: -20px;
        margin-left: -50px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="efeito-lateral-cima"></div>', unsafe_allow_html=True)
st.markdown('<div class="efeito-lateral-baixo1"></div>', unsafe_allow_html=True)
st.markdown('<div class="efeito-lateral-baixo2"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="titulo">S.I.S.E</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="caixa-login">', unsafe_allow_html=True)
    
    usuario = st.text_input("Nome de usuário:", label_visibility="collapsed", placeholder="Nome de usuário:")
    senha = st.text_input("Senha:", label_visibility="collapsed", type="password", placeholder="Senha:")

    if st.button("Entrar", use_container_width=True):
        if usuario == "admin" and senha == "12345":
            st.success("Login bem-sucedido!")
        else:
            st.error("Nome de usuário ou senha incorretos.")

    st.markdown('</div>', unsafe_allow_html=True)