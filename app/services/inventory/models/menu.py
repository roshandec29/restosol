from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

from app.db.models.base import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, index=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    outlet = relationship("Outlet", back_populates="menus")
    order_items = relationship("OrderItem", back_populates="menu")
