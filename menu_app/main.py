from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/menus", response_model=list[schemas.MenuRead])
def get_all_menus(skip: int = 0,
                  limit: int = 100,
                  db: Session = Depends(get_db)):
    return crud.read_menus(db, skip=skip, limit=limit)


@app.post("/menus", response_model=schemas.MenuRead)
def post_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_title(db=db, menu_title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=400,
            detail="A menu with that title already exists"
        )
    return crud.create_menu(db=db, menu=menu)


@app.get("/menus/{menu_id}", response_model=schemas.MenuRead)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu not found"
        )
    return db_menu


@app.patch("/menus/{menu_id}", response_model=schemas.MenuRead)
def patch_menu(menu_id: int,
               updated_menu: schemas.MenuCreate,
               db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu not found",
        )
    return crud.update_menu(db=db,
                            current_menu=db_menu,
                            updated_menu=updated_menu)


@app.delete("/menus/{menu_id}", response_model=list[schemas.MenuRead])
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu not found",
        )
    return crud.delete_menu(db=db, menu_id=menu_id)
