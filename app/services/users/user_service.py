from sqlalchemy.orm import Session
from app.services.users.models.user import User, UserRole
from app.services.users.models.roles import Role
from app.services.users.utils.token_utils import decode_token
from app.services.users.utils.password_utils import verify_password, hash_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.schema.user_schema import UserResponse
from app.db.session import DBSync, DBManager
from app.services.users.models.tenant import Tenant, Outlet
from app.utils.sms_utils import SMSUtils
from app.services.communication.models.otp import OTPModel
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, username: str) -> User | None:
        """
        Fetch a user from the database by username.
        """
        result = self.db.query(User).filter(
            User.username == username,
            User.is_active == True
        ).first()

        return result

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.query(UserRole).filter(UserRole.user_id == user_id).delete(synchronize_session=False)

        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted"}


def get_user(db: Session, username: str) -> User | None:
    """
    Fetch a user from the database by username.
    """
    result = db.query(User).filter(
        User.username == username,
        User.is_active == True
    ).first()

    return result if result else None


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Fetch a user from the database by email.
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Authenticate a user by verifying the username and password.
    """
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Get the current authenticated user from the JWT token.
    """
    db = DBSync()
    session = db.get_new_session()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token to get the payload
        payload = decode_token(token)
        username: str = payload.get("username")
        if not username:
            raise credentials_exception
    except Exception as e:
        raise credentials_exception from e

    # Query the user from the database
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    # Transform SQLAlchemy model to Pydantic response model
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        name=user.name,
        phone=user.phone,
        date_of_birth=user.date_of_birth,
        is_active=user.is_active,
        phone_verified=user.phone_verified,
        email_verified=user.email_verified,
        last_login=user.last_login,
        created_at=user.created_at,
        preferences=user.preferences
    )


def user_registration(user, session, db):

    user_data = get_user(session, user.username)

    if user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    email_data = session.query(User).filter(User.email == user.email).first()
    if email_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if user.tenant_id is None or user.outlet_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant ID and Outlet ID are required for non-global admin users"
        )

    tenant = session.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant not found"
        )

    outlet = session.query(Outlet).filter(Outlet.id == user.outlet_id).first()
    if not outlet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Outlet not found"
        )

    customer_role = session.query(Role.id).filter(Role.name == "customer",
                                                  Role.tenant_id == user.tenant_id).first()
    if not customer_role:
        raise ValueError(f"Role 'customer' not found for tenant {user.tenant_id}")

    new_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        phone=user.phone,
        date_of_birth=user.date_of_birth,
        hashed_password=hash_password(user.password),
        tenant_id=user.tenant_id,
        outlet_id=user.outlet_id,
        is_active=True,
        phone_verified=True if user.phone_verified else False,
        email_verified=True if user.email_verified else False,
        preferences=None
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    user_role = UserRole(
        role_id=customer_role.id,
        user_id=new_user.id,
        tenant_id=user.tenant_id,
        outlet_id=user.outlet_id
    )

    session.add(user_role)
    session.commit()
    session.refresh(new_user)

    response = UserResponse(
        id=new_user.id,
        role_id=user_role.role_id,
        username=new_user.username,
        email=new_user.email,
        name=new_user.name,
        phone=new_user.phone,
        date_of_birth=new_user.date_of_birth,
        is_active=new_user.is_active,
        phone_verified=new_user.phone_verified,
        email_verified=new_user.email_verified,
        last_login=new_user.last_login,
        created_at=new_user.created_at,
        preferences=new_user.preferences,
        tenant_id=new_user.tenant_id,
        outlet_id=new_user.outlet_id
    )

    db.close_session(session)

    return response


def user_otp_generate(session, data):
    user = session.query(User).filter(User.phone == data.phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="User with this phone not found.")

    otp = SMSUtils().generate_otp(session, data.phone)

    return otp


def verify_user_otp(db, request):
    otp_entry = (
        db.query(OTPModel)
        .filter(OTPModel.phone_number == request.phone_number)
        .order_by(OTPModel.created_at.desc())
        .first()
    )

    if not otp_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid OTP.")

    now = datetime.now(timezone.utc)

    # Ensure created_at is timezone-aware
    if otp_entry.created_at.tzinfo is None:
        otp_created_at = otp_entry.created_at.replace(tzinfo=timezone.utc)
    else:
        otp_created_at = otp_entry.created_at

    if now - otp_created_at > timedelta(minutes=5):
        db.delete(otp_entry)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP expired.")

    if otp_entry.otp != request.otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP.")

    db.delete(otp_entry)
    db.commit()
    return True



