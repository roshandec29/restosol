from fastapi import FastAPI
from app.db.session import DBSync
from app.db.session import Base

db = DBSync()
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": 200, "message": "healthy"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=db.engine)