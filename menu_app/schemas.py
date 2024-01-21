from pydantic import BaseModel, validator
from uuid import UUID


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
    # submenus_count: int

    @validator('id')
    def validate_id(cls, value: UUID) -> str:
        """Перевод id в строку для вывода"""
        return str(value)

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    """Базовая схема для подменю"""
    title: str
    description: str


class SubmenuCreate(MenuBase):
    """Схема для добавления нового подменю"""
    pass


class SubmenuRead(MenuBase):
    """Схема для просмотра подменю"""
    id: UUID
    menu_id: UUID

    @validator('id')
    def validate_submenu_id(cls, value: UUID) -> str:
        """Перевод submenu_id в строку для вывода"""
        return str(value)

    @validator('menu_id')
    def validate_menu_id(cls, value: UUID) -> str:
        """Перевод menu_id в строку для вывода"""
        return str(value)

    class Config:
        orm_mode = True
