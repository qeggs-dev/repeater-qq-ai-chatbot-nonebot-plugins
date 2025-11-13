from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from ..configs import Loader, Mode

T = TypeVar("T")

class TextLengthScoreThreshold(BaseModel):
    group: float = 1.0
    private: float = 2.48

class TextLengthScoreConfigs(BaseModel):
    lines: int = 5
    single_line_max: int = 64
    mean_line_max: int = 32
    total_length: int = 400
    threshold: TextLengthScoreThreshold = Field(default_factory = TextLengthScoreThreshold)
    

class StorageConfigs(BaseModel):
    text_length_score_configs: TextLengthScoreConfigs = Field(default_factory = TextLengthScoreConfigs)
    reason_model_uid: str = "reasoner"
    hello_content: str = "Repeater Is Ready!"
    welcome_messages_by_weekday: dict[int | str, str] = Field(default_factory=dict, max_length=7)

loader: Loader[StorageConfigs] = Loader(
    model=StorageConfigs,
    path="configs/main_api.json",
    mode=Mode.JSON
)
storage_config: StorageConfigs = loader.load(write_on_failure=True)