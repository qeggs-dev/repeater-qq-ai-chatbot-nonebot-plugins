from pydantic import BaseModel

class WithdrawResponse(BaseModel):
    status: str = "success"
    deleted: int = 0
    context: list

class ContextTotalLengthResponse(BaseModel):
    total_context_length: int = 0
    context_length: int = 0
    average_content_length: float = 0.0