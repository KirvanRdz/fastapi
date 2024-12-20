from fastapi import FastAPI
from database.database import engine, Base
from routers.movie import routerMovie
from routers.user import routerUser

app= FastAPI(
    title='FastAPI2',
    description='API rest para operaciones CRUD',
    version='0.0.1'
)

app.include_router(routerMovie)
app.include_router(routerUser)
Base.metadata.create_all(bind=engine)





