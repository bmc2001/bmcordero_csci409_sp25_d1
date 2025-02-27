import os
import jwt
import json
import requests
from jwt.algorithms import RSAAlgorithm
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidAudienceError
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
AUTH0_ALGORITHMS = os.getenv("AUTH0_ALGORITHM", "RS256")

security = HTTPBearer()


def jwt_verify(token: str):
    try:
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid Token: Key was not found")

        payload = jwt.decode(
            token,
            key=jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(rsa_key)),
            algorithms=[AUTH0_ALGORITHMS],
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidAudienceError:
        raise HTTPException(status_code=401,
                            detail="Claims are incorrect, make sure the audiences and issuer is correct")
    except Exception:
        raise HTTPException(status_code=401, detail="Token Invalid")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return jwt_verify(credentials.credentials)
