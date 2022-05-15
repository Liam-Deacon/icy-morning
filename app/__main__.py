"""Convenience entrypoint for starting REST API using `python -m app`."""
import uvicorn

from .api.main_app import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
