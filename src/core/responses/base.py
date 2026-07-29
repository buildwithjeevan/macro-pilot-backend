from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Standard API envelope. Every endpoint returns this shape.

    - code: HTTP-style status code (also mirrored in the HTTP status line)
    - data: endpoint-specific payload (or null on errors)
    - message: human-readable summary
    - status: "success" | "error"
    - timestamp: when the response was built (UTC)
    """

    code: int
    data: Optional[T] = None
    message: str
    status: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def success_response(
    data: Any = None,
    message: str = "Success",
    code: int = 200,
) -> BaseResponse:
    return BaseResponse(
        code=code,
        data=data,
        message=message,
        status="success",
    )


def error_response(
    message: str = "Error",
    code: int = 400,
    data: Any = None,
) -> BaseResponse:
    return BaseResponse(
        code=code,
        data=data,
        message=message,
        status="error",
    )
