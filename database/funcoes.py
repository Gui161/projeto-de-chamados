import sqlite3
import os





def fazer_login(email, senha):
    caminho_db = os.path.join(os.path.dirname(__file__), "..", "chamados.db")
    con = sqlite3.connect(r"C:\Users\usuario\Desktop\sistema de chamados\database\chamados.db")
    cursor = con.cursor()

    try:
        cursor.execute("SELECT id, nome, acesso, senha  FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            id, nome, acesso, senha_db = usuario
            if senha == senha_db:
                return {"status": "logado", "id":id, "nome":nome, "acesso":acesso}
            else:
                return {"status":"Erro", "mensagem":"Senha incorreta"}
        else:
            return{"status":"Erro", "mensagem":"Usuario não encontrado"}
    except Exception as erro:
        
        return {f"status":"Erro", "mensagem":"Erro ao efetuar login {erro}"}
    
    



