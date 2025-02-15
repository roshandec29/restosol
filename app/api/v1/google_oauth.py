from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
from fastapi import APIRouter
from app.api.v1.users import register_user, login
from app.db.schema.user_schema import UserRegisterRequest
from fastapi.security import OAuth2PasswordRequestForm
from app.config import config
router = APIRouter()

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID = config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = config.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = config.GOOGLE_REDIRECT_URI
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Scopes for Google OAuth2
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

@router.get("/auth/google")
async def login_with_google(request: Request, tenant_id: str, outlet_id: str, context: str = None):
    request.session["tenant_id"] = tenant_id
    request.session["outlet_id"] = outlet_id
    request.session["context"] = context
    auth_url = (
        f"{GOOGLE_AUTH_URL}?"
        f"response_type=code&"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"scope={' '.join(SCOPES)}&"
        f"access_type=offline&"
        f"include_granted_scopes=true"
    )
    return RedirectResponse(auth_url)

@router.get("/auth/google/callback")
async def google_callback(request: Request, code: str):

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        user_info_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_info_response.json()
        tenant_id = request.session.get("tenant_id")
        outlet_id = request.session.get("outlet_id")
        context = request.session.get("context")

        if context=="register":
            new_user = UserRegisterRequest(**{
                          "username": user_info.get("email"),
                          "email": user_info.get("email"),
                          "password": f"{user_info.get('email')}+!12&*^%$#",
                          "name": user_info.get("name"),
                          "phone": None,
                          "tenant_id": tenant_id,
                          "outlet_id": outlet_id,
                          "is_global_admin": False,
                          "email_verified": user_info.get("verified_email")
                        })

            response = register_user(new_user)

        else:
            data = {
                "username": user_info.get("email"),
                "password": f"{user_info.get('email')}+!12&*^%$#"
            }
            response = await login(OAuth2PasswordRequestForm(**data))


    return response

@router.get("/logout")
async def logout(request: Request):
    """
    Log out the user by clearing the session.
    """
    request.session.clear()
    return {"message": "Logged out successfully"}

@router.get("/protected")
async def protected_route(request: Request):
    """
    A protected route that requires the user to be logged in.
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"message": "You are authenticated", "user": user}