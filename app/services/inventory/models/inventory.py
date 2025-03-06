from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime, func, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.models.base import Base

class StockItem(Base):
    """ Represents an item that can be stocked and sold. """
    __tablename__ = 'stock_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    unit_price = Column(Float, nullable=False)  # Selling price per unit
    cost_price = Column(Float, nullable=False)  # Cost price per unit (for expense tracking)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    stock = relationship("Stock", back_populates="item", uselist=False)
    purchase_order_items = relationship("PurchaseOrderItem", back_populates="stock_item")


class Stock(Base):
    """ Represents stock levels of each item. """
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('stock_items.id'), nullable=False, unique=True)
    quantity = Column(Integer, default=0, nullable=False)
    min_threshold = Column(Integer, default=5)  # Minimum required before restocking alert
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    item = relationship("StockItem", back_populates="stock")


class Supplier(Base):
    """ Represents a supplier from whom stock is purchased. """
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(JSON, nullable=True)  # e.g., {"phone": "123456789", "email": "supplier@mail.com"}
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")


class PurchaseOrder(Base):
    """ Represents an order placed to a supplier for stock purchase. """
    __tablename__ = 'purchase_orders'

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    order_date = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Enum("Pending", "Completed", "Cancelled", name="purchase_status"), default="Pending")
    total_cost = Column(Float, nullable=False)

    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order")
    transactions = relationship("PurchaseTransaction", back_populates="purchase_order")


class PurchaseOrderItem(Base):
    """ Represents items within a purchase order. """
    __tablename__ = 'purchase_order_items'

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey('purchase_orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('stock_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Price at which this batch was bought

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    stock_item = relationship("StockItem", back_populates="purchase_order_items")


class PurchaseTransaction(Base):
    """ Represents payments made for purchase orders. """
    __tablename__ = 'purchase_transactions'

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey('purchase_orders.id'), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(DateTime, server_default=func.now(), nullable=False)
    payment_method = Column(Enum("Cash", "Card", "UPI", "Bank Transfer", name="payment_method"), nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="transactions")


class StockMovement(Base):
    """ Tracks stock movements (inflow from purchases, outflow from sales/wastage). """
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('stock_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum("Purchase", "Sale", "Wastage", name="stock_movement_type"), nullable=False)
    movement_date = Column(DateTime, server_default=func.now(), nullable=False)
    remarks = Column(String(255), nullable=True)  # Notes about the movement

    stock_item = relationship("StockItem", backref="movements")


class Expense(Base):
    """ Tracks all expenses related to running the shop (not just stock). """
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    expense_type = Column(Enum("Stock Purchase", "Rent", "Utilities", "Salaries", "Miscellaneous", name="expense_type"), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(DateTime, server_default=func.now(), nullable=False)
