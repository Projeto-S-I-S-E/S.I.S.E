import services.database as db

ID_CARGO_CENTRAL = 2 

def Adicionar(nome_central, usuario, senha):
    try:
        sql_central = "INSERT INTO Central (nome, status) VALUES (?, 1)"
        db.cursor.execute(sql_central, nome_central)
        
        sql_perfil = """
            INSERT INTO Perfil (idCargo, nome, usuario, senha) 
            VALUES (?, ?, ?, ?)
        """
        db.cursor.execute(sql_perfil, ID_CARGO_CENTRAL, nome_central, usuario, senha) 

        db.cnxn.commit()
        return True

    except Exception as e:
        print(f"Erro ao adicionar central e perfil: {e}")
        db.cnxn.rollback()
        return False

def SelecionarNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central")

    return db.cursor.fetchall()