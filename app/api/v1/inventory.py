from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import DBSync
from app.services.inventory.schema import CategoryResponse, ItemResponse, ItemCreate, CategoryCreate
from app.services.inventory.models.menu import Item, Category


router = APIRouter()

def get_session():
    return DBSync().get_new_session()


class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_data: CategoryCreate):
        category = Category(**category_data.dict())
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_categories(self):
        return self.session.query(Category).all()

    def get_category(self, category_id: int):
        category = self.session.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def delete_category(self, category_id: int):
        category = self.get_category(category_id)
        self.session.delete(category)
        self.session.commit()
        return {"message": "Category deleted successfully"}

class ItemService:
    def __init__(self, session: Session):
        self.session = session

    def create_item(self, item_data: ItemCreate):
        item = Item(**item_data.dict())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_items(self):
        return self.session.query(Item).all()

    def get_item(self, item_id: int):
        item = self.session.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def delete_item(self, item_id: int):
        item = self.get_item(item_id)
        self.session.delete(item)
        self.session.commit()
        return {"message": "Item deleted successfully"}

# Routes
@router.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    return CategoryService(session).create_category(category)

@router.get("/categories/", response_model=List[CategoryResponse])
def get_categories(session: Session = Depends(get_session)):
    return CategoryService(session).get_categories()

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, session: Session = Depends(get_session)):
    return CategoryService(session).get_category(category_id)


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_session)):
    return CategoryService(session).delete_category(category_id)


@router.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    return ItemService(session).create_item(item)


@router.get("/items/", response_model=List[ItemResponse])
def get_items(session: Session = Depends(get_session)):
    return ItemService(session).get_items()


@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: Session = Depends(get_session)):
    return ItemService(session).get_item(item_id)


@router.delete("/items/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    return ItemService(session).delete_item(item_id)
