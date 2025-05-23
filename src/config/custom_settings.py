
import os
from typing import Tuple, Type, TypeVar, Any
from loggerhelper import LoggerHelper

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource
)
log = LoggerHelper(__name__)



# Custom config adds few functionalities to the base settings
# 1. Priority of the sources
# 2. Parameter to the source files
# 3. Logging the loaded settings
# 4. Checking if the file exists

# Most of the cases we don't have to change this file

T = TypeVar("T", bound="CustomSettings")

class CustomSettings(BaseSettings):
    _instance : T = None # lazy initialization

    model_config = SettingsConfigDict(
        env_prefix='example__',
        env_nested_delimiter='_',
        env_file=[],
        env_file_encoding='utf-8',
        toml_file=[]
    )

    @classmethod
    def set_toml_files(cls, toml_files: list[str]):
        cls.model_config['toml_file'] = toml_files
        CustomSettings.log_if_exists(toml_files)

    @classmethod
    def set_env_files(cls, env_files: list[str]  ):
        cls.model_config['env_file'] = env_files
        CustomSettings.log_if_exists(env_files)

    @classmethod
    def get_instance(cls: Type[T]) -> T:
        return cls._instance.default

    def __init__(self,**values: Any):
        super().__init__(**values)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:

        env_settings.config['env_file'] = cls.model_config['env_file']

        # first < highest priority,  last < lowest
        priority = (
            init_settings,  # explicit assigment in the code
            env_settings,    # enviroment variables
            dotenv_settings,  # .env kind of files
            TomlConfigSettingsSource(settings_cls, toml_file=cls.model_config['toml_file'])  # toml files
        )
        return priority

    def log(self):
        # just a few fields to show that the config is loaded
        log.info(f"Site {self.app.site}")
        log.info(f"Environment: {self.app.environment}")
        log.info(f"Version: {self.app.version}")
        log.info(f"DB -> {self.postgres.host}:{self.postgres.port}/{self.postgres.database} user={self.postgres.user} {self.postgres.pw}  ")
        log.info(f"MQTT Broker -> {self.mqtt.host}:{self.mqtt.port} user={self.mqtt.user} {self.mqtt.pw}")


    @staticmethod
    def with_path(filename: str) -> str:
        return f"{os.getcwd()}/src/config/{filename}"

    @staticmethod
    def log_if_exists(filenames: list[str]):
        for filename in filenames:
            path = CustomSettings.with_path(filename)
            if os.path.exists(path):
                log.log(f"Loading settings from file '{path}'")
            else:
                log.log(f"Error: settings file '{path}' doesn't exist")