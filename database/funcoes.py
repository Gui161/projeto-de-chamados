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
    


print(abrir_chamado("Software", "Meu aoki parou", 1, "19/08/2026", 'P&D'))    


