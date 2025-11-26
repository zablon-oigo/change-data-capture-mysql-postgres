import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI) -> None:
