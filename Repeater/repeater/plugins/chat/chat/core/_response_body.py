from dataclasses import dataclass, asdict

@dataclass
class ResponseBody:
    status_code: int = 0
    response_text: str = ""
    reasoning_content: str = ""
    content: str = ""

    @property
    def as_dict(self):
        return asdict(self)

