from pydantic import BaseModel, ConfigDict, Field
import math
from typing import Literal

class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    reasoning_content: str = ""
    content: str = ""
    model_name: str = ""
    model_type: str = ""
    model_uid: str = ""
    create_time: int = 0
    id: str = ""
    finish_reason_cause: str = ""
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
    model_config = ConfigDict(extra="allow")
    
    id: str = ""
    reasoning_content: str = ""
    content: str = ""
    function_id: str = ""
    function_type: str = ""
    function_name: str = ""
    function_arguments: str = ""
    token_usage: TokensCount = Field(default_factory=TokensCount)
    finish_reason: Literal["stop", "length", "content_filter", "tool_calls", "insufficient_system_resource"] | None = None
    created: int = 0
    model: str = ""
    system_fingerprint: str = ""
    logprobs: list[Logprob] = Field(default_factory=list)