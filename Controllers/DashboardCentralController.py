import services.database as db

def ObterContagens(nome_central):
    contagens = {
        'regionais': 0,
        'plantonistas': 0
    }

    try:
        sql_central_id = "SELECT idCentral FROM Central WHERE nome = ?"
        db.cursor.execute(sql_central_id, nome_central)
        resultado = db.cursor.fetchone()
        
        if not resultado:
            return contagens
            
        id_central = resultado[0]

        sql_regionais = "SELECT COUNT(idRegional) FROM Regional WHERE idCentral = ?"
        db.cursor.execute(sql_regionais, id_central)
        contagens['regionais'] = db.cursor.fetchone()[0]

        sql_plantonistas = """
            SELECT COUNT(P.idPlantonista) 
            FROM Plantonista P
            JOIN Regional R ON P.idRegional = R.idRegional
            WHERE R.idCentral = ?
        """
        db.cursor.execute(sql_plantonistas, id_central)
        contagens['plantonistas'] = db.cursor.fetchone()[0]

        return contagens

    except Exception as e:
        print(f"Erro ao obter contagens da Central: {e}")
        return contagens