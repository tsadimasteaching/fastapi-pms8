from fastapi import FastAPI, Depends, HTTPException
from models import User
from typing import List
from db import init_db
from routes.user import router as userrouter
from routes.job import router as jobrouter
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient
import jwt
from typing import Annotated


app = FastAPI()

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://keycloak:8080/realms/hulk/protocol/openid-connect",
    authorizationUrl="http://keycloak:8080/realms/hulk/protocol/openid-connect/auth",
    refreshUrl="http://keycloak:8080/realms/hulk/protocol/openid-connect/token",
)


async def valid_access_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    url = "http://keycloak:8080/realms/hulk/protocol/openid-connect/certs"
    optional_custom_headers = {"User-agent": "custom-user-agent"}
    jwks_client = PyJWKClient(url, headers=optional_custom_headers)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "Ce endpoint est privé"}

app.include_router(userrouter, prefix='/user', tags=["User"])
app.include_router(jobrouter, prefix='/job', tags=["Job"])
