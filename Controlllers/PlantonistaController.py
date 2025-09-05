import services.database as db

def Adicionar(plantonista):
    count = db.cursor.execute("""
    INSERT INTO Plantonista(idRegional, usuario, senha, nome)
    VALUES (?,?,?,?)""",
    plantonista.regiao, plantonista.usuario, plantonista.senha, plantonista.nome).rowcount
    db.cnxn.commit()