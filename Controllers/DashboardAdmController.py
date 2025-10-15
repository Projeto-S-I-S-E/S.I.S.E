import services.database as db

def ObterContagens():
    db.cursor.execute("SELECT COUNT(idCentral) FROM Central WHERE status = 1")
    contagem_centrais = db.cursor.fetchone()[0]

    db.cursor.execute("SELECT COUNT(idPlantonista) FROM Plantonista WHERE status = 1")
    contagem_plantonistas = db.cursor.fetchone()[0]

    db.cursor.execute("SELECT COUNT(idRegional) FROM Regional WHERE status = 1")
    contagem_regionais = db.cursor.fetchone()[0]

    return {
        "centrais": contagem_centrais,
        "plantonistas": contagem_plantonistas,
        "regionais": contagem_regionais
    }