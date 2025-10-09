import services.database as db
import bcrypt

ID_CARGO_PLANTONISTA = 3

def Adicionar(plantonista):
    try:
        senha_bytes = plantonista.senha.encode('utf-8') 
        
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        
        senha_hash_str = senha_hash.decode('utf-8')

        sql_plantonista = "INSERT INTO Plantonista (idRegional, nome, status) VALUES (?, ?, 1)"
        db.cursor.execute(sql_plantonista, plantonista.regiao, plantonista.nome)
        
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

def SelecionarNome():
    db.cursor.execute("SELECT idPlantonista, nome FROM Plantonista")

    return db.cursor.fetchall()

def SelecionarRegionalIdNome():
    db.cursor.execute("SELECT idRegional, nome FROM Regional")

    return db.cursor.fetchall()