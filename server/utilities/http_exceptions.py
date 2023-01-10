from fastapi import HTTPException, status


async def http_exc_400_credentials_bad_signup_request() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="signup failed! please recheck all your credentials!",
    )


async def http_exc_400_credentials_bad_signin_request() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="signin failed! please recheck all your credentials!",
    )


async def http_400_exc_bad_username_request(username: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"username {username} is taken! Please choose a different one!",
    )


async def http_400_exc_bad_email_request(email: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"email {email} is already registered! Please choose a different one!",
    )
