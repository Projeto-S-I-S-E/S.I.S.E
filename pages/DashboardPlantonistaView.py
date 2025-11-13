import streamlit as st
import Controllers.DashboardPlantonistaController as DashboardPlantonistaController
import time

def renderizar_dashboard_plantonista():

    st.markdown("""
    <style>
        .stMain div[data-testid="stMainBlockContainer"]{
            margin-left: 200px;
            max-width: 1220px;        
        }
                
        .stColumn div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlockBorderWrapper"]{
            background-color: #F0F0F0 !important;
            color: black;
        }
                
        .stButton button{
            background-color: #446A8A;
            color: white;
        }
                
        .stPopover > div > button{
            width: 100%;        
        }
                
        .st-key-botaoAtualizar div[data-testid="stButton"] button{
            background-color: #446A8A;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    id_usuario_logado = st.session_state['usuario_id']
    
    col_espaco, col_atualizar, col_espaco1 = st.columns([3, 1, 3])
    
    with col_atualizar:
        st.button(
            "Atualizar",
            key="btn_atualizar_dashboard",
            use_container_width=True
        )

    try:
        solicitacoes = DashboardPlantonistaController.ObterSolicitacoes(id_usuario_logado)
        renderizar_solicitacoes_cards(solicitacoes)
    except Exception as e:
        st.error(f"Erro ao carregar solicitações: {e}")
        st.info("Verifique se o banco está acessível e se a lógica de JOIN para obter o serviço do Plantonista está correta.")

def renderizar_solicitacoes_cards(solicitacoes):
    
    STATUS_COLOR_MAP = {
        'Aguardando': "#FFBE46",
        'Em Andamento': "#29948F",
        'Concluída': '#32CD32',
        'Crítica': "#46073B",
        'Alta': '#DC143C',
        'Média': "#FF9100",
        'Baixa': '#32CD32'
    }

    st.markdown('<div style="padding-top: 1.5%; padding-left: 5.5%;">', unsafe_allow_html=True)
    
    if not solicitacoes:
        st.info("Nenhuma solicitação aberta ou em andamento no momento.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    cols = st.columns(4)

    def mudar_estado(id_solicitacao, novo_status):
        if DashboardPlantonistaController.AtualizarStatusSolicitacao(id_solicitacao, novo_status):
            pass
        else:
            st.error(f"Falha ao atualizar o status da Solicitação.")

    for i, sol in enumerate(solicitacoes):
        id_solicitacao = sol[0]
        endereco = sol[1]
        descricao_completa = sol[2]
        gravidade = sol[3]
        nome_usuario = sol[5]
        telefone = sol[6]
        status_atual = sol[7]
        
        gravidade_cor_hex = STATUS_COLOR_MAP.get(gravidade, '#AAAAAA')
        status_cor_hex = STATUS_COLOR_MAP.get(status_atual, '#666666')
        status_label = status_atual.upper()
        
        col = cols[i % 4]

        with col:
            with st.container(border=True): 
                
                st.markdown(f"""
                <div style="
                    background-color: {gravidade_cor_hex}; 
                    color: white; 
                    padding: 5px; 
                    text-align: center;
                    font-weight: bold;
                    font-size: 1.1em;
                    margin: -16px;
                    margin-bottom: 10px;
                    border-radius: 9px 9px 0 0;
                    ">
                    {gravidade.upper()}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <strong style="
                    font-size: 1.1em; 
                    line-height: 1.3em;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical; 
                    overflow: hidden;
                    height: 3.9em;
                ">{endereco}</strong>
                <hr style="margin: 15px 0; background-color: black;">
                <p style="
                    margin: 0; 
                    font-size: 0.9em;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical; 
                    overflow: hidden;
                    line-height: 1.3em;
                    height: 2.6em;
                ">
                    {descricao_completa}
                </p>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="
                    background-color: {status_cor_hex}; 
                    color: white; 
                    padding: 5px; 
                    text-align: center;
                    font-weight: bold;
                    font-size: 0.9em;
                    margin: -16px;
                    margin-top: 10px;
                    border-radius: 0 0 9px 9px;
                    ">
                    {status_label}
                </div>
                """, unsafe_allow_html=True)
            
            with st.popover("Ver Detalhes"):
                st.subheader("Detalhes da Solicitação")
                
                st.markdown(f"**Nome:** {nome_usuario}")
                st.markdown(f"**Telefone:** {telefone}")
                st.markdown(f"**Endereço:** {endereco}")
                st.markdown(f"**Gravidade:** **{gravidade}**")
                st.markdown(f"**Status Atual:** *{status_atual}*")
                st.divider()
                st.markdown("**Descrição Completa:**")
                st.markdown(descricao_completa)
                
                if status_atual == 'Aguardando':
                    novo_status_popover = 2
                    st.button("Assumir", 
                              key=f"pop_ass_{id_solicitacao}",
                              on_click=mudar_estado, 
                              args=(id_solicitacao, novo_status_popover),
                              use_container_width=True)
                elif status_atual == 'Em Andamento':
                    novo_status_popover = 3
                    st.button("Finalizar Solicitação", 
                              key=f"pop_fin_{id_solicitacao}",
                              on_click=mudar_estado, 
                              args=(id_solicitacao, novo_status_popover),
                              use_container_width=True)
            
            if status_atual == 'Aguardando':
                botao_label = "Assumir"
                novo_status = 2
                botao_key = f"btn_ass_{id_solicitacao}"
            elif status_atual == 'Em Andamento':
                botao_label = "Finalizar"
                novo_status = 3
                botao_key = f"btn_fin_{id_solicitacao}"
            else:
                botao_label = "" 
                botao_key = f"btn_pass_{id_solicitacao}"

            if botao_label:
                st.button(
                    botao_label, 
                    key=botao_key,
                    use_container_width=True,
                    on_click=mudar_estado,
                    args=(id_solicitacao, novo_status)
                )

    st.markdown('</div>', unsafe_allow_html=True)