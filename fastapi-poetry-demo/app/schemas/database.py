from pydantic import BaseModel


class Database(BaseModel):
    id: int
    host: str
    username: str
