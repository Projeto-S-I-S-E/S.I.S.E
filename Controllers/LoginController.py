import services.database as db
import bcrypt

def AutenticarUsuario(usuario, senha):
    sql = "SELECT idCargo, senha FROM Perfil WHERE usuario = ?"
    db.cursor.execute(sql, usuario)
    resultado = db.cursor.fetchone()

    if resultado:
        id_cargo = resultado[0]
        senha_hash = resultado[1]

        try:
            senha_bytes = senha.encode('utf-8')
            hash_bytes = senha_hash.encode('utf-8')

            if bcrypt.checkpw(senha_bytes, hash_bytes):
                return id_cargo
            else:
                return None
        except ValueError:
            return None
    else:
        return None