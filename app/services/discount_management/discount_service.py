from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .models.discount import Discount
from app.services.order_management.models.orders import Order
from .schema import DiscountResponse
from sqlalchemy import func


class DiscountService:
    @staticmethod
    def apply_discount(order_id: int, discount_code: str, db: Session):
        discount = db.query(Discount).filter(Discount.code == discount_code,
                                             Discount.validity >= func.now()).first()
        if not discount:
            raise HTTPException(status_code=400, detail="Invalid or expired discount code")

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if discount.discount_type == "flat":
            discount_amount = discount.value
        else:  # percentage
            discount_amount = (discount.value / 100) * order.total_amount

        order.total_amount -= discount_amount
        order.discount_id = discount.id
        db.commit()
        return {"order_id": order.id, "new_total": order.total_amount, "discount_applied": discount_amount}

    @staticmethod
    def validate_discount(code: str, db: Session):
        discount = db.query(Discount).filter(Discount.code == code, Discount.validity >= func.now()).first()
        if not discount:
            raise HTTPException(status_code=400, detail="Invalid or expired discount code")

        return DiscountResponse(
            code=discount.code,
            discount_type=discount.discount_type,
            value=discount.value,
            valid_until=discount.validity
        )
