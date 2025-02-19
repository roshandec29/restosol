from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime, func, JSON
from sqlalchemy.orm import declarative_base, relationship
from app.db.models.base import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    type = Column(String(50), nullable=False)
    is_available = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    unit = Column(String(50), nullable=True)
    discount = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    attributes = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("Category", back_populates="items")
    order_items = relationship("OrderItem", back_populates="item")