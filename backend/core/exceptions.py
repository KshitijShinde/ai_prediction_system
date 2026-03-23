from fastapi import Request
from fastapi.responses import JSONResponse
from backend.core.logging import logger

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)}
    )
