from fastapi import FastAPI

from .database import Base, engine
from .dishes.dish_api import dish_router
from .menus.menu_api import menu_router
from .submenus.submenu_api import submenu_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
