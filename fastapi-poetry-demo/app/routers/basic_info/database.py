from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from app.schemas.database import Database

from app.dependencies.exceptions import HTTP_404_NOT_FOUND
from app.models.user import User, extract_user_token
from app.schemas.user import User_Pydantic, UserIn_Pydantic
from app.dependencies.api import  BaseApiOut
router = APIRouter()

from pydantic import BaseModel


class PageOut(BaseModel):
    total: int
    items: List[Database]

@router.get("/api/database/list", response_model=BaseApiOut[PageOut])
async def get_users(_: User = Depends(extract_user_token)):
    return BaseApiOut(data=PageOut(total=2, items= [
        Database(id=1, host='192.168.1.1', username='user01'),
        Database(id=2, host='192.168.1.3', username='root')
    ]))