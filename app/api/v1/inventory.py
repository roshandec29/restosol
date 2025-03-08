from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.inventory.schema import (
    StockCreate, PurchaseOrderCreate, SupplierCreate, PurchaseOrderItemCreate, StockResponse,
    StockMovementCreate, StockMovementResponse, PurchaseTransactionCreate, PurchaseTransactionResponse,
    SaleTransactionCreate, SaleTransactionResponse, ExpenseCreate, ExpenseResponse, SupplierResponse,
    PurchaseOrderResponse
)
from app.services.inventory.inventory_service import InventoryService
from app.db.session import DBSync

router = APIRouter()


def get_session():
    return DBSync().get_new_session()


@router.post("/stocks/", response_model=StockResponse)
def create_stock(stock: StockCreate, session: Session = Depends(get_session)):
    return InventoryService(session).create_stock(stock)


@router.put("/stocks/{item_id}/movement", response_model=StockResponse)
def update_stock(item_id: int, quantity: int, movement_type: str, remarks: str = None, session: Session = Depends(get_session)):
    return InventoryService(session).update_stock(item_id, quantity, movement_type, remarks)


@router.get("/stocks/low-inventory")
def get_low_inventory(session: Session = Depends(get_session)):
    return InventoryService(session).get_low_inventory_items()

# Stock Movement Routes
@router.post("/stock/movement/", response_model=StockMovementResponse)
def record_stock_movement(movement: StockMovementCreate, session: Session = Depends(get_session)):
    return InventoryService(session).record_stock_movement(movement)

@router.get("/stock/movement/{item_id}", response_model=list[StockMovementResponse])
def get_stock_movements(item_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).get_stock_movements(item_id)

# Supplier Routes
@router.post("/supplier/", response_model=SupplierResponse)
def add_supplier(supplier_data: SupplierCreate, session: Session = Depends(get_session)):
    return InventoryService(session).create_supplier(supplier_data)

@router.get("/suppliers/", response_model=list[SupplierResponse])
def list_suppliers(session: Session = Depends(get_session)):
    return InventoryService(session).get_all_suppliers()

@router.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).delete_supplier(supplier_id)

# Purchase Order Routes
@router.post("/purchase_order/", response_model=PurchaseOrderResponse)
def add_purchase_order(order_data: PurchaseOrderCreate, session: Session = Depends(get_session)):
    return InventoryService(session).create_purchase_order(order_data)

@router.get("/purchase_orders/", response_model=list[PurchaseOrderResponse])
def list_purchase_orders(session: Session = Depends(get_session)):
    return InventoryService(session).get_all_purchase_orders()

@router.get("/purchase_orders/{order_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(order_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).get_purchase_order(order_id)

@router.patch("/purchase_orders/{order_id}")
def update_purchase_order_status(order_id: int, status: str, session: Session = Depends(get_session)):
    return InventoryService(session).update_purchase_order_status(order_id, status)

@router.delete("/purchase_orders/{order_id}")
def delete_purchase_order(order_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).delete_purchase_order(order_id)

# Purchase Transaction Routes
@router.post("/purchase-transactions/", response_model=PurchaseTransactionResponse)
def record_purchase_payment(transaction: PurchaseTransactionCreate, session: Session = Depends(get_session)):
    return InventoryService(session).record_purchase_payment(transaction)

@router.get("/purchase-transactions/{order_id}", response_model=list[PurchaseTransactionResponse])
def get_purchase_transactions(order_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).get_purchase_transactions(order_id)

# Sale Transaction Routes
@router.post("/sales/", response_model=SaleTransactionResponse)
def record_sale(sale: SaleTransactionCreate, session: Session = Depends(get_session)):
    return InventoryService(session).record_sale(sale)

@router.get("/sales/{item_id}", response_model=list[SaleTransactionResponse])
def get_sales_history(item_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).get_sales_history(item_id)

@router.get("/sales/", response_model=list[SaleTransactionResponse])
def list_sales(session: Session = Depends(get_session)):
    return InventoryService(session).get_all_sales()

# Expense Routes
@router.post("/expenses/", response_model=ExpenseResponse)
def record_expense(expense: ExpenseCreate, session: Session = Depends(get_session)):
    return InventoryService(session).record_expense(expense)

@router.get("/expenses/", response_model=list[ExpenseResponse])
def list_expenses(session: Session = Depends(get_session)):
    return InventoryService(session).get_expenses()

@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).get_expense(expense_id)
