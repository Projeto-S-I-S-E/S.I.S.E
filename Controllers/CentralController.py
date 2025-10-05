import services.database as db

def Adicionar(central):
    db.cursor.execute("""
    INSERT INTO Central(usuario, senha, nome)
    VALUES (?,?,?)""",
    central.usuario, central.senha, central.nome).rowcount
    db.cnxn.commit() 

def SelecionarNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central")

    return db.cursor.fetchall()