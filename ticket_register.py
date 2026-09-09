import streamlit as st
from datetime import datetime

from db import SessionLocal
from models import Occurrence
from auth import get_current_user


def run() -> None:
    st.subheader("📝 Cadastrar Ocorrência", divider='rainbow')

    with st.form("form_occurrence"):
        occurrence_date = st.date_input("Data da ocorrência", value=datetime.now().date())
        title = st.text_input("Título *")
        occurrence_type = st.selectbox("Tipo", ["Erro de sistema", "Erro de operação", "Outros"])
        temporary_solution = st.text_area("Solução provisória")
        definitive_solution = st.text_area("Solução definitiva")
        submit = st.form_submit_button("💾 Salvar ocorrência")

    if submit:
        if not title.strip():
            st.error("O título é obrigatório.")
        else:
            occurrence = Occurrence(
                occurrence_date=occurrence_date.strftime("%Y-%m-%d"),
                occurrence_type=occurrence_type,
                title=title.strip(),
                temporary_solution=temporary_solution.strip(),
                definitive_solution=definitive_solution.strip(),
                username=get_current_user(),
                registered_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            with SessionLocal() as session:
                session.add(occurrence)
                session.commit()
            st.success("Ocorrência registrada com sucesso!")


