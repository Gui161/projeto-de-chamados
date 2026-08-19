import sqlite3
import os





def fazer_login(email, senha):
    
    con = sqlite3.connect(r"C:\Users\usuario\Desktop\sistema de chamados\projeto de chamados\database\chamados.db")
    cursor = con.cursor()

    try:
        cursor.execute("SELECT id, nome, acesso, senha  FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            id, nome, acesso, senha_db = usuario
            if senha == senha_db:
                return {"status": "logado", "id":id, "nome":nome, "acesso":acesso, "email":email}
            else:
                return {"status":"Erro", "mensagem":"Senha incorreta"}
        else:
            return{"status":"Erro", "mensagem":"Usuario não encontrado"}
    except Exception as erro:
        
        return {f"status":"Erro", "mensagem":"Erro ao efetuar login {erro}"}
    
    
def abrir_chamado(tipo, descricao, usuario_id, data_abertura, departamento):
    con = sqlite3.connect(r"C:\Users\usuario\Desktop\sistema de chamados\projeto de chamados\database\chamados.db")
    cursor = con.cursor()

    try:
        cursor.execute("INSERT INTO chamados(tipo, descricao, status, usuario_id, data_abertura, departamento) VALUES (?, ?, ?, ?, ?, ?)",
                       (tipo, descricao,"ABERTO", usuario_id, data_abertura, departamento))
        con.commit()
        return {"status":"sucesso", "mensagem":"Chamado aberto com sucesso!"}
    except Exception as e:
        return {"status":"erro", "mensagem":f"Erro ao abrir chamado {e}"}
    

def listar_chamados_usuario(usuario_id):
    con = sqlite3.connect(r"C:\Users\usuario\Desktop\sistema de chamados\projeto de chamados\database\chamados.db")
    cursor = con.cursor()
    try:
        cursor.execute("SELECT tipo, descricao, status, data_abertura, departamento FROM chamados WHERE usuario_id = ?", (usuario_id,))
        linhas = cursor.fetchall()
        chamados_usuario = [{
            "tipo":linha[0],
            "Descricao":linha[1],
            "status":linha[2],
            "data_abertura":linha[3],
            "departamento":linha[4]
            
        }for linha in linhas]
        return {"status":"sucesso","chamados":chamados_usuario}
    except Exception as e:
        print(e)
        return {"status":"erro", "mensagem":"Erro ao carregar chamados"}
   



