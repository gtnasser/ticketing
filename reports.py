import streamlit as st

from database import get_connection

def run() -> None:
    st.subheader("📊 Relatório de Ocorrências")

    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM occurrences").fetchone()["n"]
        by_type = conn.execute(
            "SELECT type, COUNT(*) AS n FROM occurrences GROUP BY type ORDER BY n DESC"
        ).fetchall()
        by_user = conn.execute(
            "SELECT username, COUNT(*) AS n FROM occurrences GROUP BY username ORDER BY n DESC"
        ).fetchall()

    st.metric("Total de ocorrências", total)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Por tipo**")
        for row in by_type:
            st.write(f"- {row['type']}: {row['n']}")
    with col2:
        st.write("**Por usuário**")
        for row in by_user:
            st.write(f"- {row['username']}: {row['n']}")