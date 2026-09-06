import streamlit as st
from datetime import datetime

from database import get_connection
from auth import get_current_user

def run() -> None:
    st.subheader("📝 Cadastrar Ocorrência", divider='rainbow')

    with st.form("form_occurrence"):
        occurrence_date = st.date_input("Data da ocorrência", value=datetime.now().date())
        title = st.text_input("Título *")
        type_ = st.selectbox("Tipo", ["Erro de sistema", "Erro de operação", "Outros"])
        temporary_solution = st.text_area("Solução provisória")
        definitive_solution = st.text_area("Solução definitiva")
        submit = st.form_submit_button("💾 Salvar ocorrência")

    if submit:
        if not title.strip():
            st.error("O título é obrigatório.")
        else:
            registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            todo="""
            with get_connection() as conn:
                conn.execute(
                    " ""
                    INSERT INTO occurrences
                        (occurrence_date, title, type, temporary_solution,
                         definitive_solution, username, registered_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    " "",
                    (
                        occurrence_date.strftime("%Y-%m-%d"),
                        title.strip(),
                        type_,
                        temporary_solution.strip(),
                        definitive_solution.strip(),
                        get_current_user(),
                        registered_at,
                    ),
                )
            st.success("Ocorrência registrada com sucesso!")
            """
        st.success("TODO: add database stuff, basic routing is OK")


