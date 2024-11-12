from . import database
from . import export

def include_router(app):
    app.include_router(database.router)
    app.include_router(export.router)