from typing import List, Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: Optional[str] = "USD"
    category_id: int
    type: str
    is_available: Optional[bool] = True
    stock_quantity: Optional[int] = 0
    unit: Optional[str] = None
    discount: Optional[float] = 0.0
    tax_rate: Optional[float] = 0.0
    attributes: Optional[dict] = None


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True