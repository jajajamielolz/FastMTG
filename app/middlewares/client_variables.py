import traceback

from fastapi import Request
from starlette_context import context


def get_request_variables(request: Request):
    try:
        if not hasattr(request.state, "no_purpose"):
            request.state.no_purpose = "update later with global non-user based stuff if required"

            # update the context to include the request state
        if not hasattr(context, "state"):
            context.state = request.state
    except Exception as e:
        traceback.print_exc()
        print("initializing global request variables errors: " + str(e))
        return (
            {
                "status": "error",
                "error": type(e).__name__,
                "message": "REQUEST VARIABLES: Error getting request variables in middleware",
            },
            500,
        )
