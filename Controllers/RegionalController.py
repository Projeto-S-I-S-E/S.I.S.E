import services.database as db

def Adicionar(regional):
    try:
        db.cursor.execute("""
        INSERT INTO Regional(idCentral, idServico, cidade, nome, status)
        VALUES (?,?,?,?,1)""",
        regional.central, regional.servico, regional.cidade, regional.nome).rowcount

        db.cnxn.commit()
        return True
    
    except Exception as e:
        print(f"Erro ao adicionar Regional: {e}")
        db.cnxn.rollback()
        return False

def Inativar(idRegional):
    try:
        sql_update_regional = "UPDATE Regional SET status = 0 WHERE idRegional = ?"
        db.cursor.execute(sql_update_regional, idRegional)

        db.cnxn.commit()
        return True
    
    except Exception as e:
        print(f"Erro ao inativar Regional: {e}")
        db.cnxn.rollback()
        return False
    
def Atualizar(regional_obj):
    try:
        sql = """
        UPDATE Regional 
        SET nome = ?, idCentral = ?, idServico = ?, cidade = ? 
        WHERE idRegional = ?
        """
        
        parametros = (
            regional_obj.nome, 
            regional_obj.central,
            regional_obj.servico,
            regional_obj.cidade, 
            regional_obj.id
        )
        
        db.cursor.execute(sql, parametros)
        db.cnxn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar Regional: {e}")
        db.cnxn.rollback()
        return False
    
def SelecionarPorId(idRegional):
    try:
        sql = """
        SELECT 
            R.idRegional, 
            R.nome, 
            C.nome AS nomeCentral,
            S.nome AS nomeServico,
            R.cidade,
            R.status,
            R.idCentral,
            R.idServico
        FROM Regional R
        INNER JOIN Central C ON R.idCentral = C.idCentral
        INNER JOIN Servico S ON R.idServico = S.idServico
        WHERE R.idRegional = ?
        """

        resultado = db.cursor.execute(sql, idRegional).fetchone()
        
        if resultado:
            
            regional = {
                'id': resultado[0],
                'nome': resultado[1],
                'nomeCentral': resultado[2],
                'nomeServico': resultado[3],
                'cidade': resultado[4],
                'status': resultado[5],
                'idCentral': resultado[6],
                'idServico': resultado[7]
            }

            return regional
        return None
        
    except Exception as e:
        print(f"Erro ao selecionar Regional por ID: {e}")
        return None

def SelecionarNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional WHERE status = 1")

    return db.cursor.fetchall()

def SelecionarServicoIdNome():
    db.cursor.execute("SELECT idServico, nome FROM Servico")

    return db.cursor.fetchall()

def SelecionarCentralIdNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central WHERE status = 1")

    return db.cursor.fetchall()