from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from . import menu_crud

menu_router = APIRouter(prefix="/api/v1/menus")


@menu_router.get("/", response_model=list[schemas.MenuRead])
def get_all_menus(skip: int = 0,
                  limit: int = 100,
                  db: Session = Depends(get_db)):
    return menu_crud.read_menus(db, skip=skip, limit=limit)


@menu_router.post("/", response_model=schemas.MenuRead, status_code=201)
def post_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = menu_crud.get_menu_by_title(db=db, menu_title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=400,
            detail="A menu with that title already exists"
        )
    return menu_crud.create_menu(db=db, menu=menu)


@menu_router.get("/{menu_id}", response_model=schemas.MenuRead)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = menu_crud.get_menu_by_id(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu not found"
        )
    return db_menu


@menu_router.patch("/{menu_id}", response_model=schemas.MenuRead)
def patch_menu(menu_id: str,
               updated_menu: schemas.MenuCreate,
               db: Session = Depends(get_db)):
    current_menu = menu_crud.get_menu_by_id(db, menu_id=menu_id)
    updated_title = menu_crud.get_menu_by_title(db,
                                                menu_title=updated_menu.title)
    if current_menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu not found",
        )
    elif updated_title:
        raise HTTPException(
            status_code=400,
            detail="A menu with that title already exists"
        )

    return menu_crud.update_menu(db=db,
                                 current_menu=current_menu,
                                 updated_menu=updated_menu)


@menu_router.delete("/{menu_id}", response_model=list[schemas.MenuRead])
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = menu_crud.get_menu_by_id(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu not found",
        )
    return menu_crud.delete_menu(db=db, menu_id=menu_id)
