import streamlit as st
from sqlalchemy import func, select

from db import SessionLocal
from models import Occurrence


def run() -> None:
#    st.write(f"Bem-vindo, **{get_current_user()}**!")
    st.subheader("🏠 Welcome to Ticketing - Registro de Ocorrências", divider='rainbow')

    with SessionLocal() as session:

        total = session.scalars(
            select(func.count()).select_from(Occurrence)
        ).one()

        rows_type = session.execute(
            select(Occurrence.occurrence_type, func.count().label("total"))
            .group_by(Occurrence.occurrence_type)
            .order_by(func.count().desc())
        ).all()

        rows_user = session.execute(
            select(Occurrence.username, func.count().label("total"))
            .group_by(Occurrence.username)
            .order_by(func.count().desc())
        ).all()

        count_definitive = session.scalars(
            select(func.count())
            .select_from(Occurrence)
            .where(Occurrence.definitive_solution != "")
        ).one()

        count_temporary = session.scalars(
            select(func.count())
            .select_from(Occurrence)
            .where(Occurrence.temporary_solution != "")
        ).one()

        count_both = session.scalars(
            select(func.count())
            .select_from(Occurrence)
            .where(
                Occurrence.definitive_solution != "",
                Occurrence.temporary_solution != "",
            )
        ).one()

        count_none = session.scalars(
            select(func.count())
            .select_from(Occurrence)
            .where(
                Occurrence.definitive_solution == "",
                Occurrence.temporary_solution == "",
            )
        ).one()

    st.metric("Total de ocorrências", total, border=True, width=300)

    col1, col2, col3 = st.columns(3)

    with col1:
        if rows_type:
            st.write("**Ocorrências por Tipo:**")
            st.dataframe(
                [{"Tipo": tipo, "Quantidade": qtd} for tipo, qtd in rows_type],
                width="stretch",
            )

    with col2:
        if rows_user:
            st.write("**Ocorrências por Usuário:**")
            st.dataframe(
                [{"Usuário": user, "Quantidade": qtd} for user, qtd in rows_user],
                width="stretch",
            )

    with col3:
        st.write("**Soluções registradas:**")
        st.dataframe(
            [
                {"Situação": "Com solução definitiva", "Quantidade": count_definitive},
                {"Situação": "Com solução provisória", "Quantidade": count_temporary},
                {"Situação": "Com ambas as soluções", "Quantidade": count_both},
                {"Situação": "Sem nenhuma solução", "Quantidade": count_none},
            ],
            width="stretch",
        )
