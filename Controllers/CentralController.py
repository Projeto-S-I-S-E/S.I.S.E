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
    
def Atualizar(central_obj, nova_senha=None):
    try:
        sql_nome_antigo = "SELECT nome FROM Central WHERE idCentral = ?"
        nome_antigo = db.cursor.execute(sql_nome_antigo, central_obj.id).fetchone()[0]

        sql_update_central = "UPDATE Central SET nome = ? WHERE idCentral = ?"

        parametros_central = (
            central_obj.nome,
            central_obj.id
        )

        db.cursor.execute(sql_update_central, parametros_central)

        sql_update_perfil = "UPDATE Perfil SET nome = ?, usuario = ? WHERE nome = ? AND idCargo = ?"

        parametros_perfil = (
            central_obj.nome,
            central_obj.usuario,
            nome_antigo,
            ID_CARGO_CENTRAL
        )

        db.cursor.execute(sql_update_perfil, parametros_perfil)
        
        if nova_senha:
            senha_bytes = nova_senha.encode('utf-8')
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
            
            sql_update_senha = "UPDATE Perfil SET senha = ? WHERE nome = ? AND idCargo = ?"

            parametros_senha = (
                senha_hash,
                central_obj.nome,
                ID_CARGO_CENTRAL
            )

            db.cursor.execute(sql_update_senha, parametros_senha)

        db.cnxn.commit()
        return True

    except Exception as e:
        print(f"Erro ao atualizar Central: {e}")
        db.cnxn.rollback()
        return False
    
def SelecionarPorId(idCentral):
    sql_central = "SELECT idCentral, nome, status FROM Central WHERE idCentral = ?"
    central_resultado = db.cursor.execute(sql_central, idCentral).fetchone()

    if not central_resultado:
        return None

    nome_central = central_resultado[1]
    sql_perfil = """
        SELECT usuario, senha 
        FROM Perfil 
        WHERE nome = ? AND idCargo = ?
    """
    perfil_resultado = db.cursor.execute(sql_perfil, nome_central, ID_CARGO_CENTRAL).fetchone()

    central_dados = {
        'id': central_resultado[0],
        'nome': central_resultado[1],
        'status': central_resultado[2],
        'usuario': perfil_resultado[0] if perfil_resultado else '',
    }

    return central_dados

def SelecionarNome():
    db.cursor.execute("SELECT idCentral, nome FROM Central WHERE status = 1")

    return db.cursor.fetchall()