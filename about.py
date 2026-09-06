import streamlit as st

def run():

    # Título e descrição
    st.subheader("📄 Ticketing - Registro de Ocorrências", divider='rainbow')
    st.markdown(
        "O **Ticketing** foi desenvolvido para ser um sistema simples de "
        "armazenamento e consulta de ocorrências e soluções adotadas, com o "
        "objetivo de formar uma base de conhecimento compartilhada."
    )

    # Histórico de alterações
    st.write("**📝 Últimas Modificações**")
    try:
        with open("history.log", "r", encoding="utf-8") as f:
            content = f.read()

        # Divide em blocos por versão (separador "---")
        blocks = [b.strip() for b in content.split("\n---\n") if b.strip()] # [-5:] # ultimas 5? 
        for index, block in enumerate(reversed(blocks)):
            # versao e data
            title = f"**{block.split('\n', 1)[0].lstrip('# ')}**"
            with st.expander(title, expanded=(index == 0)):
                # demais linhas
                body = block.split("\n", 1)[1] if "\n" in block else ""
                st.markdown(body)

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
    st.caption("© 2026 gtnasser@gmail.com")


