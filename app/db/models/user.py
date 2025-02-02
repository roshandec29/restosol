from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(255))
    date_of_birth = Column(DateTime, nullable=True)
    hashed_password = Column(String(1055))
    is_active = Column(Boolean, default=True)
    is_global_admin = Column(Boolean, default=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=True)
    phone_verified = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    preferences = Column(String(255), nullable=True)

    tenant = relationship('Tenant', back_populates='users')
    outlet = relationship('Outlet', back_populates='users')
    roles = relationship('UserRole', back_populates='user')
    global_admin = relationship('GlobalAdmin', uselist=False, back_populates='user')
    address = relationship('Address', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


class GlobalAdmin(Base):
    __tablename__ = 'global_admins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)  # Link to User
    user = relationship('User', back_populates='global_admin')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<GlobalAdmin(id={self.id}, user_id={self.user_id})>"


class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=True)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='user_roles')
    tenant = relationship('Tenant', back_populates='user_roles')
    outlet = relationship('Outlet', back_populates='user_roles')

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id}, tenant_id={self.tenant_id}, outlet_id={self.outlet_id})>"


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('User', back_populates='address')

    def __repr__(self):
        return f"<Address(user_id={self.user_id}, street_address={self.street_address}, city={self.city})>"
