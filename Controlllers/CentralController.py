import services.database as db

def Adicionar(central):
    count = db.cursor.execute("""
    INSERT INTO Central(idServico, usuario, senha, nome)
    VALUES (?,?,?,?)""",
    central.servico, central.usuario, central.senha, central.nome).rowcount
    db.cnxn.commit()