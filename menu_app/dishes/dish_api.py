from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..submenus.submenu_crud import get_submenu_by_id
from ..submenus.submenu_api import find_menu
from . import dish_crud


dish_router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
)


@dish_router.get("/", response_model=list[schemas.DishRead])
def get_all_dishes(menu_id: str,
                   submenu_id: str,
                   skip: int = 0,
                   limit: int = 100,
                   db: Session = Depends(get_db)):
    # if find_menu(menu_id, db) and find_submenu(submenu_id, db):
    return dish_crud.read_dishes(db, submenu_id, skip, limit)


@dish_router.post("/", response_model=schemas.DishRead, status_code=201)
def post_dish(dish: schemas.DishCreate,
              menu_id: str,
              submenu_id: str,
              db: Session = Depends(get_db)):
    if find_menu(menu_id, db) and find_submenu(submenu_id, db):
        db_dish = dish_crud.get_dish_by_title(db, dish.title)
        if db_dish:
            raise HTTPException(
                status_code=400,
                detail="A dish with that title already exists"
            )
        # dish.price = f"{dish.price:.2f}"
        return dish_crud.create_dish(db, submenu_id, dish)


@dish_router.get("/{dish_id}", response_model=schemas.DishRead)
def get_dish(menu_id: str,
             submenu_id: str,
             dish_id: str,
             db: Session = Depends(get_db)):
    if find_menu(menu_id, db) and find_submenu(submenu_id, db):
        db_dish = dish_crud.get_dish_by_id(db, dish_id)
        if db_dish is None:
            raise HTTPException(
                status_code=404,
                detail="dish not found"
            )
        return db_dish


@dish_router.patch("/{dish_id}", response_model=schemas.DishRead)
def patch_dish(menu_id: str,
               submenu_id: str,
               dish_id: str,
               updated_dish: schemas.DishCreate,
               db: Session = Depends(get_db)):
    if find_menu(menu_id, db) and find_submenu(submenu_id, db):
        current_dish = dish_crud.get_dish_by_id(db, dish_id)
        updated_title = dish_crud.get_dish_by_title(db, updated_dish.title)
        if current_dish is None:
            raise HTTPException(
                status_code=404,
                detail="dish not found"
            )
        elif updated_title:
            raise HTTPException(
                status_code=400,
                detail="A dish with that title already exists"
            )

        return dish_crud.update_dish(db, current_dish, updated_dish)


@dish_router.delete("/{dish_id}", response_model=list[schemas.DishRead])
def delete_dish(menu_id: str,
                submenu_id: str,
                dish_id: str,
                db: Session = Depends(get_db)):
    if find_menu(menu_id, db) and find_submenu(submenu_id, db):
        db_dish = dish_crud.get_dish_by_id(db, dish_id)
        if db_dish is None:
            raise HTTPException(
                status_code=404,
                detail="dish not found"
            )
        return dish_crud.delete_dish(db, submenu_id, dish_id)


def find_submenu(submenu_id: str, db: Session = Depends(get_db)):
    current_submenu = get_submenu_by_id(db, submenu_id)
    if current_submenu is None:
        raise HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    return current_submenu
