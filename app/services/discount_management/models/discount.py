from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base import Base


class Discount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    discount_type = Column(String, nullable=False)  # flat or percentage
    value = Column(Float, nullable=False)
    validity = Column(DateTime, nullable=False)


