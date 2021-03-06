from fastapi import Depends

from app.auth import JWTBearer
from app.auth import requires_auth
from app.middlewares.client_variables import get_request_variables


def RequiredAuthDependencies():  # noqa
    dependency_list = [
        Depends(get_request_variables),
        Depends(JWTBearer()),
        Depends(requires_auth),
    ]

    return dependency_list


def NoRequiredAuthDependencies():  # noqa
    dependency_list = [
        Depends(get_request_variables),
    ]

    return dependency_list
