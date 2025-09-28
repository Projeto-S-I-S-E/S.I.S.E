import services.database as db
import models.Central as central

def Adicionar(central):
    db.cursor.execute("""
    INSERT INTO Central(usuario, senha, nome)
    VALUES (?,?,?)""",
    central.usuario, central.senha, central.nome).rowcount
    db.cnxn.commit()

def SelecionarNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central")
    listaCentral = []

    for row in db.cursor.fetchall():
        listaCentral.append(central.Central(row[0], row[1], None, None))

    return listaCentral