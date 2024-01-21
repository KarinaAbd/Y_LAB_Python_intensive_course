from sqlalchemy.orm import Session

from . import schemas
from .models import Menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    new_menu = Menu(title=menu.title)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def read_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Menu).offset(skip).limit(limit).all()


def get_menu_by_title(db: Session, menu_title: str):
    return db.query(Menu).filter(Menu.title == menu_title).first()


def get_menu_by_id(db: Session, menu_id: int):
    return db.query(Menu).filter(Menu.id == menu_id).first()


def update_menu(db: Session,
                current_menu: schemas.MenuRead,
                updated_menu: schemas.MenuCreate):
    current_menu.title = updated_menu.title
    db.merge(current_menu)
    db.commit()
    db.refresh(current_menu)
    return current_menu


def delete_menu(db: Session, menu_id: int):
    menu = get_menu_by_id(db=db, menu_id=menu_id)
    db.delete(menu)
    db.commit()
    return read_menus(db=db)
