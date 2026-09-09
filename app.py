import streamlit as st

from db import init_db
from auth import get_current_user, is_auth
from login import do_login, do_logout

# ---------- paginas ----------
import about
import home
import ticket_register
import ticket_search
import report01

st.set_page_config(page_title="Ticketing", page_icon="📋", layout="wide")

# ---------- Inicializa banco de dados ----------
init_db()

# ---------- Controle de sessão ----------
if not is_auth():
    do_login()
    st.stop()

# ---------- Menu lateral ----------
PAGES = {
    "🏠 Home": home.run,
    "📝 Cadastrar Ocorrência": ticket_register.run,
    "🔍 Pesquisar Ocorrências": ticket_search.run,
    "📊 Relatório e Análises": report01.run,    
    "ℹ️ Sobre": about.run,
}
with st.sidebar:
    st.title(f"👤 {get_current_user()}")
    page = st.radio("Menu", list(PAGES.keys()))
    if st.button("Sair"):
        do_logout()
        #st.rerun() ja chamado em do_logout

# ---------- Roteamento ----------
PAGES[page]()
