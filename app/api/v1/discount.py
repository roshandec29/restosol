from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.discount_management.discount_service import DiscountService
from app.services.discount_management.schema import DiscountApplyRequest, DiscountResponse
from app.db.session import DBSync
router = APIRouter()


def get_db():
    return DBSync().get_new_session()


@router.post("/discounts/apply/")
def apply_discount(request: DiscountApplyRequest, db: Session = Depends(get_db)):
    return DiscountService.apply_discount(request.order_id, request.discount_code, db)


@router.get("/discounts/validate/{code}", response_model=DiscountResponse)
def validate_discount(code: str, db: Session = Depends(get_db)):
    return DiscountService.validate_discount(code, db)
