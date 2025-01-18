from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any

class BookAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": request.url.path
            }
        },
    )

# Custom exceptions
class DatabaseError(BookAPIException):
    def __init__(self):
        super().__init__(503, "Database service unavailable")

class ValidationError(BookAPIException):
    def __init__(self, detail: str):
        super().__init__(422, detail)

class NotFoundError(BookAPIException):
    def __init__(self, resource: str):
        super().__init__(404, f"{resource} not found")