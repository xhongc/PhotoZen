from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class SuccessResponse(Generic[T], BaseModel):
    msg: str
    data: Optional[T] = None
    result: bool

class ErrorResponse(BaseModel):
    msg: str
    result: bool
