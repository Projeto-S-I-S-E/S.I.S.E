import services.database as db
import bcrypt

def AutenticarUsuario(usuario, senha):
    sql = "SELECT P.idCargo, C.nome, P.senha FROM Perfil P LEFT JOIN Cargo C ON C.idCargo = P.idCargo WHERE usuario = ?"
    db.cursor.execute(sql, usuario)
    resultado = db.cursor.fetchone()

    if resultado:
        id_cargo = resultado[0]
        nome_usuario = resultado[1]
        senha_hash = resultado[2]

        try:
            senha_bytes = senha.encode('utf-8')
            hash_bytes = senha_hash.encode('utf-8')

            if bcrypt.checkpw(senha_bytes, hash_bytes):
                return id_cargo, nome_usuario
            else:
                return None, None
        except ValueError:
            return None, None
    else:
        return None, None