from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..menus.menu_api import get_menu
from . import submenu_crud

submenu_router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus")


@submenu_router.get("/", response_model=List[schemas.SubmenuRead])
def get_all_submenus(menu_id: str, skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    return submenu_crud.read_submenus(db, menu_id, skip, limit)


@submenu_router.post("/", response_model=schemas.SubmenuRead, status_code=201)
def post_submenu(submenu: schemas.SubmenuCreate,
                 menu_id: str,
                 db: Session = Depends(get_db)):
    if get_menu(menu_id, db):
        db_submenu = submenu_crud.get_submenu_by_title(db, submenu.title)

        if db_submenu:
            raise HTTPException(
                status_code=400,
                detail="A submenu with that title already exists"
            )
        return submenu_crud.create_submenu(db, menu_id, submenu)


@submenu_router.get("/{submenu_id}", response_model=schemas.SubmenuRead)
def get_submenu(submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = submenu_crud.get_submenu_by_id(db, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(
            status_code=404,
            detail="submenu not found"
        )
    return db_submenu


@submenu_router.patch("/{submenu_id}", response_model=schemas.SubmenuRead)
def patch_submenu(submenu_id: str,
                  updated_submenu: schemas.MenuCreate,
                  db: Session = Depends(get_db)):
    current_submenu = submenu_crud.get_submenu_by_id(db, submenu_id)
    updated_title = submenu_crud.get_submenu_by_title(db,
                                                      updated_submenu.title)

    if current_submenu is None:
        raise HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    elif updated_title:
        raise HTTPException(
            status_code=400,
            detail="A submenu with that title already exists"
        )

    return submenu_crud.update_submenu(db, current_submenu, updated_submenu)


@submenu_router.delete("/{submenu_id}",
                       response_model=List[schemas.SubmenuRead])
def delete_submenu(menu_id: str, submenu_id: str,
                   db: Session = Depends(get_db)):
    db_submenu = submenu_crud.get_submenu_by_id(db, submenu_id)

    if db_submenu is None:
        raise HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    return submenu_crud.delete_submenu(db, menu_id, submenu_id)
