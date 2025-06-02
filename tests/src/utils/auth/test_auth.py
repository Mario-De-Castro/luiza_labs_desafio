import os
import pytest
from jose import jwt
from fastapi import Depends
from src.utils.auth.auth import verify_token, ALGORITHM
from src.utils.exceptions.exceptions import UnauthorizedException

SECRET_KEY = "test_secret_key"

@pytest.fixture(autouse=True)
def set_secret_key_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", SECRET_KEY)

def generate_token(payload, key=SECRET_KEY):
    return jwt.encode(payload, key, algorithm=ALGORITHM)

def test_verify_token_valid(monkeypatch):
    token = generate_token({"sub": "user123"})
    assert verify_token(token) == "user123"

def test_verify_token_no_sub(monkeypatch):
    token = generate_token({})
    with pytest.raises(UnauthorizedException):
        verify_token(token)

def test_verify_token_invalid_token(monkeypatch):
    invalid_token = "invalid.token.value"
    with pytest.raises(UnauthorizedException):
        verify_token(invalid_token)