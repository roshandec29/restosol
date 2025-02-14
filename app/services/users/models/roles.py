from pydantic import BaseModel
from enum import Enum
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base import Base


class RoleEnum(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    CASHIER = "cashier"
    STAFF = "staff"
    SUPPLIER = "supplier"
    CUSTOMER = "customer"


class PermissionEnum(str, Enum):
    # User Management
    CREATE_USER = "create_user"
    UPDATE_USER = "update_user"
    DISABLE_USER = "disable_user"

    # Access Control
    MANAGE_ROLES = "manage_roles"
    MULTI_LOCATION_ACCESS = "multi_location_access"

    # Sales & Transactions
    PROCESS_PAYMENT = "process_payment"
    REFUND_PAYMENT = "refund_payment"
    GENERATE_INVOICE = "generate_invoice"

    # Inventory Management
    ADD_INVENTORY = "add_inventory"
    EDIT_INVENTORY = "edit_inventory"
    TRACK_INVENTORY = "track_inventory"

    # Service Management
    MANAGE_SERVICES = "manage_services"

    # Bookings & Reservations
    MANAGE_BOOKINGS = "manage_bookings"

    # Reporting & Analytics
    VIEW_REPORTS = "view_reports"

    # Marketing & Promotions
    CREATE_PROMOTIONS = "create_promotions"

    # Audit & Logs
    VIEW_AUDIT_LOGS = "view_audit_logs"


class RolePermissions(BaseModel):
    role: RoleEnum
    permissions: List[PermissionEnum]


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)  # e.g. 'platform_admin', 'outlet_admin'
    description = Column(String(255), nullable=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=True)  # Tenant-specific roles

    tenant = relationship('Tenant', back_populates='roles')  # Relationship to Tenant
    user_roles = relationship('UserRole', back_populates='role')
    role_permissions = relationship('RolePermission', back_populates='role')

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    permission_id = Column(Integer, ForeignKey('permissions.id'))

    role = relationship('Role', back_populates='role_permissions')
    permission = relationship('Permission', back_populates='role_permissions')

    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)  # e.g. 'manage_outlet', 'view_analytics'
    category = Column(String(255))
    description = Column(String(255))

    role_permissions = relationship('RolePermission', back_populates='permission')

    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name})>"
