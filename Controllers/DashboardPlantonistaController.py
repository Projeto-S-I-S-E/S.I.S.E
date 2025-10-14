import services.database as db

def ObterSolicitacoes():
    solicitacoes = []
    
    try:
        sql = """
            SELECT idSolicitacao, endereco, gravidade, descricao 
            FROM Solicitacao
            ORDER BY 
                CASE gravidade 
                    WHEN 'Grave' THEN 1
                    WHEN 'Média' THEN 2
                    WHEN 'Baixa' THEN 3
                    ELSE 4 
                END, 
                idSolicitacao DESC
        """
        db.cursor.execute(sql)
        resultados = db.cursor.fetchall()
        
        for row in resultados:
            solicitacoes.append({
                'id': row[0],
                'endereco': row[1],
                'gravidade': row[2],
                'descricao': row[3]
            })

        return solicitacoes

    except Exception as e:
        print(f"Erro ao obter solicitações: {e}")
        return solicitacoes