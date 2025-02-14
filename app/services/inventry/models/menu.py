from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, index=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    outlet = relationship("Outlet", back_populates="menus")
    order_items = relationship("OrderItem", back_populates="menu")