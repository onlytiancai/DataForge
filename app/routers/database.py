from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import  Session, select
from ..models import Database, engine

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/api/database")
async def index(request: Request):
    with Session(engine) as session:
        statement = select(Database)
        return session.exec(statement).all()

@router.post("/api/database")
def create_hero(database: Database):
    with Session(engine) as session:
        session.add(database)
        session.commit()
        session.refresh(database)
        return database        

@router.get("/database/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="database.html", 
        context={
            'menu': 'database',
            'title': 'Database',
        }
    )
