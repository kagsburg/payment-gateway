from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException, Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.payments import router as payments_router
from app.services.payment import error_response 
from app.models.database import Base, engine
import logging

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
app = FastAPI(title="Payment Gateway API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Optional: log the original error
    logging.warning(f"Validation error: {exc}")
    first_error = exc.errors()[0]['msg']
    return error_response(first_error, status_code=422)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(exc.detail, status_code=exc.status_code)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return error_response("An unexpected error occurred", status_code=500)
if __name__ == "__main__":
    # Create database tables
    Base.metadata.create_all(bind=engine)

app.include_router(payments_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Payment Gateway API"}