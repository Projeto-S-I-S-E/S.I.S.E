import services.database as db
import bcrypt

ID_CARGO_PLANTONISTA = 3

def Adicionar(plantonista):
    try:
        senha_bytes = plantonista.senha.encode('utf-8') 
        
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        
        senha_hash_str = senha_hash.decode('utf-8')

        sql_plantonista = "INSERT INTO Plantonista (idRegional, nome, status) VALUES (?, ?, 1)"
        db.cursor.execute(sql_plantonista, plantonista.regional, plantonista.nome)
        
        sql_perfil = """
            INSERT INTO Perfil (idCargo, nome, usuario, senha, status) 
            VALUES (?, ?, ?, ?, 1)
        """
        db.cursor.execute(sql_perfil, ID_CARGO_PLANTONISTA, plantonista.nome, plantonista.usuario, senha_hash_str) 

        db.cnxn.commit()
        return True

    except Exception as e:
        print(f"Erro ao adicionar Plantonista: {e}")
        db.cnxn.rollback()
        return False
    
def Inativar(idPlantonista):
    try:
        sql_update_plantonista = "UPDATE Plantonista SET status = 0 WHERE idPlantonista = ?"
        db.cursor.execute(sql_update_plantonista, idPlantonista)

        sql_select_nome = "SELECT nome FROM Plantonista WHERE idPlantonista = ?"
        db.cursor.execute(sql_select_nome, idPlantonista)
        nome_plantonista = db.cursor.fetchone()[0]

        sql_update_perfil = "UPDATE Perfil SET status = 0 WHERE nome = ? AND idCargo = 3"
        db.cursor.execute(sql_update_perfil, nome_plantonista)

        db.cnxn.commit()
        return True
    
    except Exception as e:
        print(f"Erro ao inativar Plantonista: {e}")
        db.cnxn.rollback()
        return False

def Atualizar(plantonista_obj, nova_senha=None):
    try:
        sql_nome_antigo = "SELECT nome FROM Plantonista WHERE idPlantonista = ?"
        nome_antigo = db.cursor.execute(sql_nome_antigo, plantonista_obj.id).fetchone()[0]

        sql_update_plantonista = "UPDATE Plantonista SET idRegional = ?, nome = ? WHERE idPlantonista = ?"

        parametros_plantonista = (
            plantonista_obj.regional, 
            plantonista_obj.nome, 
            plantonista_obj.id
        )

        db.cursor.execute(sql_update_plantonista, parametros_plantonista)

        sql_update_perfil = "UPDATE Perfil SET nome = ?, usuario = ? WHERE nome = ? AND idCargo = ?"

        parametros_perfil = (
            plantonista_obj.nome,          
            plantonista_obj.usuario,      
            nome_antigo,                
            ID_CARGO_PLANTONISTA
        )

        db.cursor.execute(sql_update_perfil, parametros_perfil)
        
        if nova_senha:
            senha_bytes = nova_senha.encode('utf-8')
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
            
            sql_update_senha = "UPDATE Perfil SET senha = ? WHERE nome = ? AND idCargo = ?"

            parametros_senha = (
                senha_hash, 
                plantonista_obj.nome, 
                ID_CARGO_PLANTONISTA
            )

            db.cursor.execute(sql_update_senha, parametros_senha)

        db.cnxn.commit()
        return True

    except Exception as e:
        print(f"Erro ao atualizar Plantonista: {e}")
        db.cnxn.rollback()
        return False

def SelecionarPorId(idPlantonista):
    sql_plantonista = """
        SELECT 
            P.idPlantonista, 
            P.idRegional, 
            P.nome, 
            P.status,
            R.nome AS nomeRegional
        FROM Plantonista P
        INNER JOIN Regional R ON P.idRegional = R.idRegional
        WHERE P.idPlantonista = ?
    """
    plantonista_resultado = db.cursor.execute(sql_plantonista, idPlantonista).fetchone()

    if not plantonista_resultado:
        return None

    nome_plantonista = plantonista_resultado[2]
    sql_perfil = """
        SELECT usuario, senha 
        FROM Perfil 
        WHERE nome = ? AND idCargo = ?
    """
    perfil_resultado = db.cursor.execute(sql_perfil, (nome_plantonista, ID_CARGO_PLANTONISTA)).fetchone()

    plantonista_dados = {
        'id': plantonista_resultado[0],
        'regional': plantonista_resultado[1],
        'nome': plantonista_resultado[2],
        'status': plantonista_resultado[3],
        'nomeRegional': plantonista_resultado[4],
        'usuario': perfil_resultado[0] if perfil_resultado else '',
    }

    return plantonista_dados

def SelecionarNome():
    db.cursor.execute("SELECT idPlantonista, nome FROM Plantonista WHERE status = 1")

    return db.cursor.fetchall()

def SelecionarRegionalIdNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional WHERE status = 1")

    return db.cursor.fetchall()