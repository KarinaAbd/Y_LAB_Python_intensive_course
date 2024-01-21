from pydantic import BaseModel


class MenuBase(BaseModel):
    """Базовая схема для меню"""
    title: str


class MenuCreate(MenuBase):
    """Схема для добавления нового меню"""
    pass


class MenuRead(MenuBase):
    """Схема для просмотра меню"""
    id: int

    class Config:
        orm_mode = True
