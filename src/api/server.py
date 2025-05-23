
from fastapi import FastAPI, HTTPException
from uvicorn import Server, Config


from api.router_example import router_example
from api.midldleware_logging import MiddlewareLogging
from api.exception_handler import custom_http_exception_handler
from loggerhelper import LoggerHelper, LogLevel
from gui.example import ui
from contextlib import asynccontextmanager
from api.schema import save_schema, create_folder_if_not_exists
from api.jython import generate_jython_client

from api.terminate_gently import listen_to_terminate_signal

logger = LoggerHelper(__name__, log_level=LogLevel.INFO)


@ asynccontextmanager
async def lifespan(app: FastAPI):
    # at starting server
    create_folder_if_not_exists('./client/jython')

    save_schema(app)

    generate_jython_client()

    listen_to_terminate_signal()

    yield
    # at ending server


# FASTAPI
api = FastAPI(
    title="Microserice API",
    description="API's used for this microservice",
    version="0.1",
    lifespan=lifespan,
)

# exception handler for extra log message in case of HTTPException
api.add_exception_handler(HTTPException, custom_http_exception_handler)

# add middlewares
api.add_middleware(MiddlewareLogging, skip_paths=["/monitor"])

# example how to add api routes
api.include_router(router=router_example)


async def custom_shutdown():
    print("Shutting down NiceGUI...")
    await ui.shutdown()
api.add_event_handler("shutdown", custom_shutdown)


def get_api():
    return api


def get_server():

    config = Config(api, host="0.0.0.0", port=8000)
    return Server(config)
