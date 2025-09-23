from typing import Generic, TypeVar
from dataclasses import dataclass, asdict

@dataclass
class RendedImage:
    status_code: int = 0
    response_text: str = ""
    image_url: str = ""
    style: str = ""
    timeout: int = 0
    created: str = ""
    created_ms: str = ""

    @property
    def as_dict(self):
        return asdict(self)

T_Response = TypeVar("T_Response")

@dataclass
class Response(Generic[T_Response]):
    status_code: int = 0
    response_text: str = ""
    response_body: T_Response | None = None