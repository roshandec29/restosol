from sqlalchemy.orm import Session
from app.services.inventory.models.inventory import Stock, PurchaseOrder, Supplier, PurchaseOrderItem
from app.services.inventory.schema import StockCreate, PurchaseOrderCreate, SupplierCreate, PurchaseOrderItemCreate


def create_stock(db: Session, stock_data: StockCreate):
    new_stock = Stock(**stock_data.model_dump())
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


def create_purchase_order(db: Session, order_data: PurchaseOrderCreate):
    new_order = PurchaseOrder(**order_data.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def create_supplier(db: Session, supplier_data: SupplierCreate):
    new_supplier = Supplier(**supplier_data.model_dump())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier


def create_purchase_order_item(db: Session, item_data: PurchaseOrderItemCreate):
    new_item = PurchaseOrderItem(**item_data.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item