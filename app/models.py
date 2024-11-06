from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Database(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str
    host: str
    port: int
    password: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)