import json
from typing import (
    Any,
    Literal,
    AsyncIterator
)

from nonebot import logger
import httpx
from ..exit_register import ExitRegister

from ..core_config import *

exit_register = ExitRegister()

class ChatCore:
    _chat_client = httpx.AsyncClient(timeout=600.0)
    _client = httpx.AsyncClient()
    
    def __init__(self, session_id: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.session_id = session_id
    async def send_message(
        self,
        message: str,
        username: str,
        role_name: str | None = None,
        model_type: str | None = None,
        load_prompt: bool = True,
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
    ) -> dict[Literal["status_code", "response_text", "reasoning", "content"], str | int]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param username: 用户名
        :
        :return: AI返回的消息
        """
        url = f"{self.url}/{CHAT_ROUTE}/{self.session_id}"
        data = self._prepare_request_body(
            message = message,
            username = username,
            role_name = role_name,
            model_type = model_type,
            load_prompt = load_prompt,
            enable_md_prompt = enable_md_prompt,
            reference_context_id = reference_context_id,
        )
        response = await self._chat_client.post(
            url=url,
            json=data  # 使用 json= 表示请求体数据
        )
        reasoning = ''
        content = ''
        if response.status_code == 200:
            try:
                result:dict = response.json()
            except json.JSONDecodeError:
                return response.text
            reasoning = result.get('reasoning_content', '')
            content = result.get('content', '')
        return {
            "status_code": response.status_code,
            "response_text": response.text,
            "reasoning": reasoning,
            "content": content
        }
    
    async def send_stream_message(
        self,
        message: str,
        username: str,
        role_name: str | None = None,
        model_type: str | None = None,
        load_prompt: bool = True,
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
    ) -> AsyncIterator[Any]:
        """
        发送消息到AI后端，并获取流式响应
        
        :param message: 消息内容
        :param username: 用户名
        :
        :return: AI返回的消息
        """
        import json
        url = f"{self.url}/{CHAT_ROUTE}/{self.session_id}"
        data = self._prepare_request_body(
            message = message,
            username = username,
            role_name = role_name,
            model_type = model_type,
            load_prompt = load_prompt,
            enable_md_prompt = enable_md_prompt,
            reference_context_id = reference_context_id,
        )
        async with self._chat_client.stream(
            method="POST",
            url=url,
            json=data  # 使用 json= 表示请求体数据
        ) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                yield json.loads(line)
    
    def _prepare_request_body(
        self,
        message: str,
        username: str,
        role_name: str | None = None,
        model_type: str | None = None,
        load_prompt: bool = True,
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
    ):
        # 表单数据格式 (Form Data)
        data = {
            "user_name": username,
            "load_prompt": load_prompt,
        }
        if model_type:
            data['model_type'] = model_type
        if role_name:
            data['role_name'] = role_name
        if reference_context_id:
            data['reference_context_id'] = reference_context_id
        if message:
            MD_Rendering_Enables_Prompts = "\n> Markdown rendering is turned on!!"
            MD_Rendering_Enables_Prompts = MD_Rendering_Enables_Prompts if enable_md_prompt else ''
            Reference_Enables_Prompts = "\n> Guest mode(User: {user_name})，Citation context is turned on!!"
            Reference_Enables_Prompts = Reference_Enables_Prompts if reference_context_id else ''
            data['message'] = '> SystemInfo:\n> Message sending time:{time}' + (MD_Rendering_Enables_Prompts) + (Reference_Enables_Prompts) + '\n\n---\n\n' + message
        return data
    
    async def text_render(self, text: str) -> dict[Literal['status_code', 'response_text', 'image_url', 'style', 'timeout', 'created', 'created_ms'], str | int]:
        response = await self._client.post(
            f'{self.url}/{TEXT_RENDER_ROUTE}/{self.session_id}',
            data={'text': text}
        )
        response_json:dict = response.json()
        return {
            "status_code": response.status_code,
            "response_text": response.text,
            "image_url": response_json.get('image_url', ''),
            "style": response_json.get('style', ''),
            "timeout": response_json.get('timeout', 0),
            "created": response_json.get('created', 0),
            "created_ms": response_json.get('created_ms', 0),
        }
    async def content_render(self, content: str, reasoning_content: str = ""):
        text = ""
        if reasoning_content:
            text += ("> " + reasoning_content.replace('\n', '\n> ') + "\n\n---\n\n")
        text += content

        return await self.text_render(text)
        
    async def inject_context(self, text: str, role: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{self.url}/{INJECT_CONTEXT_ROUTE}/{self.session_id}',
                data={
                    'text': text,
                    'role': role
                }
            )
        return response.status_code, response.text
    
    exit_register.register()
    async def close(self):
        await self._chat_client.aclose()
        await self._client.aclose()
    # endregion