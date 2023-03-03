import pytest
from fastapi import status

from server.services.messages import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
    http_exc_400_inactive_user,
    http_exc_400_unverified_user,
    http_exc_403_credentials_exception,
    http_exc_403_forbidden_request,
    http_exc_404_key_expired,
    http_exc_404_not_found,
)


@pytest.mark.asyncio
async def test_http_exc_400_credentials_bad_signup_request():
    result = await http_exc_400_credentials_bad_signup_request()
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert "msg" in result.detail
    assert result.detail["msg"] == "Signup failed! Recheck all your credentials!"


@pytest.mark.asyncio
async def test_http_exc_400_credentials_bad_signin_request():
    result = await http_exc_400_credentials_bad_signin_request()
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert "msg" in result.detail
    assert result.detail["msg"] == "Signin failed! Recheck all your credentials!"


@pytest.mark.asyncio
async def test_http_exc_400_inactive_user():
    result = await http_exc_400_inactive_user()
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert "msg" in result.detail
    assert result.detail["msg"] == "User not active. Please reactive account!"


@pytest.mark.asyncio
async def test_http_exc_400_unverified_user():
    result = await http_exc_400_unverified_user()
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert "msg" in result.detail
    assert result.detail["msg"] == "User not verified. Please verify your phone number!"


@pytest.mark.asyncio
async def test_http_exc_403_credentials_exception():
    result = await http_exc_403_credentials_exception()
    assert result.status_code == status.HTTP_403_FORBIDDEN
    assert "msg" in result.detail
    assert result.detail["msg"] == "Refused access to the requested resource!"
    assert "WWW-Authenticate" in result.headers
    assert result.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_http_exc_403_forbidden_request():
    result = await http_exc_403_forbidden_request()
    assert result.status_code == status.HTTP_403_FORBIDDEN
    assert "msg" in result.detail
    assert result.detail["msg"] == "Refused access to the requested resource!"


@pytest.mark.asyncio
async def test_http_exc_404_not_found():
    result = await http_exc_404_not_found()
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert "msg" in result.detail
    assert result.detail["msg"] == "Requested resource does not exist!"


@pytest.mark.asyncio
async def test_http_exc_404_key_expired():
    result = await http_exc_404_key_expired()
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert "msg" in result.detail
    assert result.detail["msg"] == "Provided key has expired! Please validate before expiration."
