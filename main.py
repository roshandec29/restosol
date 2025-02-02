from fastapi import FastAPI
from app.db.session import DBSync
from app.db.session import Base
from app.api.v1.users import router as user_router
from app.api.v1.google_oauth import router as google_router
from starlette.middleware.sessions import SessionMiddleware

db = DBSync()
app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["RestoSol"])
app.include_router(google_router, prefix="/google_auth", tags=["RestoSol"])

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
@app.get("/health")
async def health():
    return {"status": 200, "message": "healthy"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=db.engine)