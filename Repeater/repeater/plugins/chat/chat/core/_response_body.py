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

@dataclass
class ResponseBody:
    status_code: int = 0
    response_text: str = ""
    reasoning_content: str = ""
    content: str = ""

    @property
    def as_dict(self):
        return asdict(self)

