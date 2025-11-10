import streamlit as st
import Controllers.DashboardPlantonistaController as DashboardPlantonistaController
import time

def renderizar_dashboard_plantonista():

    st.markdown("""
    <style>
        .stMain div[data-testid="stMainBlockContainer"]{
            margin-left: 200px;
            max-width: 1520px;        
        }
    </style>
    """, unsafe_allow_html=True)

    id_usuario_logado = st.session_state['usuario_id']

    try:
        solicitacoes = DashboardPlantonistaController.ObterSolicitacoes(id_usuario_logado)
        renderizar_solicitacoes_cards(solicitacoes)
    except Exception as e:
        st.error(f"Erro ao carregar solicitações: {e}")
        st.info("Verifique se o banco está acessível e se a lógica de JOIN para obter o serviço do Plantonista está correta.")

def renderizar_solicitacoes_cards(solicitacoes):
    
    STATUS_COLOR_MAP = {
        'Aberta': '#DC143C',
        'Em Andamento': '#FFA500',
        'Concluída': '#32CD32',
        'Crítica': "#46073B",
        'Alta': '#DC143C',
        'Média': '#FFA500',
        'Baixa': '#32CD32'
    }

    st.markdown('<div style="padding-top: 1.5%; padding-left: 5.5%;">', unsafe_allow_html=True)
    
    if not solicitacoes:
        st.info("Nenhuma solicitação aberta ou em andamento no momento.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    cols = st.columns(5)

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
        status_atual = sol[7]
        
        descricao_curta = descricao_completa.split('.')[0]
        if len(descricao_curta) > 50:
             descricao_curta = descricao_curta[:50] + '...'
        
        gravidade_cor_hex = STATUS_COLOR_MAP.get(gravidade, '#AAAAAA')
        status_cor_hex = STATUS_COLOR_MAP.get(status_atual, '#666666')
        status_label = status_atual.upper()
        
        col = cols[i % 5]

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
                    margin: -16px; /* Ajusta margem para parecer parte do container */
                    margin-bottom: 10px;
                    border-radius: 9px 9px 0 0;
                    ">
                    {gravidade.upper()}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <strong style="font-size: 1.1em;">{endereco}</strong><br>
                <hr style="margin: 5px 0;">
                <p style="margin: 0; font-size: 0.9em; height: 50px; overflow: hidden;">
                    {descricao_curta}
                </p>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="
                    background-color: {status_cor_hex}; 
                    color: white; 
                    padding: 5px; 
                    text-align: center;
                    font-size: 0.9em;
                    margin: -16px;
                    margin-top: 10px;
                    border-radius: 0 0 9px 9px;
                    ">
                    {status_label}
                </div>
                """, unsafe_allow_html=True)
            
            if status_atual == 'Aberta':
                botao_label = "Assumir (Em Andamento)"
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