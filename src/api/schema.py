from loggerhelper import LoggerHelper, LogLevel

from fastapi import FastAPI
import os
import json

log = LoggerHelper(__name__)


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        log.info(f"Folder '{folder_path}' created")


def save_schema(app: FastAPI):
    try:
        filename = './client/openapi_schema.json'
        log.log(f"OpenApi schema is saved to file {filename}")

        with open(filename, 'w') as f:
            json.dump(app.openapi(), f, indent=2)
    except Exception as e:
        log.log(f"Error while saving OpenApi schema to file: {e}", log_level=LogLevel.ERROR)
