import services.database as db

def Adicionar(regional):
    db.cursor.execute("""
    INSERT INTO Regional(idCentral, idServico, cidade, nome, status)
    VALUES (?,?,?,?,1)""",
    regional.central, regional.servico, regional.cidade, regional.nome).rowcount
    db.cnxn.commit()

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

def SelecionarNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional")

    return db.cursor.fetchall()

def SelecionarServicoIdNome():
    db.cursor.execute("SELECT idServico, nome FROM Servico")

    return db.cursor.fetchall()

def SelecionarCentralIdNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central WHERE status = 1")

    return db.cursor.fetchall()