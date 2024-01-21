from sqlalchemy import Column, Integer, String

from .database import Base


class Menu(Base):
    """Модель меню"""

    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False, unique=True)
