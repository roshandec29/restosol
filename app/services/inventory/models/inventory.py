from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime, func, JSON
from sqlalchemy.orm import declarative_base, relationship
from app.db.models.base import Base

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    min_threshold = Column(Integer, default=5)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    item = relationship("Item", back_populates="stock")


class PurchaseOrder(Base):
    __tablename__ = 'purchase_orders'

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    order_date = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(50), default="Pending")
    total_cost = Column(Float, nullable=False)

    supplier = relationship("Supplier", back_populates="purchase_orders")


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class PurchaseOrderItem(Base):
    __tablename__ = 'purchase_order_items'

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey('purchase_orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    item = relationship("Item")
