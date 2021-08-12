import sys
from os.path import abspath
from os.path import dirname

import uvicorn

# this is needed to the app and models modules can be imported when code is executed from within app
sys.path.append(dirname(dirname(abspath(__file__))))

from app.create import create_app  # noqa

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
