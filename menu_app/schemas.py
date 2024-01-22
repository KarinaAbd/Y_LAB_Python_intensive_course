from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    """Базовая схема для меню"""
    title: str
    description: str


class MenuCreate(MenuBase):
    """Схема для добавления нового меню"""
    pass


class MenuRead(MenuBase):
    """Схема для просмотра меню"""
    id: UUID
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    """Базовая схема для подменю"""
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    """Схема для добавления нового подменю"""
    pass


class SubmenuRead(SubmenuBase):
    """Схема для просмотра подменю"""
    id: UUID
    menu_id: UUID
    dishes_count: int

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    """Базовая схема для блюда"""
    title: str
    description: str
    price: Decimal = Field(max_digits=5, decimal_places=2)


class DishCreate(DishBase):
    """Схема для добавления нового подменю"""
    pass


class DishRead(DishBase):
    """Схема для просмотра подменю"""
    id: UUID
    submenu_id: UUID

    class Config:
        orm_mode = True
