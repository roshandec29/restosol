from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    is_active: Optional[bool] = True
    phone_verified: Optional[bool] = False
    email_verified: Optional[bool] = False
    preferences: Optional[str] = None
    tenant_id: Optional[int] = None
    outlet_id: Optional[int] = None
    role_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes= True


class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    tenant_id: Optional[int] = None
    outlet_id: Optional[int] = None
    email_verified: bool = False
    phone_verified: bool = False
    is_global_admin: bool = False



# GlobalAdmin-related schemas
class GlobalAdminBase(BaseModel):
    is_active: Optional[bool] = True


class GlobalAdminCreate(GlobalAdminBase):
    user_id: int


class GlobalAdminResponse(GlobalAdminBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes= True


# UserRole-related schemas
class UserRoleBase(BaseModel):
    tenant_id: Optional[int] = None
    outlet_id: Optional[int] = None


class UserRoleCreate(UserRoleBase):
    user_id: int
    role_id: int


class UserRoleResponse(UserRoleBase):
    user_id: int
    role_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes= True


# Address-related schemas
class AddressBase(BaseModel):
    street_address: str
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str
    is_active: Optional[bool] = True


class AddressCreate(AddressBase):
    user_id: int


class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes= True


class UserResponseWithToken(UserResponse, Token):
    pass

class OTPRequest(BaseModel):
    phone: str
