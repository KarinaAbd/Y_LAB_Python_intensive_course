from uuid import uuid4
from sqlalchemy import Column, String, Text
# https://postgrespro.ru/docs/postgresql/9.5/datatype-uuid
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Menu(Base):
    """Модель меню"""

    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
