from sqlalchemy.orm import Session
from app.db.models.user import User
from app.utils.utils import verify_password, decode_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.schema.user_schema import Token, UserResponse
from app.db.session import DBSync
from app.db.models.tenant import Tenant, Outlet
from app.utils.utils import hash_password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str) -> User | None:
    """
    Fetch a user from the database by username.
    """
    result = db.query(User).filter(User.username == username).first()

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

    # Validate tenant and outlet for non-global admin users
    if not user.is_global_admin:
        if user.tenant_id is None or user.outlet_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant ID and Outlet ID are required for non-global admin users"
            )

        # Check if tenant and outlet exist
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
    else:
        # For global admin users, set tenant_id and outlet_id to None
        user.tenant_id = None
        user.outlet_id = None

    # Create new user
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
    db.close_session(session)

    return UserResponse(
        id=new_user.id,
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