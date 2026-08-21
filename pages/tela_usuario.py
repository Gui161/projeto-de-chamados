import streamlit as st
from datetime import datetime
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.funcoes import abrir_chamado, listar_chamados_usuario

st.set_page_config(layout="wide", page_title="chamados/usuarios")

data_abertura = datetime.now()
data_abertura = data_abertura.date()
data_abertura = data_abertura.strftime("%d/%m/%y")

if "usuario" not in st.session_state:
    st.error("Você precisa estar logado para acessar esta página.")
    st.stop()

usuario = st.session_state["usuario"]

abas = st.tabs(["Novo Chamado", "Meus chamados", "Minhas solicitações"])

with abas[0]: # ---Novo chamado
    with st.form("formulario_de_solicitação", width="stretch", clear_on_submit=True):
        st.markdown("# Novo chamado 📝", text_alignment="center")
        nome = st.text_input(label="Nome:", value=usuario["nome"])
        email = st.text_input(label="email", value=usuario["email"])
        tipo = st.selectbox(label="Selecione o tipo de chamado", options=["Hardware", "Software", "Redes", "Solicitação de compra" ])
        setor = st.pills(label="Setor", options=["Comercial", "Logistica", "Laboratório", "P&D", "Qualidade", "Financeiro", "Manutenção", "Fabricação", "RH", "Compras", "Outros"], default="Laboratório")
        st.write(f"Data de abertura do chamado \n{data_abertura}")
        descricao = st.text_area(label="Descreva sua solicitação", height=200)
        
        
        criar_chamado_btn = st.form_submit_button(label="Abrir chamado", use_container_width="True")
    
    if criar_chamado_btn:
        if descricao != "":
            resultado = abrir_chamado(tipo, descricao, usuario["id"], data_abertura, setor)
            if resultado["status"] == "sucesso":
                st.success(resultado["mensagem"])
                st.balloons()
            else:
                st.error(resultado["mensagem"])
        else:
            st.error("Por favor descreva o motivo do seu chamado.")
        
        
with abas[1]: # --- Listar chamados
    st.title("lista de chamados") 
    chamados = listar_chamados_usuario(usuario["id"])
    if chamados["status"] == "sucesso":
        chamados_usuario = chamados["chamados"]
        
        if chamados_usuario:
            st.dataframe(chamados_usuario)
            
        else:
            st.info("Você ainda não abriu nenhum chamado.")
    else:
        st.error(chamados["mensagem"])
         
       
with abas[2]: # ---- Listar Solicitaçoes
    st.title("Lista de Solicitações")
    chamados = listar_chamados_usuario(usuario["id"])
    if chamados["status"] == "sucesso":
        chamados_usuario = chamados["chamados"]
        if chamados_usuario:
            for c in chamados_usuario:
                if c["status"] == "ABERTO":
                    c["status"] = "ABERTO  🟢"
                elif c["status"] == "FECHADO":
                    c["status"] = "FECHADO  🔴"
                elif c["status"] == "Em ANDAMENTO":
                    c["status"] = "EM ANDAMENTO  🟡"
            solicitacoes_tbl = []
            for solicitacoes in chamados_usuario:
                if solicitacoes["tipo"] == "Solicitação de compra":
                    solicitacoes_tbl.append(solicitacoes)
            if solicitacoes_tbl == []:
                st.info("Você ainda não fez nenhuma solicitação")
            st.table(solicitacoes_tbl)
        else:
            st.info("Você ainda não fez nenhuma solicitação")
    else:
        st.error(chamados["mensagem"])
            
        
        
        