from sqlalchemy.orm import Session

from .. import schemas
from ..models import Submenu


def create_submenu(db: Session, menu_id: str, submenu: schemas.SubmenuCreate):
    new_submenu = Submenu(title=submenu.title,
                          description=submenu.description,
                          menu_id=menu_id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def read_submenus(db: Session, menu_id: str, skip: int = 0, limit: int = 100):
    return db.query(Submenu).filter(
        Submenu.menu_id == menu_id
    ).offset(skip).limit(limit).all()


def get_submenu_by_title(db: Session, submenu_title: str):
    return db.query(Submenu).filter(Submenu.title == submenu_title).first()


def get_submenu_by_id(db: Session, submenu_id: str):
    return db.query(Submenu).filter(Submenu.id == submenu_id).first()


def update_submenu(db: Session,
                   current_submenu: schemas.SubmenuRead,
                   updated_submenu: schemas.SubmenuCreate):
    current_submenu.title = updated_submenu.title
    current_submenu.description = updated_submenu.description
    db.merge(current_submenu)
    db.commit()
    db.refresh(current_submenu)
    return current_submenu


def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    submenu = get_submenu_by_id(db=db, submenu_id=submenu_id)
    db.delete(submenu)
    db.commit()
    return read_submenus(db, menu_id)
