import httpx

from ..core_config import *

class ChatCore:
    def __init__(self, session_id: str):
        self.url = f"{BACKEND_HOST}:{BACKEND_PORT}"
        self.session_id = session_id
    
    async def get_balance(self):
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.get(
                url = f"{self.url}/{BALANCE_ROUTE}"
            )
        return response.status_code, response.text