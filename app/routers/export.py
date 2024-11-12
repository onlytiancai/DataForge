from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import  Session, select
from typing import List
from ..models import Export, engine

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/api/export", response_model=List[Export])
async def readList(request: Request):
    with Session(engine) as session:
        statement = select(Export)
        return session.exec(statement).all()

@router.post("/api/export", response_model=Export)
def create(export: Export):
    with Session(engine) as session:
        session.add(export)
        session.commit()
        session.refresh(export)
        return export

@router.put("/api/export/{export_id}", response_model=Export)
def update(export_id: int, export: Export):
    with Session(engine) as session:
        db_export = session.get(Export, export_id)
        if not db_export:
            raise HTTPException(status_code=404, detail="Export not found")

        db_export.database_id = export.database_id
        db_export.output_dir = export.output_dir
        db_export.tables = export.tables

        session.add(db_export)
        session.commit()
        session.refresh(db_export)
        return db_export

@router.delete("/api/export/{export_id}", response_model=dict)
def delete_export(export_id: int):
    with Session(engine) as session:
        db_export = session.get(Export, export_id)
        if not db_export:
            raise HTTPException(status_code=404, detail="Export not found")
        session.delete(db_export)
        session.commit()
        return {"message": "export deleted successfully"}        
    
@router.get("/export/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="export.html", 
        context={
            'menu': 'export',
            'title': 'export',
        }
    )
