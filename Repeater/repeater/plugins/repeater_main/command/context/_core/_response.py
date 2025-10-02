from pydantic import BaseModel
from typing import Generic, TypeVar
from dataclasses import dataclass

T_Response = TypeVar("T_Response")

@dataclass
class Response(Generic[T_Response]):
    status_code: int = 0
    response_text: str = ""
    response_body: T_Response | None = None

class WithdrawResponse(BaseModel):
    status: str = "success"
    deleted: int = 0
    context: list

class ContextTotalLengthResponse(BaseModel):
    total_context_length: int = 0
    context_length: int = 0
    average_content_length: float = 0.0