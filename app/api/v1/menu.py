from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import DBSync
from app.services.menu_management.schema import CategoryResponse, ItemResponse, ItemCreate, CategoryCreate, MenuCreate, \
    MenuUpdate, MenuItemCreate, MenuItemUpdate
from app.services.menu_management.menu_service import CategoryService, ItemService, MenuService


router = APIRouter()

def get_session():
    return DBSync().get_new_session()


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


@router.post("/menus/")
def create_menu(menu: MenuCreate, db: Session = Depends(get_session)):
    return MenuService.create_menu(db, menu)

@router.get("/menus/{menu_id}")
def get_menu(menu_id: int, db: Session = Depends(get_session)):
    return MenuService.get_menu(db, menu_id)

@router.put("/menus/{menu_id}")
def update_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_session)):
    return MenuService.update_menu(db, menu_id, menu)

@router.delete("/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_session)):
    return MenuService.delete_menu(db, menu_id)

@router.post("/menu-items/")
def create_menu_item(menu_item: MenuItemCreate, db: Session = Depends(get_session)):
    return MenuService.create_menu_item(db, menu_item)

@router.get("/menu-items/{menu_item_id}")
def get_menu_item(menu_item_id: int, db: Session = Depends(get_session)):
    return MenuService.get_menu_item(db, menu_item_id)

@router.put("/menu-items/{menu_item_id}")
def update_menu_item(menu_item_id: int, menu_item: MenuItemUpdate, db: Session = Depends(get_session)):
    return MenuService.update_menu_item(db, menu_item_id, menu_item)

@router.delete("/menu-items/{menu_item_id}")
def delete_menu_item(menu_item_id: int, db: Session = Depends(get_session)):
    return MenuService.delete_menu_item(db, menu_item_id)