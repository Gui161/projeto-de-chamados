import streamlit as st
from datetime import datetime
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.funcoes import abrir_chamado, listar_chamados, iniciar_chamado, finalizar_chamado, buscar_responsavel


if "chamado_id" in st.session_state:
    usuario = st.session_state["usuario"]    
    
    retorno = listar_chamados()
    if retorno['status'] == "sucesso":
        chamado = retorno["chamados"]
        for c in chamado:
            if c["id"] == st.session_state["chamado_id"]:
                chamado_escolhido = c
                with st.form("formulario_chamado", ):
                    print(c)
                    st.title(f"Relatorio do chamado [ {c['descricao']} ]", text_alignment="center")
                    st.text_input(label="Solicitante", value=c['usuario'])
                    st.text_input(label="E-mail", value=c['email'])
                    st.text_input(label="Tipo", value=c["tipo"])
                    st.text_area(label="Descrição", value=c['descricao'])
                    
                    colunas = st.columns(3)
                    
                    
                    
                    
                    with colunas[0]:
                        st.write(f"Setor:    {c['setor']} ")
                        voltar_btn = st.form_submit_button("Voltar para chamados", use_container_width=True)
                        if voltar_btn:
                            st.session_state["chamado_id"] = None
                            st.switch_page("pages/tela_suporte.py")
                            
                        
                            
                            
                            
                            
                            
                            
                    with colunas[1]:
                        st.write(f"Status {c['status']}")
                        if c['status'] in ["ABERTO", "ABERTO 🟢"]:
                            iniciar_chamado_btn = st.form_submit_button(label="Iniciar Realização do chamado", use_container_width=True)
                            if iniciar_chamado_btn:
                                
                                inicio = iniciar_chamado(st.session_state["chamado_id"], usuario['id'])
                                if inicio['status'] == "sucesso":
                                    st.success(f"Chamado ID: {c['id']}, Iniciado por {usuario['nome']}")
                                else:
                                    st.error(inicio["mensagem"])
                        elif c['status'] in ["EM ANDAMENTO 🟡", "EM ANDAMENTO"]:
                            responsavel = buscar_responsavel(c['id'])
                            if responsavel:
                                st.write(f"Chamado em execução por: {responsavel['resultado'][0]} ⌛")
                        
                        
                        
                        
                        
                    with colunas[2]:
                        st.write(f"Data de abertura {c['data_abertura']}")
                        if c['status'] in ["ABERTO" , "EM ANDAMENTO" , "ABERTO 🟢" , "EM ANDAMENTO 🟡"]:
                            finalizar_btn = st.form_submit_button(label= "Finalizar chamado", use_container_width=True)
                            
                            descricao_solucao = st.text_input(label="Descreva como Solucionou o problema")
                            tempo_minuto = st.number_input("Tempo gasto(em minutos)", min_value=0, step=2)
                            tempo_horas = tempo_minuto / 60
                            
                            
                            if finalizar_btn:
                                finalizar = finalizar_chamado(st.session_state['chamado_id'], usuario['id'], tempo_horas, descricao_solucao)
                                if finalizar['status'] == "sucesso":
                                    st.success(f"Chamdo {c['id']}, finalizado por {usuario['nome']}")
                                else:
                                    st.error(finalizar['mensagem'])
                                
                                
                        
                    
                    
                    
                    
    else:
        st.error(retorno['mensagem'])

else:
    st.error("Nenhum chamado selecionado")
     