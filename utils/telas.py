import streamlit as st
import time

def novo_chamado():
    if "usuario" not in st.session_state:
        st.error("Você precisa estar logado para acessar esta página.")
        time.sleep(2)
        st.switch_page("pages/login.py")