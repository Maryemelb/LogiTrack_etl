from fastapi import FastAPI
from src.routes.login import router as login_router
from src.routes.register import router as register_router
from src.routes.prediction import router as predict_router
from sqlalchemy_utils import database_exists, create_database
from src.db.database import engine, Base
app= FastAPI()
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(bind=engine)


app.include_router(login_router)
app.include_router(register_router)
app.include_router(predict_router)