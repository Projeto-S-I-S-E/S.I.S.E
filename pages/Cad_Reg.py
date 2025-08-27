import streamlit as st

st.markdown("""
<style>
    .stApp {
        background-color: #6B8BB6;
        font-family: Arial;
    }      
    
    .stTextInput div[data-baseweb="input"]{
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
        background-color: #446A8A;
        color: white;
        border-radius: 5px;
        font-size: 1.1em;
        width: 35%;
        margin-top: 100%;
        margin-left: 80%;
        letter-spacing: 0.15em;
    }
            
    .stSelectbox div[data-baseweb="select"] > div{
        background-color: #D9D9D9;
    }
            
    .stSelectbox div[data-baseweb="select"]{
        z-index: 2;
    }
            
    .stSelectbox .st-cs{
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

st.markdown('<h1 class="titulo">Cadastro Regional</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:

    st.markdown('<div class="caixa-cadastro">', unsafe_allow_html=True)

    nome = st.text_input("Nome:", label_visibility="collapsed", placeholder="Nome:")
    servico = st.selectbox("Estado", ("Bahia", "São Paulo", "Recife"), label_visibility="collapsed", index=None, placeholder="Estado:")
    regiao = st.selectbox("Cidade", ("Salvador", "Simões Filho", "Santa Teresinha", "Rodelas"), label_visibility="collapsed", index=None, placeholder="Cidade:")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.button("Cadastrar", use_container_width=True):
        if nome == "Admin" and nome == "admin":
            st.success("Regional cadastrado com sucesso!")
        else:
            st.error("Informações preenchidas incorretamente, verifique-as!")