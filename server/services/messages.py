from fastapi import HTTPException, status


async def http_exc_400_credentials_bad_signup_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Signup failed! Recheck all your credentials!"},
    )


async def http_exc_400_credentials_bad_signin_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Signin failed! Recheck all your credentials!"},
    )


async def http_exc_400_inactive_user() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "User not active. Please reactive account!"},
    )


async def http_exc_400_unverified_user() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "User not verified. Please verify your phone number!"},
    )


async def http_exc_403_credentials_exception() -> Exception:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"msg": "Refused access to the requested resource!"},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def http_exc_403_forbidden_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"msg": "Refused access to the requested resource!"},
    )


async def http_exc_404_not_found() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Requested resource does not exist!"},
    )


async def http_exc_404_key_expired() -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Provided key has expired! Please validate before expiration."},
    )


async def http_exc_409_conflict(message: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"msg": message},
    )


async def http_exc_412_password_mismatch() -> Exception:
    return HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail={"msg": "Passwords does not match!"},
    )


async def http_exc_422_field_required(field_name: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"msg": f"{field_name} is required."},
    )
