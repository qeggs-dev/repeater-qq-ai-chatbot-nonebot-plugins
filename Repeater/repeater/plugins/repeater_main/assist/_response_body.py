from typing import Generic, TypeVar
from dataclasses import dataclass

T_Response = TypeVar("T_Response")

@dataclass
class Response(Generic[T_Response]):
    code: int = 200
    text: str = ""
    data: T_Response | None = None

    def __bool__(self) -> bool:
        return self.code == 200