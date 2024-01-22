from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Numeric, String, Text
# https://postgrespro.ru/docs/postgresql/9.5/datatype-uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql import func, select

from .database import Base


class Dish(Base):
    """Модель блюда"""

    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Numeric(scale=2), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates="dishes")


class Submenu(Base):
    """Модель подменю"""

    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish",
                          back_populates="submenu",
                          cascade="all, delete")
    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.submenu_id == id).correlate_except(Dish).as_scalar()
    )


class Menu(Base):
    """Модель меню"""

    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    submenus = relationship('Submenu',
                            back_populates="menu",
                            cascade='all, delete')
    submenus_count = column_property(
        select(func.count(Submenu.id)).where(
            Submenu.menu_id == id).correlate_except(Submenu).as_scalar()
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.submenu_id.in_(select(Submenu.id))
        ).correlate_except(Submenu).as_scalar()
    )
