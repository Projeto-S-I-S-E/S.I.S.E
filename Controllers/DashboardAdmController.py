import services.database as db

def ObterContagens():
    db.cursor.execute("SELECT COUNT(idCentral) FROM Central")
    contagem_centrais = db.cursor.fetchone()[0]

    db.cursor.execute("SELECT COUNT(idPlantonista) FROM Plantonista")
    contagem_plantonistas = db.cursor.fetchone()[0]

    db.cursor.execute("SELECT COUNT(idRegional) FROM Regional")
    contagem_regionais = db.cursor.fetchone()[0]

    return {
        "centrais": contagem_centrais,
        "plantonistas": contagem_plantonistas,
        "regionais": contagem_regionais
    }