from pydantic import BaseModel, ConfigDict, Field
from enum import StrEnum
import math

class FinishReason(StrEnum):
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    TOOL_CALL = "tool_calls"
    INSUFFICIENT_SYSTEM_RESOURCE = "insufficient_system_resource"

class ChatResponse(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow",
    )

    reasoning_content: str | None = None
    content: str | None = None
    user_raw_input: str | None = None
    model_group: str | None = None
    model_name: str | None = None
    model_type: str | None = None
    model_uid: str | None = None
    create_time: int | None = None
    id: str | None = None
    finish_reason_cause: str | None = None
    finish_reason_code: FinishReason | None = None
    status: int = 200

class TokensCount(BaseModel):
    """
    Dataclass to store the token usage data for a given date.
    """
    prompt_tokens:int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    prompt_cache_hit_tokens: int = 0
    prompt_cache_miss_tokens: int = 0

    @property
    def prompt_cache_hit_ratio(self) -> float:
        if self.prompt_cache_hit_tokens is not None and self.prompt_cache_miss_tokens is not None:
            if self.prompt_cache_hit_tokens + self.prompt_cache_miss_tokens > 0:
                return self.prompt_cache_hit_tokens / (self.prompt_cache_hit_tokens + self.prompt_cache_miss_tokens)
        return math.nan

class Top_Logprob(BaseModel):
    token: str = ""
    logprob: float = 0.0

class Logprob(BaseModel):
    """
    Dataclass to store the logprobs data for a given date.
    """
    token: str = ""
    logprob: float = 0.0
    top_logprobs: list[Top_Logprob] = Field(default_factory=list)

class StreamChatChunkResponse(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow",
    )
    
    id: str = ""
    reasoning_content: str = ""
    content: str = ""
    function_id: str = ""
    function_type: str = ""
    function_name: str = ""
    function_arguments: str = ""
    token_usage: TokensCount = Field(default_factory=TokensCount)
    finish_reason: FinishReason | None = None
    created: int = 0
    model: str = ""
    system_fingerprint: str = ""
    logprobs: list[Logprob] = Field(default_factory=list)