import csv
import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import func, select

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

def _to_csv(rows) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "Data", "Tipo", "Título", "Solução provisória",
        "Solução definitiva", "Usuário", "Registrado em",
    ])
    for row in rows:
        writer.writerow([
            _format_date(row.occurrence_date),
            row.occurrence_type,
            row.title,
            row.temporary_solution,
            row.definitive_solution,
            row.username,
            _format_datetime(row.registered_at),
        ])
    return buffer.getvalue()

def run() -> None:
    st.subheader("📊 Relatórios e Análises", divider='rainbow')

    with SessionLocal() as session:
        users = session.scalars(
            select(Occurrence.username).distinct().order_by(Occurrence.username)
        ).all()

    with st.form("report_filters"):
        col1, col2 = st.columns(2)
        with col1:
            occurrence_type = st.selectbox(
                "Tipo", ["Todos", "Erro de sistema", "Erro de operação", "Outros"]
            )
        with col2:
            selected_users = st.multiselect(
                "Usuários", users, default=users,
                placeholder="Selecione os usuários",
            )

        use_dates = st.checkbox("Filtrar por período")
        if use_dates:
            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("Data inicial")
            with col4:
                end_date = st.date_input("Data final")

        submit = st.form_submit_button("🔎 Gerar relatório")

    if not submit:
        return

    if use_dates and start_date > end_date:
        st.warning("Data inicial maior que a data final. Ajuste os filtros.")
        return

    conditions = []
    if occurrence_type != "Todos":
        conditions.append(Occurrence.occurrence_type == occurrence_type)
    if selected_users:
        conditions.append(Occurrence.username.in_(selected_users))
    if use_dates:
        conditions.append(Occurrence.occurrence_date >= start_date.strftime("%Y-%m-%d"))
        conditions.append(Occurrence.occurrence_date <= end_date.strftime("%Y-%m-%d"))

    with SessionLocal() as session:
        total = session.scalars(
            select(func.count()).select_from(Occurrence).where(*conditions)
        ).one()

        rows_month = session.execute(
            select(
                func.substr(Occurrence.occurrence_date, 1, 7).label("month"),
                func.count().label("total"),
            )
            .where(*conditions)
            .group_by("month")
            .order_by("month")
        ).all()

        rows_user_month = session.execute(
            select(
                func.substr(Occurrence.occurrence_date, 1, 7).label("month"),
                Occurrence.username,
                func.count().label("total"),
            )
            .where(*conditions)
            .group_by("month", Occurrence.username)
            .order_by("month", Occurrence.username)
        ).all()

        rows = session.scalars(
            select(Occurrence)
            .where(*conditions)
            .order_by(Occurrence.occurrence_date.desc(), Occurrence.registered_at.desc())
        ).all()

    st.metric("Ocorrências no período", total, border=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.write("**Evolução mensal**")
        if rows_month:
            df_month = pd.DataFrame(
                [(m, qtd) for m, qtd in rows_month],
                columns=["Mês", "Quantidade"],
            )
            fig_month = px.bar(df_month, x="Mês", y="Quantidade")
            fig_month.update_xaxes(type="category", categoryorder="category ascending")
            st.plotly_chart(fig_month, width="stretch")
        else:
            st.info("Sem dados para o período.")

    with col_b:
        st.write("**Ocorrências por usuário por mês**")
        if rows_user_month:
            df_user_month = pd.DataFrame(
                [(m, u, qtd) for m, u, qtd in rows_user_month],
                columns=["Mês", "Usuário", "Quantidade"],
            )
            fig_user_month = px.line(
                df_user_month,
                x="Mês",
                y="Quantidade",
                color="Usuário",
                markers=True,
            )
            fig_user_month.update_xaxes(type="category", categoryorder="category ascending")
            st.plotly_chart(fig_user_month, width="stretch")
        else:
            st.info("Sem dados para o período.")

    st.write("**Registros no período**")
    if rows:
        st.dataframe(
            [
                {
                    "Data": _format_date(r.occurrence_date),
                    "Tipo": r.occurrence_type,
                    "Título": r.title,
                    "Solução provisória": r.temporary_solution or "—",
                    "Solução definitiva": r.definitive_solution or "—",
                    "Usuário": r.username,
                    "Registrado em": _format_datetime(r.registered_at),
                }
                for r in rows
            ],
            width="stretch",
        )
        st.download_button(
            "⬇️ Baixar CSV",
            data=_to_csv(rows),
            file_name="relatorio_ocorrencias.csv",
            mime="text/csv",
        )
    else:
        st.info("Nenhuma ocorrência encontrada com esses filtros.")