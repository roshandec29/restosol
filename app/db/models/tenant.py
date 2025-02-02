from sqlalchemy import func, DateTime, Column, String, Integer, Boolean, ForeignKey, Text, Enum, JSON, DECIMAL, Date, text
from sqlalchemy.orm import relationship
from .base import Base
import enum
from sqlalchemy.dialects.mysql import TIMESTAMP

class SubscriptionPlan(str, enum.Enum):
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class PaymentStatus(str, enum.Enum):
    PAID = "paid"
    PENDING = "pending"
    OVERDUE = "overdue"


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    contact_email = Column(String(255), unique=True)
    contact_phone = Column(String(20))
    billing_address = Column(Text)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.BASIC)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    outlets = relationship("Outlet", back_populates="tenant")
    integrations = relationship("TenantIntegration", back_populates="tenant")
    billing = relationship("TenantBilling", back_populates="tenant")
    users = relationship('User', back_populates='tenant')
    user_roles = relationship('UserRole', back_populates='tenant')
    roles = relationship('Role', back_populates='tenant')


class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    phone = Column(String(20))
    operating_hours = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tenant = relationship("Tenant", back_populates="outlets")
    analytics = relationship("OutletAnalytics", back_populates="outlet")
    integrations = relationship("TenantIntegration", back_populates="outlet")
    users = relationship('User', back_populates='outlet')
    user_roles = relationship('UserRole', back_populates='outlet')



class TenantIntegration(Base):
    __tablename__ = "tenant_integrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    outlet_id = Column(Integer, ForeignKey("outlets.id"), nullable=True)
    integration_name = Column(String(255), nullable=False)
    integration_config = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tenant = relationship("Tenant", back_populates="integrations")
    outlet = relationship("Outlet", back_populates="integrations")


class TenantBilling(Base):
    __tablename__ = "tenant_billing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    amount_due = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tenant = relationship("Tenant", back_populates="billing")


class OutletAnalytics(Base):
    __tablename__ = "outlet_analytics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    outlet_id = Column(Integer, ForeignKey("outlets.id"), nullable=False)
    date = Column(Date, nullable=False)
    total_sales = Column(DECIMAL(10, 2), default=0)
    total_orders = Column(Integer, default=0)
    customer_reviews = Column(JSON)

    outlet = relationship("Outlet", back_populates="analytics")
