
from sqlmodel import create_engine, SQLModel, Field, Session, select
from datetime import datetime, timezone


#
# This is an example to use sqlmodel with traditional SQL queries
#

class Example(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    info: str
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExampleTableModel():

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def create(self):
        SQLModel.metadata.create_all(self.engine)

    def insert(self, parameters: dict):
        new_record = Example(**parameters)
        with Session(self.engine) as session:
            session.add(new_record)
            session.commit()
            session.refresh(new_record)  # Get the auto-generated ID
        return new_record

    def select(self, timestamp: datetime):
        with Session(self.engine) as session:
            statement = select(Example).where(Example.created_on >= timestamp).order_by(Example.created_on)
            latest_records = session.exec(statement).all()

        return latest_records
