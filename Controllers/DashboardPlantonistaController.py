import services.database as db

def ObterSolicitacoes(id_usuario_logado):
    
    id_servico_plantonista = ObterServicoDoPlantonista(id_usuario_logado)
    
    if id_servico_plantonista is None:
        print(f"Alerta: Serviço não encontrado para o Plantonista ID: {id_usuario_logado}")
        return []

    sql_query = """
        SELECT
            s.idSolicitacao,
            s.endereco_consolidado,
            s.descricao_consolidada,
            s.gravidade,
            s.data_abertura,
            u.nome AS nome_usuario,
            u.telefone,
            st.nome AS status_solicitacao
        FROM Solicitacao s
        JOIN Usuario u ON s.idUsuario = u.idUsuario
        JOIN [Status] st ON s.idStatus = st.idStatus
        JOIN Relacao_Solicitacao_Servico rss ON s.idSolicitacao = rss.idSolicitacao
        WHERE st.nome IN ('Aguardando', 'Em Andamento')
        AND rss.idServico = ? 
        GROUP BY s.idSolicitacao, s.endereco_consolidado, s.descricao_consolidada, s.gravidade, s.data_abertura, u.nome, u.telefone, st.nome
        ORDER BY 
            CASE 
                WHEN st.nome = 'Aguardando' THEN 1
                WHEN st.nome = 'Em Andamento' THEN 2
                ELSE 3
            END,
            s.data_abertura DESC
    """
    db.cursor.execute(sql_query, id_servico_plantonista)
    try:
        return db.cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar resultados do cursor: {e}")
        return []

def ObterServicoDoPlantonista(id_usuario):
    sql_query = """
        SELECT 
            r.idServico 
        FROM Plantonista p
        JOIN Regional r ON p.idRegional = r.idRegional
        JOIN Perfil perf ON p.nome = perf.nome
        WHERE perf.idPerfil = ?
    """

    db.cursor.execute(sql_query, id_usuario)
    resultado = db.cursor.fetchone()
    
    return resultado[0] if resultado else None

def AtualizarStatusSolicitacao(id_solicitacao, novo_status):
    sql_update = "UPDATE Solicitacao SET idStatus = ? WHERE idSolicitacao = ?"
    db.cursor.execute(sql_update, novo_status, id_solicitacao)
    db.cnxn.commit()
    return True