from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.inventory.schema import StockCreate, PurchaseOrderCreate, SupplierCreate, PurchaseOrderItemCreate
from app.services.inventory.inventory_service import create_stock, create_purchase_order, create_supplier, create_purchase_order_item
from app.db.session import DBSync

router = APIRouter()


def get_session():
    return DBSync().get_new_session()


@router.post("/stock/")
def add_stock(stock_data: StockCreate, db: Session = Depends(get_session)):
    return create_stock(db, stock_data)


@router.post("/purchase_order/")
def add_purchase_order(order_data: PurchaseOrderCreate, db: Session = Depends(get_session)):
    return create_purchase_order(db, order_data)


@router.post("/supplier/")
def add_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_session)):
    return create_supplier(db, supplier_data)


@router.post("/purchase_order_item/")
def add_purchase_order_item(item_data: PurchaseOrderItemCreate, db: Session = Depends(get_session)):
    return create_purchase_order_item(db, item_data)