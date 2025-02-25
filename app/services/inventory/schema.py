from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StockBase(BaseModel):
    item_id: int
    quantity: int
    min_threshold: Optional[int] = 5

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    status: Optional[str] = "Pending"
    total_cost: float

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    order_date: datetime

    class Config:
        from_attributes = True

class SupplierBase(BaseModel):
    name: str
    contact_info: Optional[dict] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PurchaseOrderItemBase(BaseModel):
    purchase_order_id: int
    item_id: int
    quantity: int
    unit_price: float

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int

    class Config:
        from_attributes = True