from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# Stock Schemas
class StockCreate(BaseModel):
    item_id: int
    quantity: int


class StockResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    min_threshold: int
    last_updated: datetime


# Stock Movement Schemas
class StockMovementCreate(BaseModel):
    item_id: int
    quantity: int
    movement_type: str
    remarks: Optional[str] = None


class StockMovementResponse(StockMovementCreate):
    id: int
    movement_date: datetime


# Supplier Schemas
class SupplierCreate(BaseModel):
    name: str
    contact_info: dict


class SupplierResponse(SupplierCreate):
    id: int
    created_at: datetime


# Purchase Order Schemas
class PurchaseOrderItemCreate(BaseModel):
    item_id: int
    quantity: int
    unit_price: float


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    items: List[PurchaseOrderItemCreate]


class PurchaseOrderResponse(BaseModel):
    id: int
    supplier_id: int
    order_date: datetime
    status: str
    total_cost: float
    items: List[PurchaseOrderItemCreate]


# Purchase Transaction Schemas
class PurchaseTransactionCreate(BaseModel):
    purchase_order_id: int
    amount_paid: float
    payment_method: str


class PurchaseTransactionResponse(PurchaseTransactionCreate):
    id: int
    payment_date: datetime


# Sale Transaction Schemas
class SaleTransactionCreate(BaseModel):
    item_id: int
    quantity: int
    payment_method: str


class SaleTransactionResponse(SaleTransactionCreate):
    id: int
    total_price: float
    sale_date: datetime


# Expense Schemas
class ExpenseCreate(BaseModel):
    expense_type: str
    description: str
    amount: float


class ExpenseResponse(ExpenseCreate):
    id: int
    expense_date: datetime
