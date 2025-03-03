from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.menu_management.models.menu import Item, Category, Menu, MenuItem
from app.services.menu_management.schema import CategoryResponse, ItemResponse, ItemCreate, CategoryCreate, MenuCreate, \
    MenuUpdate, MenuItemCreate, MenuItemUpdate

class MenuService:
    @staticmethod
    def create_menu(db: Session, menu: MenuCreate):
        new_menu = Menu(**menu.dict())
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        return new_menu

    @staticmethod
    def get_menu(db: Session, menu_id: int):
        return db.query(Menu).filter(Menu.id == menu_id).first()

    @staticmethod
    def update_menu(db: Session, menu_id: int, menu: MenuUpdate):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status_code=404, detail="Menu not found")
        for key, value in menu.dict(exclude_unset=True).items():
            setattr(db_menu, key, value)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    @staticmethod
    def delete_menu(db: Session, menu_id: int):
        db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not db_menu:
            raise HTTPException(status_code=404, detail="Menu not found")
        db.delete(db_menu)
        db.commit()
        return {"message": "Menu deleted"}

    @staticmethod
    def create_menu_item(db: Session, menu_item: MenuItemCreate):
        new_menu_item = MenuItem(**menu_item.dict())
        db.add(new_menu_item)
        db.commit()
        db.refresh(new_menu_item)
        return new_menu_item

    @staticmethod
    def get_menu_item(db: Session, menu_item_id: int):
        return db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()

    @staticmethod
    def update_menu_item(db: Session, menu_item_id: int, menu_item: MenuItemUpdate):
        db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not db_menu_item:
            raise HTTPException(status_code=404, detail="MenuItem not found")
        for key, value in menu_item.dict(exclude_unset=True).items():
            setattr(db_menu_item, key, value)
        db.commit()
        db.refresh(db_menu_item)
        return db_menu_item

    @staticmethod
    def delete_menu_item(db: Session, menu_item_id: int):
        db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not db_menu_item:
            raise HTTPException(status_code=404, detail="MenuItem not found")
        db.delete(db_menu_item)
        db.commit()
        return {"message": "MenuItem deleted"}


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

