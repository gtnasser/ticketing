import streamlit as st
from datetime import datetime

def run():

    # Título e descrição
    st.subheader("📄 Ticketing - Registro de Ocorrências", divider='rainbow')
    st.markdown("O **Ticketing** foi desenvolvido para ser um sistema simples de armazenamento e consultar de ocorrências e soluções adotadas, com o objetivo de formar uma base de conhecimento compartilhada.")


    # Histórico de alterações
    st.write("**📝 Últimas Modificações**")
    try:
        with open("history.log", "r", encoding="utf-8") as f:
            logs = f.readlines()
        # Mostra apenas as últimas 10 linhas
        for line in logs[-10:]:
            st.text(line.strip())
    except FileNotFoundError:
        st.warning("Arquivo de histórico não encontrado.")

    # Créditos
    st.write("**👨‍💻 Equipe de Desenvolvimento**")
    st.markdown("""
    - Giba - Back End  
    - Giba - Front End  
    - Giba - Data Analyst  
    - Giba - Coffee & snacks sponsor  
    """)

    # Rodapé
    st.divider()
    st.caption(f"&copy;2026 gtnasser@gmail.com")

