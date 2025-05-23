from fastapi.responses import JSONResponse
from starlette.requests import Request
from fastapi import HTTPException
from loggerhelper import LoggerHelper, LogLevel

logger = LoggerHelper(__name__, log_level=LogLevel.INFO)

# deafult FastApi exception doesn't generate nice log messages, only the error code
# appears in the terminal. This additional exception handler is responsible for
# sending the error with logger
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Log the HTTPException with detail
    logger.log(
        f"HTTPException raised: {exc.detail}, "
        f"Request URL: {request.url}, "
        f"Status Code: {exc.status_code}",
        LogLevel.ERROR,
    )

    # Re-raise the exception after logging
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )