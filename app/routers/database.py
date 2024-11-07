from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import  Session, select
from typing import List
from ..models import Database, engine

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/api/database", response_model=List[Database])
async def readList(request: Request):
    with Session(engine) as session:
        statement = select(Database)
        return session.exec(statement).all()

@router.post("/api/database", response_model=Database)
def create(database: Database):
    with Session(engine) as session:
        session.add(database)
        session.commit()
        session.refresh(database)
        return database        

@router.put("/api/database/{database_id}", response_model=Database)
def update(database_id: int, database: Database):
    with Session(engine) as session:
        db_database = session.get(Database, database_id)
        if not db_database:
            raise HTTPException(status_code=404, detail="Database not found")

        db_database.user = database.user
        db_database.host = database.host
        db_database.port = database.port
        db_database.password = database.password
        session.add(db_database)
        session.commit()
        session.refresh(db_database)
        return db_database

@router.delete("/api/database/{database_id}", response_model=dict)
def delete_database(database_id: int):
    with Session(engine) as session:
        db_database = session.get(Database, database_id)
        if not db_database:
            raise HTTPException(status_code=404, detail="Database not found")
        session.delete(db_database)
        session.commit()
        return {"message": "Database deleted successfully"}        
    
@router.get("/database/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="database.html", 
        context={
            'menu': 'database',
            'title': 'Database',
        }
    )
