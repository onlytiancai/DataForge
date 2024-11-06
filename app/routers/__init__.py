from . import database

def include_router(app):
    app.include_router(database.router, tags=["database service"])