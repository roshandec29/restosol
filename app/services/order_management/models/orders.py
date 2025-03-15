from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, JSON, Boolean, Index, func
from sqlalchemy.orm import relationship
from app.db.models.base import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=True)
    customer_name = Column(String(255), nullable=True)
    customer_contact = Column(String(255), nullable=True)
    status = Column(String(50), default="Pending", index=True)
    payment_status = Column(String(50), default="Unpaid", index=True)
    payment_method = Column(String(50), nullable=True)
    total_amount = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    service_charge = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    notes = Column(String(500), nullable=True)
    order_metadata = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    order_type = Column(String(50), default="Dine-In")  # Dine-In, Takeaway, Delivery
    table_number = Column(String(20), nullable=True)  # For Dine-In orders
    order_source = Column(String(50), default="POS")  # POS, Online, Third-Party
    payment_reference = Column(String(255), nullable=True)  # External payment tracking
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    users = relationship("User", back_populates="orders")
    outlet = relationship("Outlet", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_order_status", status),
        Index("idx_order_payment_status", payment_status)
    )


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    modifiers = Column(JSON, nullable=True)  # Customizations like Extra Cheese
    preparation_status = Column(String(50), default="Pending")  # Pending, Preparing, Ready, Served
    special_instructions = Column(String(500), nullable=True)  # Additional requests
    order_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")