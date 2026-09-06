import streamlit as st

from auth import clear_session, set_current_user, validate

# ---------- autenticacao provisoria ----------
def secret_validate(username: str, password: str) -> bool:
    """validate user/password by /.streamlit/secrets.toml"""
    _username = st.secrets['login']['user']
    _password = st.secrets['login']['password']
    if username == _username and password == _password:
        return True
    else:
        return False



def do_login() -> bool:
    """Render the login screen. Returns True when authenticated."""
    st.subheader("🔐 Registro de Ocorrências")
    st.write(":red[Acesse com seu usuário e senha]")

    with st.form("login"):
        username = st.text_input('Usuário', "user1", placeholder='Digite o seu usuário')
        password = st.text_input('Senha',"password1", type="password", placeholder='Digite a sua senha')
        submit = st.form_submit_button("Entrar")

    if submit:
        if validate(username, password):
            set_current_user(username)
            st.rerun()
        st.error("Usuário ou senha inválidos.")

    return False

def do_logout() -> None:
    """Clear the session and return to the login screen."""
    clear_session()
    st.rerun()

