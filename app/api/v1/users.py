from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.users.utils.token_utils import create_access_token, create_refresh_token, decode_token
from app.services.communication.utils.email import send_email, registration_email
from app.db.schema.user_schema import Token, UserResponse, UserRegisterRequest, UserResponseWithToken, OTPRequest, VerifyOTPRequest
from app.services.users.user_service import authenticate_user, get_user, user_registration, UserService, user_otp_generate, verify_user_otp
from app.db.session import DBSync, DBManager, get_db
import asyncio
router = APIRouter()


@router.post("/auth/request-otp")
async def request_otp(data: OTPRequest):
    session = DBSync().get_new_session()
    otp = user_otp_generate(session, data)
    if otp:
        return {"message": f"OTP sent successfully. {otp}"}
    else:
        raise HTTPException(
            status_code=400,
            detail="OTP not sent"
        )


@router.post("/auth/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    # Fetch OTP entry
    session = DBSync().get_new_session()

    verified = verify_user_otp(session, request)

    if verified:
        return {"message": "OTP verified successfully."}
    else:
        raise HTTPException(
            status_code=400,
            detail="Not a valid OTP"
        )


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    session = DBSync().get_new_session()
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_data= {
                  "id": user.id,
                  "name": user.name,
                  "username": user.username,
                  "email": user.email,
                  "phone": user.phone,
                  "is_active": user.is_active,
                  "is_global_admin": user.is_global_admin,
                  "tenant_id": user.tenant_id,
                  "outlet_id": user.outlet_id,
                  "phone_verified": user.phone_verified,
                  "email_verified": user.email_verified,
                }

    access_token = create_access_token(data= user_data)
    refresh_token = create_refresh_token(user_data)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_access_token({"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Refresh token error: {e}")


@router.get("/get_user", response_model=UserResponse)
async def read_users_me(username: str, db: Session = Depends(get_db)):
    user_service_obj = UserService(db)
    current_user = user_service_obj.get_user(username)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        name=current_user.name,
        phone=current_user.phone,
        date_of_birth=current_user.date_of_birth,
        phone_verified=current_user.phone_verified,
        email_verified=current_user.email_verified,
        last_login=current_user.last_login,
        created_at=current_user.created_at,
        preferences=current_user.preferences
    )


@router.post("/register", response_model=UserResponseWithToken, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegisterRequest):
    db = DBSync()
    session = db.get_new_session()
    response = user_registration(user, session, db)
    if response and response.username:
        user_data = {
            "id": response.id,
            "role_id": response.role_id,
            "name": response.name,
            "username": response.username,
            "email": response.email,
            "phone": response.phone,
            "is_active": response.is_active,
            "tenant_id": response.tenant_id,
            "outlet_id": response.outlet_id,
            "phone_verified": response.phone_verified,
            "email_verified": response.email_verified,
        }
        access_token = create_access_token(data=user_data)
        refresh_token = create_refresh_token(user_data)
        try:
            loop = asyncio.get_running_loop()  # Safe inside async functions
        except RuntimeError:
            loop = asyncio.new_event_loop()  # Create a new loop if necessary
            asyncio.set_event_loop(loop)
        loop.create_task(send_email(response.email, "Registration Successful!", registration_email()))
        return user_data | {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    return response

@router.delete("/users/{user_id}")
def delete_menu(user_id: int):
    db = DBSync().get_new_session()
    return UserService(db).delete_user(user_id)
