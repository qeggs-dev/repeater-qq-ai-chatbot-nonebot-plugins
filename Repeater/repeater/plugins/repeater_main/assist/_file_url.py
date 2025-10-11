from pathlib import Path

class FileUrl:
    def __init__(self, url_or_path: str | Path):
        self._url_or_path = Path(url_or_path)
    
    @property
    def value(self):
        try:
            return self._url_or_path.as_uri()
        except ValueError:
            return str(self._url_or_path)
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def path(self) -> Path:
        return self._url_or_path