from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.services.inventory.models.inventory import (
    Stock, PurchaseOrder, Supplier, PurchaseOrderItem, SaleTransaction, StockMovement, Expense
)
from app.services.inventory.schema import (
    StockCreate, StockMovementCreate,
    PurchaseOrderCreate, SupplierCreate, PurchaseOrderItemCreate, PurchaseTransactionCreate
)


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_stock(self, stock_data: StockCreate):
        """Create a new stock entry."""
        existing_stock = self.db.query(Stock).filter(Stock.item_id == stock_data.item_id).first()
        if existing_stock:
            raise ValueError(f"Stock entry already exists for item_id {stock_data.item_id}.")

        stock = Stock(**stock_data.dict())
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def get_stock_levels(self, item_id: int):
        """Fetch stock levels for a given item."""
        return self.db.query(Stock).filter(Stock.item_id == item_id).first()

    def update_stock(self, item_id: int, quantity: int, movement_type: str, remarks: str = None):
        """
        Update stock when an item is sold, purchased, or wasted.
        Also records the stock movement.
        """
        stock = self.db.query(Stock).filter(Stock.item_id == item_id).first()
        if not stock:
            raise ValueError(f"Stock for item_id {item_id} not found.")

        if movement_type == "Sale" and stock.quantity < quantity:
            raise ValueError("Not enough stock available.")

        # Adjust stock quantity
        stock.quantity += quantity if movement_type == "Purchase" else -quantity

        # Record stock movement
        movement = StockMovement(
            item_id=item_id,
            quantity=quantity,
            movement_type=movement_type,
            remarks=remarks
        )
        self.db.add(movement)
        self.db.commit()
        return stock

    def record_sale(self, item_id: int, quantity: int, payment_method: str):
        """
        Record a sale transaction and reduce stock.
        """
        stock = self.get_stock_levels(item_id)
        if not stock or stock.quantity < quantity:
            raise ValueError("Insufficient stock for sale.")

        stock.quantity -= quantity
        sale = SaleTransaction(
            item_id=item_id,
            quantity=quantity,
            total_price=stock.item.unit_price * quantity,
            payment_method=payment_method
        )
        self.db.add(sale)
        self.db.commit()
        return sale

    def place_purchase_order(self, supplier_id: int, items: list):
        """
        Place a new purchase order and create order items.
        """
        total_cost = sum([item['quantity'] * item['unit_price'] for item in items])

        order = PurchaseOrder(supplier_id=supplier_id, total_cost=total_cost)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        # Create purchase order items
        for item in items:
            order_item = PurchaseOrderItem(
                purchase_order_id=order.id,
                item_id=item['item_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )
            self.db.add(order_item)

        self.db.commit()
        return order

    def get_low_inventory_items(self):
        """Fetch all items below the minimum threshold."""
        return self.db.query(Stock).filter(Stock.quantity < Stock.min_threshold).all()

    def get_stock_movements(self, item_id: int):
        """Fetch stock movement history for an item."""
        return self.db.query(StockMovement).filter(StockMovement.item_id == item_id).all()

    def get_all_suppliers(self):
        """Fetch all suppliers."""
        return self.db.query(Supplier).all()

    def delete_supplier(self, supplier_id: int):
        """Delete a supplier."""
        supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise ValueError(f"Supplier with id {supplier_id} not found.")
        self.db.delete(supplier)
        self.db.commit()
        return {"message": "Supplier deleted successfully."}

    def update_purchase_order_status(self, order_id: int, status: str):
        """Update the status of a purchase order."""
        order = self.db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
        if not order:
            raise ValueError(f"Purchase order with id {order_id} not found.")
        order.status = status
        self.db.commit()
        return order

    def delete_purchase_order(self, order_id: int):
        """Cancel a purchase order."""
        order = self.db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
        if not order:
            raise ValueError(f"Purchase order with id {order_id} not found.")
        self.db.delete(order)
        self.db.commit()
        return {"message": "Purchase order cancelled successfully."}

    def record_purchase_payment(self, order_id: int, amount_paid: float, payment_method: str):
        """Record a payment transaction for a purchase order."""
        purchase_transaction = PurchaseTransactionCreate(
            purchase_order_id=order_id,
            amount_paid=amount_paid,
            payment_method=payment_method
        )
        self.db.add(purchase_transaction)
        self.db.commit()
        return purchase_transaction

    def get_expenses(self):
        """Fetch all recorded expenses."""
        return self.db.query(Expense).all()

    def record_expense(self, expense_type: str, description: str, amount: float):
        """Record a new expense."""
        expense = Expense(
            expense_type=expense_type,
            description=description,
            amount=amount
        )
        self.db.add(expense)
        self.db.commit()
        return expense