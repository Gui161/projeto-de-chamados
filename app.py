import streamlit as st
from database.funcoes import fazer_login



pg = st.navigation([
    st.Page('./pages/login.py', title="login"),
    st.Page("pages/tela_admin.py", title="Admin"),
    st.Page("pages/tela_usuario.py", title="Usuário"),
    st.Page("pages/tela_suporte.py", title="Suporte"),
    
],position='hidden')

pg.run()


