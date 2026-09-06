import streamlit as st
from database import get_connection


def run() -> None:
    st.subheader("🏠 Welcome to Ticketing - Registro de Ocorrências", divider='rainbow')

#    with get_connection() as conn:
#        total = conn.execute("SELECT COUNT(*) AS n FROM occurrences").fetchone()["n"]
    total = 23
    st.metric("Ocorrências registradas", total, border=True, width=300)
    st.metric("Ocorrências registradas", total, border=True, width=300)


    # Container flex com CSS
    st.markdown(
        """
        <style>
        .flex-container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap; /* permite quebrar linha em telas menores */
        }
        .flex-item {
            flex: 1;
            min-width: 200px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Cria o container
    st.markdown('<div class="flex-container">', unsafe_allow_html=True)

    # Cada métrica é um "item"
    st.markdown('<div class="flex-item">', unsafe_allow_html=True)
    st.metric("Ocorrências registradas", total, border=True, width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="flex-item">', unsafe_allow_html=True)
    st.metric("Ocorrências abertas", 5, border=True, width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="flex-item">', unsafe_allow_html=True)
    st.metric("Ocorrências fechadas", 18, border=True, width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    # Fecha o container
    st.markdown('</div>', unsafe_allow_html=True)

