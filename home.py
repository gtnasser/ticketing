import streamlit as st
from database import get_connection


def run() -> None:
    st.subheader("🏠 Welcome to Ticketing - Registro de Ocorrências", divider='rainbow')


    with get_connection() as conn:
        total = conn.execute(
            "SELECT COUNT(*) AS n1 FROM occurrences"
        ).fetchone()["n1"]
        perm_qty = conn.execute(
            "SELECT COUNT(*) AS n2 FROM occurrences WHERE NOT trim(definitive_solution) = ''"
        ).fetchone()["n2"]
        temp_qty = conn.execute(
            "SELECT COUNT(*) AS n2 FROM occurrences WHERE NOT trim(temporary_solution) = ''"
        ).fetchone()["n2"]
        err_sis = conn.execute(
            "SELECT COUNT(*) AS n FROM occurrences WHERE type = 'Erro de sistema'"
        ).fetchone()["n"]
        err_oper = conn.execute(
            "SELECT COUNT(*) AS n FROM occurrences WHERE type = 'Erro de operação'"
        ).fetchone()["n"]
        err_na = conn.execute(
            "SELECT COUNT(*) AS n FROM occurrences WHERE type = 'Outros'"
        ).fetchone()["n"]


    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de ocorrências", total, border=True) # , width=300)
    with col2:
        st.metric("Total Resolvidas", perm_qty, border=True)
    with col3:
        st.metric("Total Necessário Revisão", temp_qty, border=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Erro de sistema", err_sis, border=True)
    with col2:
        st.metric("Erro de operação", err_oper, border=True)
    with col3:
        st.metric("Outros", err_na, border=True)


