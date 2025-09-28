import services.database as db

def Adicionar(plantonista):
    count = db.cursor.execute("""
    INSERT INTO Plantonista(idRegional, usuario, senha, nome)
    VALUES (?,?,?,?)""",
    plantonista.regiao, plantonista.usuario, plantonista.senha, plantonista.nome).rowcount
    db.cnxn.commit()

def SelecionarNome():
    db.cursor.execute("SELECT idPlantonista, nome FROM Plantonista")

    return db.cursor.fetchall()

def SelecionarRegionalIdNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional")

    return db.cursor.fetchall()