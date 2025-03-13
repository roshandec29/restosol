from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import uvicorn

from typing import Any, Dict, Optional, List

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


class APIResponse(JSONResponse):
    """
    A custom response class for consistent API responses.
    """

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[dict] = None,
        media_type: Optional[str] = "application/json",
        background: Optional[Any] = None,
        message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        errors: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Initialize the CustomResponse.

        Args:
            content: The data payload of the response.
            status_code: The HTTP status code.
            headers: Custom headers.
            media_type: The media type of the response.
            background: Background tasks.
            message: A human-readable message.
            metadata: Additional metadata.
            errors: A list of error dictionaries.
        """
        response_content = {
            "status": "success" if 200 <= status_code < 300 else "error",
            "data": content,
            "message": message,
            "metadata": metadata,
            "errors": errors,
        }

        if errors:
            if not message:
              response_content["message"] = "An error occurred."

        if 200 <= status_code < 300:
            if errors:
                status_code = 500 # internal server error if errors are in successful response, this is not good.
        else:
            if content is None:
                del response_content["data"]
            if response_content["status"] == "success":
                response_content["status"] = "error" #force status to error if status code is not 2xx.

        super().__init__(
            content=response_content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_exception:
        # Handle HTTP exceptions (e.g., 404, 400)
        return APIResponse(
            status_code=http_exception.status_code,
            message=http_exception.detail,
        )
    except Exception as e:
        # Handle other exceptions (e.g., database errors)
        print(f"An error occurred: {e}")
        return APIResponse(
            status_code=500,
            message="Internal server error",
        )


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