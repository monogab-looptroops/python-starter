from pydantic import BaseModel, SecretStr
from config.custom_settings import CustomSettings

class AppConfig(BaseModel):
    environment: str = 'dev'
    site: str = "local"

    version: str = "0.0"
    log_level: str = "INFO"
    port: int = 8300


class MqttConfig(BaseModel):
    host: str = "localhost"
    port: int = 1883
    user: str = ""
    pw: SecretStr


class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"
    user: str = ""
    pw: SecretStr

    def get_url(self) -> str:
        return f"postgresql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.database}"


class ServiceConfig(CustomSettings):
    name : str = ""
    
    app: AppConfig | None = None
    mqtt: MqttConfig | None = None
    postgres: PostgresConfig | None = None
