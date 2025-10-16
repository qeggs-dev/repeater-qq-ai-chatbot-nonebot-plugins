from ._config import tts_config
from ..assist import Response
from ._tts_response import TTSResponse
import httpx

class ChatTTSAPI:
    def __init__(self):
        url = tts_config.base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url = url, timeout = tts_config.timeout)
    
    async def text_to_speech(self, text: str) -> Response[TTSResponse]:
        api_args = tts_config.api_args.model_dump()
        response = await self.client.post(
            "/tts",
            data={
                **api_args,
                "text": text,
            },
        )

        try:
            return Response(
                code = response.status_code,
                text = response.text,
                data = TTSResponse(
                    **response.json()
                )
            )
        except Exception as e:
            return Response(
                code = response.status_code,
                text = response.text,
                data = TTSResponse()
            )
        