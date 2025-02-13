from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

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

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_contact = Column(String, nullable=False)
    status = Column(String, default="Pending")
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu", back_populates="order_items")

    __table_args__ = (UniqueConstraint('order_id', 'menu_id', name='unique_order_menu'),)
