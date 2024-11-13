from typing import Optional
from sqlalchemy import DateTime, func, text
from sqlalchemy.exc import OperationalError
from sqlmodel import Field, Column, SQLModel, create_engine, Session
import datetime


class Database(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str
    host: str
    port: int
    password: str
    database: str

    def test(self) -> bool:
        database_url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        engine = create_engine(database_url)

        try:
            with Session(engine) as session:
                session.exec(text("SELECT 1"))
            return True
        except OperationalError as e:
            return False            

class Export(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    database_id: int
    output_dir: str
    tables: str
    created_at: datetime.datetime = Field(
        default_factory= lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    updated_at: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)