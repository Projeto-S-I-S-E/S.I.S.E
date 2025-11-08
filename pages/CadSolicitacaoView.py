import streamlit as st
import Controllers.SolicitacaoController as SolicitacaoController
from streamlit_js_eval import get_geolocation
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from utils.utils import navegar_para, rota_cargo_dashboard
from services.servico_ia import processar_solicitacao_ia

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
    if 'dados_ia' not in st.session_state:
        st.session_state['dados_ia'] = None

def renderizar_cadastro():
    iniciar_state_localizacao()

    dados_localizacao = None
    
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
                
        #endereco-da-ocorrencia{
            color: white;        
        }
                
        .stHeading{
            width: 85%;
            margin-top: 60px;
            margin-left: 40px;
        }
                
        .stTextArea label[data-testid="stWidgetLabel"] div > p{
            font-size: 2em;        
        }
                
        .stTextArea label[data-testid="stWidgetLabel"] div > p:disabled{
            color: white;
            opacity: 1;
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
                
        .stTextArea div[data-baseweb="textarea"] div > textarea:disabled{
            -webkit-text-fill-color: black;
            color: black;
            opacity: 0.5;
        }
                
        .stText {
            width: 85%;
            margin-left: 40px;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #446A8A;
            border-radius: 5px;
            font-size: 1.2em;
        }
                
        .stText div[data-testid="stText"]{
            padding: 5px;
        }
                
        .stText > div{
            color: white;        
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
            width: 42.5%;
            height: 50px;
            margin-top: 5%;
            margin-left: 0;
            letter-spacing: 0.15em;
        }
    </style>
    """, unsafe_allow_html=True)

    rota_dashboard = rota_cargo_dashboard()

    if st.button("← Voltar para Tela Inicial", key="botaoVoltar"):

        st.session_state['status_localizacao'] = 'Aguardando'
        st.session_state['requisicao_geolocalizacao'] = False
        st.session_state['latitude'] = None
        st.session_state['longitude'] = None
        st.session_state['endereco_completo'] = ""
        st.session_state['solicitacao_pendente'] = ""
        st.session_state['dados_ia'] = None

        if rota_dashboard:
            navegar_para(rota_dashboard)

    if st.session_state['status_localizacao'] == 'Obtido':
        st.subheader("Endereço da Ocorrência:")
        st.text(st.session_state['endereco_completo'])
    elif st.session_state['status_localizacao'] == 'Erro':
        st.error("Falha ao obter localização. Verifique as permissões do seu navegador e clique em 'Tentar Novamente'.")
    elif st.session_state['status_localizacao'] == 'Erro Persistência':
        st.error("Ocorreu um erro ao registrar sua solicitação no sistema. Clique em 'Tentar Novamente' para reenviar.")
    elif st.session_state['requisicao_geolocalizacao']:
        st.info("Aguardando permissão de localização do navegador. Por favor, aceite a solicitação que apareceu na tela.")

    textarea_desativado = False
    botao_desativado = False
    botao_mensagem = "Enviar Solicitação"

    if st.session_state['status_localizacao'] == 'Obtido':
        textarea_desativado = False
        botao_desativado = False
        botao_mensagem = "Confirmar Envio"
    elif st.session_state['status_localizacao'] == 'IA Processando':
        textarea_desativado = True
        botao_desativado = True
        botao_mensagem = "Processando..."
    elif st.session_state['status_localizacao'] == 'Erro' or st.session_state['status_localizacao'] == 'Erro Persistência':
        textarea_desativado = True
        botao_mensagem = "Tentar Novamente"

    if st.session_state['requisicao_geolocalizacao'] and st.session_state['status_localizacao'] == 'Aguardando':
        textarea_desativado = True
        botao_desativado = True
        botao_mensagem = "Aguardando Localização..."

    if st.session_state['status_localizacao'] == 'IA Concluída':
        textarea_desativado = True
        botao_desativado = True
        botao_mensagem = "Solicitação Enviada"
        st.success("Sua solicitação foi registrada com sucesso!")

    with st.form(key="cadastrar-solicitacao"):

        solicitacao = st.text_area(
            "Descrição do Ocorrido:",
            value=st.session_state['solicitacao_pendente'],
            placeholder="Digite aqui a sua ocorrência, em caso de vitimas, estime a quantidade de pessoas envolvidas. Se conseguir, digite as condiçoes em que as vitimas se encontram (se conseguem respirar, se estão acordadas ou estão presas em algum local).",
            disabled=textarea_desativado
        )

        botao = st.form_submit_button(botao_mensagem, use_container_width=True, disabled=botao_desativado)

        if botao and st.session_state['status_localizacao'] != 'IA Concluída':
            if not solicitacao.strip():
                st.warning("A descrição da ocorrência não pode estar vazia.")

            elif st.session_state['status_localizacao'] != 'Obtido':
                st.session_state['requisicao_geolocalizacao'] = True
                st.session_state['status_localizacao'] = 'Aguardando'
                st.session_state['solicitacao_pendente'] = solicitacao

                st.rerun()

            elif st.session_state['status_localizacao'] == 'Obtido':
                st.session_state['solicitacao_pendente'] = solicitacao
                st.session_state['status_localizacao'] = 'IA Processando'
                st.rerun()

    if st.session_state['status_localizacao'] == 'IA Processando':
        st.info("Analisando a ocorrência...")

        with st.spinner("Aguarde a análise da inteligência artificial..."):
            dados_ia_processados = processar_solicitacao_ia(
                endereco_completo=st.session_state['endereco_completo'],
                descricao_usuario=st.session_state['solicitacao_pendente']
            )

        if 'erro' in dados_ia_processados:
            st.error(f"Erro no Processamento da IA: {dados_ia_processados['erro']}")
            st.session_state['status_localizacao'] = 'Erro'
            st.rerun()
        else:
            st.session_state['dados_ia'] = dados_ia_processados
            id_usuario = st.session_state['usuario_id']

            try:
                id_solicitacao_criada = SolicitacaoController.InserirSolicitacao(
                    id_usuario=id_usuario,
                    dados_ia=st.session_state['dados_ia']
                )

                if id_solicitacao_criada:
                    st.success(f"Solicitação {id_solicitacao_criada} registrada! Plantonista notificado.")
                    st.session_state['status_localizacao'] = 'IA Concluída'
                else:
                    st.error("FATAL: Falha ao inserir dados no banco. Tente novamente.")
                    st.session_state['status_localizacao'] = 'Erro Persistência'

            except Exception as e:
                st.error(f"FATAL: Erro durante a persistência: {e}")
                st.session_state['status_localizacao'] = 'Erro Persistência'

            st.rerun()

    if st.session_state['requisicao_geolocalizacao'] and st.session_state['status_localizacao'] == 'Aguardando':
        dados_localizacao = get_geolocation()
        if dados_localizacao and 'coords' in dados_localizacao:
            dados_localizacao = dados_localizacao['coords']
        else:
            dados_localizacao = None

    if dados_localizacao and st.session_state['status_localizacao'] == 'Aguardando' and st.session_state['requisicao_geolocalizacao']:
        latitude = dados_localizacao.get("latitude")
        longitude = dados_localizacao.get("longitude")

        if latitude is not None and longitude is not None:
            st.session_state['latitude'] = latitude
            st.session_state['longitude'] = longitude
            st.session_state['status_localizacao'] = 'Obtido'

            st.session_state['requisicao_geolocalizacao'] = False

            with st.spinner('Convertendo coordenadas em endereço...'):
                endereco = buscar_endereco_reverso(latitude, longitude)

            if endereco:
                st.session_state['endereco_completo'] = endereco
            else:
                st.session_state['endereco_completo'] = f"Coordenadas: Lat={latitude:.5f}, Lon={longitude:.5f} (Endereço não encontrado)"
            
            st.rerun()

        elif dados_localizacao.get("error_message"):
            st.session_state['status_localizacao'] = 'Erro'
            st.rerun()