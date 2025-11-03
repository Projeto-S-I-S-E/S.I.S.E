import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from utils.utils import navegar_para, rota_cargo_dashboard
import json

geolocalizador = Nominatim(user_agent="projeto_sise")

def buscar_endereco_reverso(latitude, longitude):
    coordenadas = f"{latitude}, {longitude}"

    try:
        localizacao_endereco = geolocalizador.reverse(coordenadas, language='pt', timeout=10)

        if localizacao_endereco:
            return localizacao_endereco.address
        else:
            return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        st.error(f"Erro ao buscar endereço (Geopy): {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None
    
def iniciar_state_localizacao():
    if 'status_localizacao' not in st.session_state:
        st.session_state['status_localizacao'] = 'Aguardando'
    if 'requisicao_geolocalizacao' not in st.session_state:
        st.session_state['requisicao_geolocalizacao'] = False
    if 'latitude' not in st.session_state:
        st.session_state['latitude'] = None
    if 'longitude' not in st.session_state:
        st.session_state['longitude'] = None
    if 'endereco_completo' not in st.session_state:
        st.session_state['endereco_completo'] = ""
    if 'solicitacao_pendente' not in st.session_state:
        st.session_state['solicitacao_pendente'] = ""

def renderizar_cadastro():
    iniciar_state_localizacao()

    dados_localizacao = None

    textarea_desativado = (st.session_state['requisicao_geolocalizacao'] and st.session_state['status_localizacao'] != 'Obtido')
    
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp{
            background-color: #6B8BB6;
            font-family: Arial;
        }
                
        .stMain div[data-testid="stMainBlockContainer"]{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
                
        .stMainBlockContainer div[data-testid="stVerticalBlockBorderWrapper"]{
            width: 90%;
        }
                
        .stForm{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 0;        
        }
                
        #nome-usuario{
            font-size: 2em;        
        }
                
        .stTextArea label[data-testid="stWidgetLabel"] div > p{
            font-size: 2em;        
        }
                
        .stTextArea div[data-baseweb="textarea"] div{
            background-color: #D9D9D9;
            color: black;
            border-radius: 3px;
            height: 400px;
        }
                
        .stTextArea div[data-baseweb="textarea"] div > textarea{
            color: black;
            font-size: 18px;
        }
                
        .stTextArea div[data-baseweb="textarea"] div > textarea::placeholder{
            color: black;
            opacity: 0.5;
        }
                
        .stText {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #446A8A;
            color: white;
            border-radius: 5px;
            font-size: 1.2em;
        }
                
        .stText div[data-testid="stText"]{
            padding: 5px;
        }
                
        .st-key-botaoVoltar div[data-testid="stButton"] button{
            position: fixed;
            top: 0;
            left: 0;
            margin-top: 12%;
            margin-left: 5%;
            width: 280px;
            height: 50px;
            z-index: 10;
            background-color: #446A8A;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
            font-size: 1.1em;
            letter-spacing: 0.15em;
            cursor: pointer;
        }
                
        .st-key-FormSubmitter-cadastrar-solicitacao-Enviar > div{
            width: 100%;        
        }
                
        .stFormSubmitButton{
            display: flex;
            justify-content: center;
        }
                
        .stFormSubmitButton button{
            background-color: #446A8A;
            color: white;
            border-radius: 5px;
            border: none;
            font-size: 2em;
            width: 42%;
            height: 50px;
            margin-top: 5%;
            margin-left: 0;
            letter-spacing: 0.15em;
        }
                
        div[class="st-key-loc"] > div:first-child{
            background-color: transparent !important;
        }
                
        div[class="st-key-loc"] > iframe{
            height: 50px !important;
            width: 100% !important;
            border: none !important;
            margin-top: 10px;
            margin-bottom: 20px;
        }
                
        div[class="st-key-loc"] iframe body button{
            background-color: #28a745 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 1.2em !important;
            font-weight: bold !important;
            border: none !important;
            cursor: pointer;
            width: 100%;
            height: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

    rota_dashboard = rota_cargo_dashboard()

    if st.button("← Voltar para Tela Inicial", key="botaoVoltar"):
        if rota_dashboard:
            navegar_para(rota_dashboard)

    if st.session_state['status_localizacao'] == 'Obtido':
        st.success("Localização Obtida!")
        st.subheader("Endereço da Ocorrência:")
        st.text(st.session_state['endereco_completo'])
    elif st.session_state['status_localizacao'] == 'Erro':
        st.error("Falha ao obter localização. Verifique as permissões do seu navegador e clique em 'Tentar Novamente'.")
    elif st.session_state['requisicao_geolocalizacao']:
        st.info("Passo 2 de 2: Clique no botão abaixo para permitir a captura da sua localização.")

    botao_desativado = False
    botao_mensagem = "Enviar Solicitação"

    if st.session_state['status_localizacao'] == 'Obtido':
        botao_mensagem = "Confirmar Envio"
    elif st.session_state['status_localizacao'] == 'Erro':
        botao_desativado = True
        botao_mensagem = "Verificar Permissões"

    if st.session_state['requisicao_geolocalizacao'] and st.session_state['status_localizacao'] == 'Aguardando':
        botao_desativado = True
        botao_mensagem = "Aguardando Localização..."

    with st.form(key="cadastrar-solicitacao"):

        solicitacao = st.text_area(
            "Descrição do Ocorrido:",
            value=st.session_state['solicitacao_pendente'],
            placeholder="Digite aqui a sua ocorrência, em caso de vitimas, estime a quantidade de pessoas envolvidas. Se conseguir, digite as condiçoes em que as vitimas se encontram (se conseguem respirar, se estão acordadas ou estão presas em algum local).",
            disabled=textarea_desativado
        )

        if st.session_state['requisicao_geolocalizacao'] and st.session_state['status_localizacao'] == 'Aguardando':
            with st.container(key="localizacao"):
                st.markdown(
                    """
                    <div style='text-align: center; margin-bottom: 10px; font-size: 1.2em; color: #f8d7da; background-color: #721c24; border-radius: 5px; padding: 10px;'>
                        Clique no botão verde abaixo para capturar sua localização.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                dados_localizacao = streamlit_geolocation()

        botao = st.form_submit_button(botao_mensagem, use_container_width=True, disabled=botao_desativado)

        if botao:
            if not solicitacao.strip():
                st.warning("A descrição da ocorrência não pode estar vazia.")
            elif st.session_state['status_localizacao'] != 'Obtido':
                st.session_state['requisicao_geolocalizacao'] = True
                st.session_state['status_localizacao'] = 'Aguardando'
                st.session_state['solicitacao_pendente'] = solicitacao

                st.rerun()
            elif st.session_state['status_localizacao'] == 'Obtido':
                dados_finais = {
                    "descricao": solicitacao,
                    "lat": st.session_state['latitude'],
                    "lon": st.session_state['longitude'],
                    "endereco_final": st.session_state['endereco_completo']
                }

                st.json(dados_finais)

    if dados_localizacao and st.session_state['status_localizacao'] == 'Aguardando' and st.session_state['requisicao_geolocalizacao']:
        latitude = dados_localizacao.get("latitude")
        longitude = dados_localizacao.get("longitude")

        if latitude is not None and longitude is not None:
            st.session_state['latitude'] = latitude
            st.session_state['longitude'] = longitude
            st.session_state['status_localizacao'] = 'Obtido'

            endereco = buscar_endereco_reverso(latitude, longitude)

            if endereco:
                st.session_state['endereco_completo'] = endereco
            else:
                st.session_state['endereco_completo'] = f"Coordenadas: Lat={latitude:.5f}, Lon={longitude:.5f} (Endereço não encontrado)"
            
            st.rerun()

        elif dados_localizacao.get("error_message"):
            st.session_state['status_localizacao'] = 'Erro'
            st.rerun()