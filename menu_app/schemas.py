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

    @validator('id')
    def validate_id(cls, value: UUID) -> str:
        """Перевод id в строку для вывода"""
        return str(value)

    class Config:
        orm_mode = True
