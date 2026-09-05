import streamlit as st

from database import init_db, get_connection
from auth import get_current_user, is_auth
from login import do_login, do_logout

# ---------- paginas ----------
import about
import home
import ticket_register
import ticket_search

st.set_page_config(page_title="Ticketing", page_icon="📋", layout="wide")

# ---------- Inicializa banco de dados ----------
#TODO: init_db()

# ---------- Controle de sessão ----------
if not is_auth():
    do_login()
    st.stop()

# ---------- Menu lateral ----------
with st.sidebar:
    st.title(f"👤 {get_current_user()}")
    page = st.radio("Manu", ["📝 Cadastrar Ocorrência", "🔍 Pesquisar Ocorrências", "ℹ️ Sobre", ], index=None)
    if st.button("Sair"):
        do_logout()
        st.rerun()

# ---------- Roteamento ----------
if page:
    if page.startswith("📝"):
        ticket_register.run()
    elif page.startswith("🔍"):
        ticket_search.run()
    elif page.startswith("ℹ️"):
        about.run()
else:
    home.run()
