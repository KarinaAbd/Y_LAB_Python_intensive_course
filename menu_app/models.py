from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String, Text
# https://postgrespro.ru/docs/postgresql/9.5/datatype-uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Menu(Base):
    """Модель меню"""

    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    submenus = relationship('Submenu',
                            back_populates="menu",
                            cascade='all, delete')


class Submenu(Base):
    """Модель подменю."""

    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    menu = relationship("Menu", back_populates="submenus")
