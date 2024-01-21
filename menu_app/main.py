from fastapi import FastAPI

from .menus.menu_api import menu_router
from .submenus.submenu_api import submenu_router

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
