import os
import sys
from os.path import dirname

import dotenv


def load_environment(env: str = None, root: str = None):
    """
    :param env: The environment. For example, "production", "staging" and "development".
    :param root: The folder to load the .env files. Defaults to current working directory,.
    """
    if not env and "pytest" in sys.modules:
        env = "testing"
    elif not env:
        env = os.environ.get("ENVIRONMENT", "development")

    os.environ["ENVIRONMENT"] = env

    root = root or dirname(dirname(dirname(__file__)))

    for file in [".env", f".env.{env}", f".env.{env}.local"]:
        path = os.path.join(root, file)
        if not os.path.isfile(path):
            continue

        # Set verbose=True to ensure the dotenv file is being loaded correctly
        dotenv.load_dotenv(path, override=True, verbose=True)

    return env
