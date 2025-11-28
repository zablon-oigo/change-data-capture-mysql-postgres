import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI) -> None:

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        process_time = time.time() - start_time

        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"

        log_message = (
            f"{client_host}:{client_port} - {request.method} {request.url.path} "
            f"→ {response.status_code} (completed in {process_time:.3f}s)"
        )
        print(log_message)  
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],     
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )