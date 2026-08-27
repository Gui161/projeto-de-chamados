import streamlit as st
from datetime import datetime
import sys
import os
import time
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.funcoes import abrir_chamado, listar_chamados, buscar_chamados_por_data


st.set_page_config(layout="wide", page_title="chamados/suporte")

if "usuario" not in st.session_state:
    st.error("Você precisa estar logado para acessar esta página.")
    time.sleep(2)
    st.switch_page("pages/login.py")

                        
                                

data_abertura = datetime.now()
data_abertura = data_abertura.date()
data_abertura = data_abertura.strftime("%d/%m/%y")

usuario = st.session_state["usuario"]

abas = st.tabs(["Novo chamado", "Listar chamados", "Análise de chamados"])

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
            filtro_data = st.date_input(label="Filtrar por datas", format="DD/MM/YYYY")
            data_escolhida = str(filtro_data)
            mes_escolhido = data_escolhida[5:7]
            ano_escolhido = data_escolhida[0:4]
            data_final_escolhida = (f"{mes_escolhido}/{ano_escolhido}")   
                       
            filtro_status = st.multiselect(label="Filtar por status", options=["ABERTO 🟢", "EM ANDAMENTO 🟡", "FECHADO 🔴"])
            for c in chamado:
                data_chamado = str(c['data_abertura'][3:])
                if data_final_escolhida == data_chamado:
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


with abas[2]:
    st.title("Análise de chamados", text_alignment="center", )
    with st.container(border=True):
        colunas = st.columns(4)
        with colunas[0]:
            data_escolhida = st.date_input(label="Escolha um mês para filtrar.", format="DD/MM/YYYY", width=200)
            buscar_mes_btn = st.button("Buscar")
        
        with colunas[2]:
             
            if buscar_mes_btn:
                st.write("Quantidade de chamados")
                data_escolhida = str(data_escolhida)
                mes_escolhido = data_escolhida[5:7]
                ano_escolhido = data_escolhida[0:4]
                resultado = buscar_chamados_por_data(mes_escolhido, ano_escolhido)
                with st.container(border=True, width=165, height=80):
                    st.subheader(len(resultado["resultado"]), text_alignment="center")
                    
        with colunas[1]:
            if buscar_mes_btn:
                st.write("Chamados Finalizados.")
                data_escolhida = str(data_escolhida)
                mes_escolhido = data_escolhida[5:7]
                ano_escolhido = data_escolhida[0:4]
                resultado = buscar_chamados_por_data(mes_escolhido, ano_escolhido)
                chamados = resultado["resultado"]
                cont = 0
                for c in chamados:
                    if "FECHADO" in c[3]:
                        cont +=1
                with st.container(border=True, width=165, height=80):
                    st.subheader((cont), text_alignment="center")
                
                        
        
        
        with colunas[3]:
            if buscar_mes_btn:
                st.write("Média de tempo por chamado.")
                data_escolhida = str(data_escolhida)
                mes_escolhido = data_escolhida[5:7]
                ano_escolhido = data_escolhida[0:4]
                resultado = buscar_chamados_por_data(mes_escolhido, ano_escolhido)
                if resultado["status"] == "sucesso":
                    qtdd_horas_total = []
                    chamados_mes = resultado['resultado']
                    for c in chamados_mes:
                        if "FECHADO" in c[3]:
                            qtdd_horas_total.append(c[8]*60)
                    
                    if qtdd_horas_total:
                        media_horas_chamado = (sum(qtdd_horas_total)/len(qtdd_horas_total))
                        
                        with st.container(border=True, width=250, height=80):
                            
                            st.subheader(f'{media_horas_chamado:.2f} minutos', text_alignment="center")
    # -- Tabela de visualização          
            
    if buscar_mes_btn:
        data_escolhida = str(data_escolhida)
        mes_escolhido = data_escolhida[5:7]
        ano_escolhido = data_escolhida[0:4]
        resultado = buscar_chamados_por_data(mes_escolhido, ano_escolhido)
        if resultado["status"] == "sucesso":
            chamados_mes = resultado["resultado"]
            if chamados_mes != []:
                colunas = ["ID", "Tipo","Descição","Status", "usuario id", "Data de Abertura", "Setor", "Responsavel", "Tempo gasto", "Solução" ]
                df = pd.DataFrame(chamados_mes, columns=colunas)
                st.dataframe(df, column_order=("Tipo","Descição","Data de Abertura", "Setor", "Status"), height="content")
                
            else:
                st.info("Não existem registros para esta data.")
        else:
            st.error(resultado["mensagem"])

                
    

                
                        
                    
            
    