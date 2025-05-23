from adapters.db.example_table_inline import ExampleTableInline
from adapters.db.example_table_files import ExampleTableFiles
from adapters.db.example_table_model import ExampleTableModel
from datetime import datetime, timedelta


def get_db_url():
    #
    #  Remark: the postgres url with the given user+password points
    #  to the docker-compose.yaml/postgres server
    #  extra step: you should create the database "example-dev-test"
    #
    return f'postgresql://myuser:mypassword@localhost:30042/testdb'


yesterday = datetime.now() - timedelta(days=1)


class TestExampleTableInline:
    @classmethod
    def setup_method(cls):
        cls.table = ExampleTableInline(get_db_url())
        cls.table.create()

    def test_insert(self):
        res = self.table.insert({'Info': 'test example inline'})
        assert res is not None

    def test_select(self):
        res = self.table.select(yesterday)
        assert len(res) > 0


class TestExampleTableFiles:
    @classmethod
    def setup_method(cls):
        cls.table = ExampleTableFiles(get_db_url())
        cls.table.create()

    def test_insert(self):
        res = self.table.insert({'Info': 'test example file'})
        assert res is not None

    def test_select(self):
        res = self.table.select(yesterday)
        assert len(res) > 0


class TestExampleTableModel:
    @classmethod
    def setup_method(cls):
        cls.table = ExampleTableModel(get_db_url())
        cls.table.create()

    def test_insert(self):
        res = self.table.insert({'info': 'test table model'})
        assert res is not None

    def test_select(self):
        res = self.table.select(yesterday)
        assert len(res) > 0
