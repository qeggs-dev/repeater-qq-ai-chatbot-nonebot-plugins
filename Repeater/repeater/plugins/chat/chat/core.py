import json
from typing import (
    Optional,
    Union,
    Tuple
)

from nonebot import logger
import httpx

from ..core_config import *

class ChatCore:
    def __init__(self, session_id: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.session_id = session_id
        
    async def send_message_and_get_image(
        self,
        message: str,
        username: str,
        model_type: str | None = None,
        load_prompt: bool = True,
        rendering: bool = True
    ) -> Tuple[str, int, str, str, str]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param session_id: 会话ID
        :param username: 用户名
        :param reason: 是否需要推理链
        :return: AI返回的消息(文件路径,状态码,响应内容, 推理链,AI回复)
        """
        url = f"{self.url}/{CHAT_ROUTE}/{self.session_id}"
        async with httpx.AsyncClient(timeout=600.0) as client:
            # 表单数据格式 (Form Data)
            data = {
                "user_name": username,
                "load_prompt": load_prompt,
                "rendering": rendering,
            }
            if model_type:
                data['model_type'] = model_type
            if message:
                MD_Rendering_Enables_Prompts = "\n> Markdown渲染已开启！！！"
                data['message'] = '> SystemInfo:\n> 消息发送时间：{time}' + (MD_Rendering_Enables_Prompts if rendering else '') + '\n\n---\n\n' + message
            response = await client.post(
                url=url,
                data=data  # 使用 data= 表示表单数据
            )
            image_url = ''
            reasoning = ''
            content = ''
            if response.status_code == 200:
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    return response.text
                image_url = result.get('image_url', '')
                file_uuid = result.get('file_uuid', '')
                reasoning = result.get('reasoning_content', '')
                content = result.get('content', '')
        return f'{self.url}/{DOWNLOAD_RENDERED_IMAGE_ROUTE}/{file_uuid}.png', response.status_code, response.text, reasoning, content
        
        
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
    # endregion