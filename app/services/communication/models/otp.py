from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from app.db.models.base import Base


class OTPModel(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
