from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import List
from pydantic import BaseModel

Base = declarative_base()

# Modelo SQLAlchemy para la base de datos
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    category = Column(String, index=True)
    rating = Column(Float)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Modelo Pydantic para la API
class Product(BaseModel):
    id: int
    title: str
    price: float
    category: str
    rating: float
    image_url: str = None

    class Config:
        orm_mode = True

# Modelo para crear productos
class ProductCreate(BaseModel):
    title: str
    price: float
    category: str
    rating: float
    image_url: str = None