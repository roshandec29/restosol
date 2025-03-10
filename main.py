from fastapi import FastAPI, HTTPException
import os
import uvicorn

from app.db.session import Base, init_db
from app.api.v1.users import router as user_router
from app.api.v1.google_oauth import router as google_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.menu import router as menu_router
from starlette.middleware.sessions import SessionMiddleware
from app.db.schema.email import EmailRequest
from app.services.communication.utils.email import send_email
from app.config import config
from app.core.startup import seed_data
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=init_db(config.DB_URL).engine)
    seed_data()


app = FastAPI(lifespan=lifespan)

SECRET_KEY=config.SECRET_KEY


app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["RestoSol"])
app.include_router(google_router, prefix="/google_auth", tags=["RestoSol"])
app.include_router(menu_router, prefix="/menu", tags=["RestoSol"])
app.include_router(inventory_router, prefix="/inventory", tags=["RestoSol"])
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.get("/health")
async def health():
    return {"status": 200, "message": "healthy"}


@app.post("/send-email/")
async def send_email_api(email_data: EmailRequest):
    success = await send_email(email_data.recipient, email_data.subject, email_data.message)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")

    return {"message": "Email sent successfully"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)