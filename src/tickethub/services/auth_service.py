import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from tickethub.security import bearer_scheme
from tickethub.config import settings

async def verify_token(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    token = creds.credentials
    base = settings.external_api_url
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{base}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

async def get_token(username: str, password: str):

    base = settings.external_api_url
    data = {"username": username,
            "password": password}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base}/auth/login", json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_data = response.json()
    return {
        "token": user_data["accessToken"],
        "username": user_data["username"],
        "email": user_data["email"]
    }   
