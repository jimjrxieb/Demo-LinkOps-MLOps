from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, Cookie, HTTPException, Response, status
from pydantic import BaseModel

# Move to environment variables in production
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Hard-coded demo accounts; replace with DB lookup in prod
ACCOUNTS = {
    "demo-slim": {"password": "demo", "role": "slim"},
    "demo-full": {"password": "arise!", "role": "full"},
}


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str


router = APIRouter(tags=["auth"])


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access",
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, response: Response):
    acct = ACCOUNTS.get(data.username)
    if not acct or acct["password"] != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Create tokens
    token_data = {"sub": data.username, "role": acct["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Set refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return {"access_token": access_token, "token_type": "bearer", "role": acct["role"]}


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(response: Response, refresh_token: Optional[str] = Cookie(None)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token provided"
        )

    try:
        # Verify refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        # Create new tokens
        token_data = {"sub": payload["sub"], "role": payload["role"]}
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        # Set new refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "role": payload["role"],
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )


@router.post("/logout")
def logout(response: Response):
    """Clear refresh token cookie"""
    response.delete_cookie(
        key="refresh_token", httponly=True, secure=True, samesite="strict"
    )
    return {"message": "Logged out successfully"}
