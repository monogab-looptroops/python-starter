from config.config import ServiceConfig, AppConfig

import os

# We are testing mainly if the priorities are correct and
# we can overwrite the lower level values with higher level values

# priority0 - default values (defined in the class)
# priority1 - toml files
# priority2 - .env files
# priority3 - environment variables
# priority4 - explicit assigment in the code


class TestConfig():

    def test_priority0_default_values(self):

        ServiceConfig.set_toml_files([])
        ServiceConfig.set_env_files([])

        config = ServiceConfig(app=AppConfig())
        assert config.app.log_level == "INFO"
        assert config.mqtt is None
        assert config.postgres is None

    def test_priority1_toml(self):
        ServiceConfig.set_toml_files(['src/config/testdata/settings.toml'])
        config = ServiceConfig()

        assert config.postgres.host == "localhost"
        assert config.postgres.database == "example-db"

        ServiceConfig.set_toml_files(['src/config/testdata/settings.toml', 'src/config/testdata/another.toml'])
        config = ServiceConfig()

        assert config.postgres.port == 30042
        assert config.postgres.user == "myuser"
        assert config.postgres.pw.get_secret_value() == "mypassword"

    def test_priority2_env(self):
        ServiceConfig.set_toml_files(['src/config/testdata/settings.toml'])
        ServiceConfig.set_env_files(['src/config/testdata/.env.test'])

        config = ServiceConfig()
        assert config.postgres.user == "user from config_test.env"

    def test_priority3_envvar(self):
        ServiceConfig.set_toml_files(['src/config/settings.toml'])
        ServiceConfig.set_env_files(['src/config/.env.test'])
        os.environ['example__app_version'] = "defined here"
        config = ServiceConfig()
        assert config.app.version == "defined here"

        # config = ServiceConfig.get_instance()
        # assert config.app.version == "defined here"
        # assert config.postgres.user == "user defined here"

    def test_priority4_direct(self):
        ServiceConfig.set_toml_files(['src/config/settings.toml'])
        ServiceConfig.set_env_files(['src/config/.env.test'])
        os.environ['example__app_version'] = "smt2"

        config = ServiceConfig(app=AppConfig(version="explicit"))
        assert config.app.version == "explicit"
