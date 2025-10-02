from ..core_config import *
from ._response_body import RendedImage
from ._namespace import Namespace
import httpx

class TextRender:
    _client = httpx.AsyncClient()

    def __init__(self, namespace: str | Namespace):
        self.url = f"{BACKEND_HOST}:{BACKEND_PORT}"
        if isinstance(namespace, str):
            self.namespce = namespace
        elif isinstance(namespace, Namespace):
            self.namespce = namespace.namespace
        else:
            raise TypeError(f'namespace must be str or Namespace, not {type(namespace)}')

    async def render(self, text: str) -> RendedImage:
        response = await self._client.post(
            f'{TEXT_RENDER_ROUTE}/{self.namespce}',
            json={'text': text}
        )
        response_json:dict = response.json()
        return RendedImage(
            status_code = response.status_code,
            response_text = response.text,
            image_url = response_json.get('image_url', ''),
            style = response_json.get('style', ''),
            timeout = response_json.get('timeout', 0),
            created = response_json.get('created', 0),
            created_ms = response_json.get('created_ms', 0),
        )