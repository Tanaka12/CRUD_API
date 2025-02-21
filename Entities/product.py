from sqlalchemy import Column, Integer, String

from .base import Base

class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String)