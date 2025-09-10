import services.database as db
import models.Central as central

def Adicionar(central):
    count = db.cursor.execute("""
    INSERT INTO Central(idServico, usuario, senha, nome)
    VALUES (?,?,?,?)""",
    central.servico, central.usuario, central.senha, central.nome).rowcount
    db.cnxn.commit()

def SelecionarTodos():
    db.cursor.execute("SELECT * FROM Central")
    listaCentral = []

    for row in db.cursor.fetchall():
        listaCentral.append(central.Central(row[0], row[4], row[1], row[2], row[3]))

    return listaCentral