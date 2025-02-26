from sqlalchemy import Column, Integer, ForeignKey, String, Float, Boolean, DateTime, func, JSON
from sqlalchemy.orm import declarative_base, relationship
from app.db.models.base import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)  # "Lunch Menu", "Dinner Menu"
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    outlet_id = Column(Integer, ForeignKey("outlets.id"), nullable=False)  # Foreign key to Outlet
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to Outlet
    outlet = relationship("Outlet", back_populates="menus")
    menu_items = relationship("MenuItem", back_populates="menu")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    is_available = Column(Boolean, default=True)  # Item availability in a specific menu
    price_override = Column(Float, nullable=True)  # Custom price for this menu
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    menu = relationship("Menu", back_populates="menu_items")
    item = relationship("Item", back_populates="menu_items")


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
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
    menu_items = relationship("MenuItem", back_populates="item")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    parent_category = relationship("Category", remote_side=[id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent_category")
    items = relationship("Item", back_populates="category")
