import streamlit as st
from datetime import datetime

from sqlalchemy import or_, select

from db import SessionLocal
from models import Occurrence


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
            occurrence_type = st.selectbox("Tipo", ["Todos", "Erro de sistema", "Erro de operação", "Outros"])
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
        stmt = select(Occurrence)

        if use_dates:
            if start_date > end_date:
                st.warning("Data inicial maior que a data final. Ajuste os filtros.")
                return
            stmt = stmt.where(
                Occurrence.occurrence_date >= start_date.strftime("%Y-%m-%d"),
                Occurrence.occurrence_date <= end_date.strftime("%Y-%m-%d"),
            )

        if occurrence_type != "Todos":
            stmt = stmt.where(Occurrence.occurrence_type == occurrence_type)

        if term.strip():
            like = f"%{term.strip()}%"
            stmt = stmt.where(
                or_(
                    Occurrence.title.like(like),
                    Occurrence.temporary_solution.like(like),
                    Occurrence.definitive_solution.like(like),
                    Occurrence.username.like(like),
                )
            )

        stmt = stmt.order_by(
            Occurrence.occurrence_date.desc(),
            Occurrence.registered_at.desc(),
        )

        with SessionLocal() as session:
            results = session.scalars(stmt).all()

        if not results:
            st.info("Nenhuma ocorrência encontrada com esses filtros.")
            return

        st.write(f"**{len(results)} ocorrência(s) encontrada(s)**")

        for row in results:
            with st.expander(
                f"{_format_date(row.occurrence_date)} — {row.title} "
                f"({row.occurrence_type}) — {row.username}"
            ):
                st.write(f"**Data da ocorrência:** {_format_date(row.occurrence_date)}")
                st.write(f"**Tipo:** {row.occurrence_type}")
                st.write(f"**Solução provisória:** {row.temporary_solution or '—'}")
                st.write(f"**Solução definitiva:** {row.definitive_solution or '—'}")
                st.write(f"**Registrado por:** {row.username}")
                st.write(f"**Registrado em:** {_format_datetime(row.registered_at)}")

 
