from typing import Generic, TypeVar
from dataclasses import dataclass

T_Response = TypeVar("T_Response")

@dataclass
class Response(Generic[T_Response]):
    code: int = 0
    text: str = ""
    data: T_Response | None = None