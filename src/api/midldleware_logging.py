import time
import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loggerhelper import LoggerHelper

logger = LoggerHelper(__name__)


class MiddlewareLogging(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, skip_paths: list[str]):
        super().__init__(app)
        self.skip_paths = skip_paths

    async def dispatch(self, request: Request, call_next):

        if any(skip_path in request.url.path for skip_path in self.skip_paths):
            return await call_next(request)

        logger.info(f"Incoming request: {request.method} {request.url}")
        start_time = time.time()

        response: Response = await call_next(request)

        duration = time.time() - start_time
        logger.info(
            f"Outgoing response: {request.method} {request.url} "
            f"Status code: {response.status_code} Duration: {duration:.2f}s"
        )

        return response
