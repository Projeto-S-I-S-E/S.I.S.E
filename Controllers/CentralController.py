import services.database as db
import bcrypt

ID_CARGO_CENTRAL = 2 

def Adicionar(central):
    try:
        senha_bytes = central.senha.encode('utf-8') 
        
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        
        senha_hash_str = senha_hash.decode('utf-8')

        sql_central = "INSERT INTO Central (nome, status) VALUES (?, 1)"
        db.cursor.execute(sql_central, central.nome)
        
        sql_perfil = """
            INSERT INTO Perfil (idCargo, nome, usuario, senha, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        db.cursor.execute(sql_perfil, ID_CARGO_CENTRAL, central.nome, central.usuario, senha_hash_str)

        db.cnxn.commit()
        return True

    except Exception as e:
        print(f"Erro ao adicionar Central: {e}")
        db.cnxn.rollback()
        return False

def SelecionarNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central")

    return db.cursor.fetchall()