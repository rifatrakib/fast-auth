from fastapi import HTTPException, status


async def http_exc_400_credentials_bad_signup_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Signup failed! Recheck all your credentials!",
    )
