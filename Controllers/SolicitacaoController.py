import services.database as db
from typing import Dict, List, Any

def InserirSolicitacao(id_usuario: int, dados_ia: Dict[str, Any]) -> int | None:
    endereco_consolidado = dados_ia.get("endereco_consolidado", "Endereço Desconhecido")
    descricao_consolidada = dados_ia.get("descricao_consolidada", "Descrição Padrão")
    gravidade = dados_ia.get("gravidade", "Indefinida")
    servicos_necessarios: List[str] = dados_ia.get("servicos_acessados", [])

    try:
        sql_solicitacao = """
            INSERT INTO Solicitacao(idUsuario, idStatus, endereco_consolidado, descricao_consolidada, gravidade)
            OUTPUT INSERTED.idSolicitacao
            VALUES (?, 1, ?, ?, ?)
        """

        db.cursor.execute(
            sql_solicitacao,
            id_usuario,
            endereco_consolidado,
            descricao_consolidada,
            gravidade
        )
        id_solicitacao = db.cursor.fetchone()[0]

        if servicos_necessarios:
            placeholders = ','.join(['?'] * len(servicos_necessarios))
            sql_select_servicos = f"SELECT idServico FROM Servico WHERE nome IN ({placeholders})"

            db.cursor.execute(sql_select_servicos, *servicos_necessarios)
            servico_ids = [item[0] for item in db.cursor.fetchall()]

            sql_relacao = """
                INSERT INTO Relacao_Solicitacao_Servico (idSolicitacao, idServico)
                VALUES (?, ?)
            """
            for id_servico in servico_ids:
                db.cursor.execute(sql_relacao, id_solicitacao, id_servico)

        db.cnxn.commit()
        return id_solicitacao
    
    except Exception as e:
        print(f"Erro ao inserir Solicitação e Relações de Serviço: {e}")
        db.cnxn.rollback()
        return None