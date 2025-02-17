from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    customer_name = Column(String(255), nullable=False)
    customer_contact = Column(String(255), nullable=False)
    status = Column(String(255), default="Pending")
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    outlet = relationship("Outlet", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_id = Column(Integer, ForeignKey('menus.id'), nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu", back_populates="order_items")

    __table_args__ = (UniqueConstraint('order_id', 'menu_id', name='unique_order_menu'),)