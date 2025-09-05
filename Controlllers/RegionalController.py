import services.database as db

def Adicionar(regional):
    count = db.cursor.execute("""
    INSERT INTO Regional(idCentral, cidade, nome)
    VALUES (?,?,?)""",
    regional.estado, regional.cidade, regional.nome).rowcount
    db.cnxn.commit()