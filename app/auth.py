import os
import traceback

from fastapi import HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from starlette_context import context

from app.errors import HTTP401Exception


async def requires_auth(request: Request):

    # noinspection PyBroadException
    # TODO check user tables for this auth
    try:
        pass
    except Exception:
        traceback.print_exc()
        raise HTTP401Exception(
            {
                "status": "error",
                "code": "incorrect_login",
                "message": "Incorrect username or password",
            }
        )

    # TODO: update this with results of auth table above
    request.state.user = "user"
    request.state.other = "other property"

    if not hasattr(context, "state"):
        context.state = request.state
    return


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = jwtoken
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
