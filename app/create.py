import datetime
import subprocess
import sys
import time
from os.path import abspath
from os.path import dirname

# this is needed to the app and models modules can be imported when code is executed from within app
sys.path.append(dirname(dirname(abspath(__file__))))

from app import __version__  # noqa
from fastapi import FastAPI  # noqa
from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware  # noqa


def get_git_revision_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()


def create_app():
    version = __version__
    print(f"Initializing the app (version: {version}")

    # Always make sure that the "journal_mode" is set to WAL for "litestream"
    from starlette.middleware import Middleware
    from starlette_context import plugins
    from starlette_context.middleware import ContextMiddleware

    middleware = [
        Middleware(
            ContextMiddleware,
            plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
        )
    ]

    app = FastAPI(middleware=middleware)

    # uncomment to add profiler
    # app.add_middleware(PyInstrumentProfilerMiddleware)

    start_time = time.time()

    def get_uptime():
        conversion = datetime.timedelta(seconds=time.time() - start_time)

        return {"seconds": time.time() - start_time, "HH:MM:SS": str(conversion)}

    # environment.add_section("app uptime", get_uptime)
    # end of healthcheck

    from app.api import deck_builder
    from app.api import search

    app.include_router(deck_builder.router)
    app.include_router(search.router)

    return app
