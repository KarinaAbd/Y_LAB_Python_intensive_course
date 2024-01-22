from sqlalchemy.orm import Session

from .. import schemas
from ..models import Dish


def create_dish(db: Session, submenu_id: str, dish: schemas.DishCreate):
    new_dish = Dish(title=dish.title,
                    description=dish.description,
                    price=dish.price,
                    submenu_id=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


def read_dishes(db: Session, submenu_id: str, skip: int = 0, limit: int = 100):
    return db.query(Dish).filter(
        Dish.submenu_id == submenu_id
    ).offset(skip).limit(limit).all()


def get_dish_by_title(db: Session, dish_title: str):
    return db.query(Dish).filter(Dish.title == dish_title).first()


def get_dish_by_id(db: Session, dish_id: str):
    return db.query(Dish).filter(Dish.id == dish_id).first()


def update_dish(db: Session,
                current_dish: schemas.DishRead,
                updated_dish: schemas.DishCreate):
    current_dish.title = updated_dish.title
    current_dish.description = updated_dish.description
    current_dish.price = updated_dish.price

    db.merge(current_dish)
    db.commit()
    db.refresh(current_dish)
    return current_dish


def delete_dish(db: Session, submenu_id: str, dish_id: str):
    dish = get_dish_by_id(db, dish_id)
    db.delete(dish)
    db.commit()
    return read_dishes(db, submenu_id)
