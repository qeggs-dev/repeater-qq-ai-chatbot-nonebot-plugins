from pydantic import BaseModel, Field
from typing import Literal
from ..config_loader import Loader, Mode

class API_ARGS(BaseModel):
    voice: str = ""
    speed: int = 6
    tts_prompt: str = "[break_6]"
    temperature: float = 0.2
    top_p: float = 0.7
    top_k: int = 20
    refine_max_new_token: int = 384
    infer_max_new_token: int = 2048
    text_seed: int = 42
    skip_refine: Literal[1, 0] = 1
    is_stream: Literal[1, 0] = 0
    custom_voice: int = 0
    

class TTSConfig(BaseModel):
    base_url: str = "http://127.0.0.1:8123"
    api_args: API_ARGS = Field(default_factory=API_ARGS)
    timeout: float = 60.0

loader: Loader[TTSConfig] = Loader(
    model = TTSConfig,
    path = "configs/tts.json",
    mode = Mode.JSON
)

tts_config: TTSConfig = loader.load(write_on_failure=True)