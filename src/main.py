from loggerhelper import LoggerHelper, LogLevel
from config.config import ServiceConfig

def bootstrap_example():
    ServiceConfig.set_toml_files(['src/settings.toml', 'src/.secrets.toml'])
    config = ServiceConfig()

    logger = LoggerHelper(__name__, log_level=LogLevel.INFO)
    logger.info(r" __________   ___      ___      .___  ___. .______    __       _______ ")
    logger.info(r"|   ____\  \ /  /     /   \     |   \/   | |   _  \  |  |     |   ____|")
    logger.info(r"|  |__   \  V  /     /  ^  \    |  \  /  | |  |_)  | |  |     |  |__   ")
    logger.info(r"|   __|   >   <     /  /_\  \   |  |\/|  | |   ___/  |  |     |   __|  ")
    logger.info(r"|  |____ /  .  \   /  _____  \  |  |  |  | |  |      |  `----.|  |____ ")
    logger.info(r"|_______/__/ \__\ /__/     \__\ |__|  |__| | _|      |_______||_______|")
    logger.info(f"started with version = {config.app.version} ")
    config.log()
    # initializing endpoints
    from api.server import get_server, get_api
    server = get_server()

    # initializing gui
    from gui.server import init_gui
    init_gui(get_api())
    return server


if __name__ == "__main__":
    server = bootstrap_example()
    server.run()
