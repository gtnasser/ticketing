import hashlib
import os

import streamlit as st
from sqlalchemy.exc import IntegrityError

from db import SessionLocal, get_user
from models import User


ITERATIONS = 100_000
_SESSION_USER_KEY = "user"

def _ensure_session() -> None:
    """Create the session variable if it does not exist."""
    if _SESSION_USER_KEY not in st.session_state:
        st.session_state[_SESSION_USER_KEY] = None

def set_current_user(username: str) -> None:
    """Store the authenticated username in the session."""
    _ensure_session()
    st.session_state[_SESSION_USER_KEY] = username

def get_current_user() -> str | None:
    """Return the authenticated username, or None if not logged in."""
    _ensure_session()
    return st.session_state[_SESSION_USER_KEY]

def is_auth() -> bool:
    """Return True if a user is authenticated."""
    return get_current_user() is not None

def clear_session() -> None:
    """Clear the authenticated user from the session."""
    _ensure_session()
    st.session_state[_SESSION_USER_KEY] = None

def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return salt.hex(), digest.hex()

def create_user(username: str, password: str) -> bool:
    salt_hex, hash_hex = _hash_password(password)
    user = User(username=username, password_hash=f"{salt_hex}${hash_hex}")
    try:
        with SessionLocal() as session: 
            session.add(user)
            session.commit()
        return True
    except IntegrityError:
        return False
    
def validate(username: str, password: str) -> bool:
    user = get_user(username)
    if user is None:
        return False
    salt_hex, hash_hex = user.password_hash.split("$")
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return digest.hex() == hash_hex
