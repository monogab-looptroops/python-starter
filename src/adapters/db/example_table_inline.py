
from sqlmodel import create_engine, text
from datetime import datetime

#
# This is an example to use sqlmodel with traditional SQL queries
#


sql_create = text('''
CREATE TABLE IF NOT EXISTS example (
    id SERIAL PRIMARY KEY,
    info TEXT,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

sql_insert = text('''
INSERT INTO example(info, created_on)
VALUES ( :Info , CURRENT_TIMESTAMP)
''')

sql_select = text('''
SELECT *
FROM example
WHERE created_on >= :StartTimestamp
ORDER BY info
''')


class ExampleTableInline():

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def create(self):
        with self.engine.connect() as connection:
            result = connection.execute(sql_create)
            connection.commit()
        return result

    def insert(self, parameters: dict):

        with self.engine.connect() as connection:
            result = connection.execute(sql_insert, parameters)
            connection.commit()
        return result

    def select(self, timestamp: datetime):

        parameters = {"StartTimestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")}

        with self.engine.connect() as connection:
            result = connection.execute(sql_select, parameters)
            rows = result.fetchall()
        return rows
