from pydantic import BaseModel, Field

class Audio_Files(BaseModel):
    filename: str = ""
    url: str = ""

class TTSResponse(BaseModel):
    code: int = 0
    message: str = "ok"
    audio_files: list[Audio_Files] = Field(default_factory=list)