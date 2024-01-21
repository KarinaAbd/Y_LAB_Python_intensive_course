from fastapi import FastAPI

from .menus.menu_api import menu_router

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menu_router)
