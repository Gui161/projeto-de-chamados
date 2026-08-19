import streamlit as st
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.funcoes import fazer_login


st.title("Sistema de chamados Intermetro")

if "usuario" not in st.session_state:
    with st.form("formulario_login"):
        email = st.text_input(label="E-mail", value="@intermetro.com.br", key="email", persist_state="session")
        senha = st.text_input(label="Senha", type="password",key="senha", persist_state="session" )
        st.write("---")
        logar_btn = st.form_submit_button(label="Login", width="stretch")



    if logar_btn:
        resultado = fazer_login(email, senha)
        if resultado["status"] == "logado":
            st.session_state["usuario"] = resultado
            st.success(f"Bem vindo {resultado["nome"]} você tem permições de {resultado["acesso"]}")
            time.sleep(2)
            
            # ---- Ir para as outras paginas
            if resultado["acesso"] == "suporte":
                st.switch_page("pages/tela_suporte.py")
            elif resultado["acesso"] == "admin":
                st.switch_page("pages/tela_admin.py")
            elif resultado["acesso"] == "usuario":
                st.switch_page("pages/tela_usuario.py")   
            
                
            
            
        else:
            st.error(resultado["mensagem"])
else:
    st.info("Você ja esta logado")
    
    
 