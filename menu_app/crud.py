from sqlalchemy.orm import Session

from . import models, schemas


def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Menu).offset(skip).limit(limit).all()


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_menu_by_id(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()
