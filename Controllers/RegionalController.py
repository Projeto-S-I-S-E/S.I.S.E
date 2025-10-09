import services.database as db

def Adicionar(regional):
    db.cursor.execute("""
    INSERT INTO Regional(idCentral, idServico, cidade, nome, status)
    VALUES (?,?,?,?,1)""",
    regional.central, regional.servico, regional.cidade, regional.nome).rowcount
    db.cnxn.commit()

def SelecionarNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional")

    return db.cursor.fetchall()

def SelecionarServicoIdNome():
    db.cursor.execute("SELECT idServico, nome FROM Servico")

    return db.cursor.fetchall()

def SelecionarCentralIdNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central")

    return db.cursor.fetchall()