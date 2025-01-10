from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    is_success: bool = Field(default=True)
    error: Optional[str] = None
    data: T