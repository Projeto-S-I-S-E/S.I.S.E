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

def SelecionarNome():
    db.cursor.execute("SELECT idPlantonista, nome FROM Plantonista WHERE status = 1")

    return db.cursor.fetchall()

def SelecionarRegionalIdNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional WHERE status = 1")

    return db.cursor.fetchall()