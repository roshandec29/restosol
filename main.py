from fastapi import FastAPI, HTTPException
from app.db.session import DBSync
from app.db.session import Base
from app.api.v1.users import router as user_router
from app.api.v1.google_oauth import router as google_router
from starlette.middleware.sessions import SessionMiddleware
from app.db.schema.email import EmailRequest
from app.utils.email import send_email


db = DBSync()
app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["RestoSol"])
app.include_router(google_router, prefix="/google_auth", tags=["RestoSol"])
app.add_middleware(SessionMiddleware, secret_key="9b847788b25b7551a4f5143f47c324f7166b67cb1856f6f68b75228a202fd83d")

@app.get("/health")
async def health():
    return {"status": 200, "message": "healthy"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=db.engine)


@app.post("/send-email/")
async def send_email_api(email_data: EmailRequest):
    success = await send_email(email_data.recipient, email_data.subject, email_data.message)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")

    return {"message": "Email sent successfully"}