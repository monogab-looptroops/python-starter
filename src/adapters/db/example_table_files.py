from sqlmodel import create_engine, text
from datetime import datetime

#
# This is an example to use sqlmodel with traditional SQL queries
# where the queries are in one file
# Of course they can be in separate files too, but it is interesting
# to see them together
#


# MIGRATING from PostgresHelper to sqlmodel
#
# client = PostgresHelper(
#     url=host,
#     database=db_name,
#     user=user,
#     pwd=pw,
#     port=port,
# )
#
# result = client.execute_get_query(
#     Queries.get_previous_record_for_device_statistics_data_hour,
#     parameters,
# )

# =>

# engine = create_engine(f'postgresql://{user}:{pw}@{host}:{port}/{db_name}')
#
# with engine.connect() as connection:
#       result = connection.execute(self.queries['select'], parameters)
#       rows = result.fetchall()
#


class ExampleTableFiles:
    def __init__(self, db_url: str):

        self.engine = create_engine(db_url)

        self.queries = ExampleTableFiles.load_sql_queries()

    @staticmethod
    def load_sql_queries():
        with open('src/adapters/db/example_queries.sql', 'r') as file:
            queries = file.read().split('-- SQL')
            return {'create': text(queries[1].strip()), 'insert': text(queries[2].strip()), 'select': text(queries[3].strip())}

    def create(self):
        with self.engine.connect() as connection:
            result = connection.execute(self.queries['create'])
            connection.commit()
        return result

    def insert(self, parameters: dict):
        with self.engine.connect() as connection:
            result = connection.execute(self.queries['insert'], parameters)
            connection.commit()
        return result

    def select(self, timestamp: datetime):
        parameters = {'StartTimestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        with self.engine.connect() as connection:
            result = connection.execute(self.queries['select'], parameters)
            rows = result.fetchall()
        return rows
