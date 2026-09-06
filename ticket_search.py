import streamlit as st
from datetime import datetime

from database import get_connection

def _format_date(iso: str) -> str:
    try:
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return iso

def _format_datetime(iso: str) -> str:
    try:
        return datetime.strptime(iso, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return iso

def run() -> None:
    st.subheader("🔍 Pesquisar Ocorrências", divider='rainbow')

    with st.form("filters"):
        col1, col2 = st.columns(2)
        with col1:
            type_ = st.selectbox("Tipo", ["Todos", "Erro de sistema", "Erro de operação", "Outros"])
        with col2:
            term = st.text_input("Buscar em título, soluções ou usuário")

        use_dates = st.checkbox("Filtrar por período")
        if use_dates:
            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("Data inicial")
            with col4:
                end_date = st.date_input("Data final")

        submit = st.form_submit_button("🔎 Buscar")

    if submit:
        query = "SELECT * FROM occurrences WHERE 1=1"
        params = []

        if use_dates:
            if start_date > end_date:
                st.warning("Data inicial maior que a data final. Ajuste os filtros.")
                return
            query += " AND occurrence_date BETWEEN ? AND ?"
            params.extend([start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")])

        if type_ != "Todos":
            query += " AND type = ?"
            params.append(type_)

        if term.strip():
            like = f"%{term.strip()}%"
            query += """ AND (title LIKE ? OR temporary_solution LIKE ?
                          OR definitive_solution LIKE ? OR username LIKE ?)"""
            params.extend([like, like, like, like])

        query += " ORDER BY occurrence_date DESC, registered_at DESC"

        with get_connection() as conn:
            results = conn.execute(query, params).fetchall()

        if not results:
            st.info("Nenhuma ocorrência encontrada com esses filtros.")
            return

        st.write(f"**{len(results)} ocorrência(s) encontrada(s)**")

        for row in results:
            with st.expander(
                f"{_format_date(row['occurrence_date'])} — {row['title']} "
                f"({row['type']}) — {row['username']}"
            ):
                st.write(f"**Data da ocorrência:** {_format_date(row['occurrence_date'])}")
                st.write(f"**Tipo:** {row['type']}")
                st.write(f"**Solução provisória:** {row['temporary_solution'] or '—'}")
                st.write(f"**Solução definitiva:** {row['definitive_solution'] or '—'}")
                st.write(f"**Registrado por:** {row['username']}")
                st.write(f"**Registrado em:** {_format_datetime(row['registered_at'])}")


