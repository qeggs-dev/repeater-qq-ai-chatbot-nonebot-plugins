from pydantic import BaseModel, Field
from ..configs import Loader, Mode

class StorageConfigs(BaseModel):
    max_text_length: int = 400
    max_single_line_length: int = 64
    max_text_lines: int = 5
    hello_content: str = "Repeater Is Ready!"
    welcome_messages_by_weekday: dict[int | str, str] = Field(default_factory=dict, max_length=7)

loader: Loader[StorageConfigs] = Loader(
    model=StorageConfigs,
    path="configs/main_api.json",
    mode=Mode.JSON
)
storage_config: StorageConfigs = loader.load(write_on_failure=True)