import services.database as db

def AutenticarUsuario(usuario, senha):
    sql = "SELECT idCargo FROM Perfil WHERE usuario = ? AND senha = ?"
    db.cursor.execute(sql, usuario, senha)
    resultado = db.cursor.fetchone()
    
    if resultado:
        return resultado[0] 
    else:
        return None