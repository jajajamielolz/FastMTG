from fastapi import Request

from app.errors import HTTP401Exception


def get_token_auth_header(request: Request):
    """Obtains the access token from the Authorization Header"""
    token = request.headers.get("Authorization", None)
    if not token:
        raise HTTP401Exception(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            }
        )

    parts = token.split()

    if parts[0].lower() != "bearer":
        raise HTTP401Exception(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            }
        )
    elif len(parts) == 1:
        raise HTTP401Exception(
            {"code": "invalid_header", "description": "Token not found"}
        )
    elif len(parts) > 2:
        raise HTTP401Exception(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            }
        )

    token = parts[1]
    return token
