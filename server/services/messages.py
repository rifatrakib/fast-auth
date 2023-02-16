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
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Refused access to the requested resource!"},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def http_exc_403_forbidden_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": "Refused access to the requested resource!"},
    )
