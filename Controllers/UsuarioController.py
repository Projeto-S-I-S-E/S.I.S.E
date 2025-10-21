import services.database as db
import bcrypt

ID_CARGO_USUARIO = 4

def Adicionar(usuario):
    try:
        senha_bytes = usuario.senha.encode('utf-8') 
        
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        
        senha_hash_str = senha_hash.decode('utf-8')

        sql_usuario = "INSERT INTO Usuario (nome, telefone) VALUES (?, ?)"
        db.cursor.execute(sql_usuario, usuario.nome, usuario.telefone)
        
        sql_perfil = """
            INSERT INTO Perfil (idCargo, nome, usuario, senha, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        db.cursor.execute(sql_perfil, ID_CARGO_USUARIO, usuario.nome, usuario.email, senha_hash_str)

        db.cnxn.commit()
        return True

    except Exception as e:
        print(f"Erro ao adicionar Usuario: {e}")
        db.cnxn.rollback()
        return False