from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.menu_management.models.menu import Item, Category
from app.services.menu_management.schema import CategoryResponse, ItemResponse, ItemCreate, CategoryCreate


class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category_data: CategoryCreate):
        category = Category(**category_data.model_dump())
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
        item = Item(**item_data.model_dump())
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