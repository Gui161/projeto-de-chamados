import streamlit as st
from datetime import datetime
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.funcoes import abrir_chamado, listar_chamados

def dados_finalizar_chamado():
    st.popover(label="finalizar chamado")

st.set_page_config(layout="wide", page_title="chamados/suporte")

if "usuario" not in st.session_state:
    st.error("Você precisa estar logado para acessar esta página.")
    st.stop()

    

data_abertura = datetime.now()
data_abertura = data_abertura.date()
data_abertura = data_abertura.strftime("%d/%m/%y")

usuario = st.session_state["usuario"]

abas = st.tabs(["Novo chamado", "listar chamados"])

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


with abas[1]:
    st.markdown("# painel de chamados")
    chamados = listar_chamados()
    if chamados['status'] == "sucesso":
        chamado = chamados['chamados']
        if chamado:
            filtro_status = st.multiselect(label="Filtar por status", options=["ABERTO", "EM ANDAMENTO", "FECHADO"])
            for c in chamado:
                if c['status'] in filtro_status:
                    with st.form(f"chamado {c["id"]}"):
                        colunas = st.columns(3)
                        with colunas[0]:
                            st.write(f"nome: {c['usuario']}")
                            st.write(f"Status atual: {c['status']}")
                            st.write(f"tipo: {c['tipo']}")
                        with colunas[1]:
                            st.write(f"Data de abertura: {c['data_abertura']}")
                            st.write(f"Setor: {c['setor']}")
                            st.write(f"E-mail: {c['email']}")
                        with colunas[2]:
                            st.space(size="small")
                            
                            escolher_chamado = st.form_submit_button(label="Visualizar chamado", use_container_width=True)
                            if escolher_chamado:
                                st.session_state["chamado_id"] = c["id"]
                                st.switch_page("pages/tela_chamado.py")
                            
                            
                
                        
                    
            
    