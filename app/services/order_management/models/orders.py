from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, UniqueConstraint, func, JSON, Boolean
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=True)
    customer_name = Column(String(255), nullable=True)
    customer_contact = Column(String(255), nullable=True)
    status = Column(String(50), default="Pending")
    payment_status = Column(String(50), default="Unpaid")
    payment_method = Column(String(50), nullable=True)
    total_amount = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    notes = Column(String(500), nullable=True)
    metadata = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="orders")
    outlet = relationship("Outlet", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    metadata = Column(JSON, nullable=True)  # Store additional attributes
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")
