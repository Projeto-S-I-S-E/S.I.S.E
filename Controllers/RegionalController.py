import services.database as db

def Adicionar(regional):
    db.cursor.execute("""
    INSERT INTO Regional(idCentral, idServico, cidade, nome)
    VALUES (?,?,?,?)""",
    regional.central, regional.servico, regional.cidade, regional.nome).rowcount
    db.cnxn.commit()

def SelecionarServicoIdNome():
    db.cursor.execute("SELECT idServico, nome FROM Servico")

    return db.cursor.fetchall()

def SelecionarCentralIdNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central")

    return db.cursor.fetchall()