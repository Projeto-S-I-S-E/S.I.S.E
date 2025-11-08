import services.database as db
import bcrypt

def AutenticarUsuario(usuario, senha):
    sql = "SELECT u.idUsuario, p.idCargo, p.nome, p.senha FROM Perfil p LEFT JOIN Usuario u ON u.nome = p.nome WHERE usuario = ?"
    db.cursor.execute(sql, usuario)
    resultado = db.cursor.fetchone()

    if resultado:
        id_perfil = resultado[0]
        id_cargo = resultado[1]
        nome_usuario = resultado[2]
        senha_hash = resultado[3]

        try:
            senha_bytes = senha.encode('utf-8')
            hash_bytes = senha_hash.encode('utf-8')

            if bcrypt.checkpw(senha_bytes, hash_bytes):
                return id_perfil, id_cargo, nome_usuario
            else:
                return None, None
        except ValueError:
            return None, None
    else:
        return None, None