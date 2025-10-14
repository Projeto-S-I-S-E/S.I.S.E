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
    
def Inativar(idCentral):
    try:
        sql_update_central = "UPDATE Central SET status = 0 WHERE idCentral = ?"
        db.cursor.execute(sql_update_central, idCentral)

        sql_select_nome = "SELECT nome FROM Central WHERE idCentral = ?"
        db.cursor.execute(sql_select_nome, idCentral)
        nome_central = db.cursor.fetchone()[0]

        sql_update_perfil = "UPDATE Perfil SET status = 0 WHERE nome = ? AND idCargo = 2"
        db.cursor.execute(sql_update_perfil, nome_central)

        db.cnxn.commit()
        return True
    
    except Exception as e:
        print(f"Erro ao inativar Central: {e}")
        db.cnxn.rollback()
        return False

def SelecionarNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central WHERE status = 1")

    return db.cursor.fetchall()