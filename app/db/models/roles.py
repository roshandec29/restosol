from pydantic import BaseModel
from enum import Enum
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class RoleEnum(str, Enum):
    ADMIN = "admin"
    RESTAURANT_ADMIN = "restaurant_admin"
    RESTAURANT_STAFF = "restaurant_staff"
    DELIVERY_BOY = "delivery_boy"
    END_USER = "end_user"


class PermissionEnum(str, Enum):
    CREATE_RESTAURANT = "create_restaurant"
    DELETE_RESTAURANT = "delete_restaurant"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_BILLING = "manage_billing"
    CONFIGURE_SETTINGS = "configure_settings"
    MANAGE_ORDERS = "manage_orders"
    VIEW_ORDERS = "view_orders"
    UPDATE_DELIVERY_STATUS = "update_delivery_status"
    RATE_RESTAURANT = "rate_restaurant"
    UPDATE_PROFILE = "update_profile"


class RolePermissions(BaseModel):
    role: RoleEnum
    permissions: List[PermissionEnum]


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)  # e.g. 'platform_admin', 'restaurant_admin'
    description = Column(String(255))
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=True)  # Tenant-specific roles

    tenant = relationship('Tenant', back_populates='roles')  # Relationship to Tenant
    user_roles = relationship('UserRole', back_populates='role')
    role_permissions = relationship('RolePermission', back_populates='role')

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"


class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)

    role = relationship('Role', back_populates='role_permissions')
    permission = relationship('Permission', back_populates='role_permissions')

    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)  # e.g. 'manage_restaurant', 'view_analytics'
    description = Column(String(255))

    role_permissions = relationship('RolePermission', back_populates='permission')

    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name})>"
