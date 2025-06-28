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

    # region send message
    async def send_message(
        self,
        message: str,
        username: str,
        model_type: str,
        load_prompt:bool=True,
        recomplete:bool=False,
        temperature:Optional[float]=None
    ) -> Union[dict, int]:
        """
        发送消息到AI后端

        :param message: 消息内容
        :param session_id: 会话ID
        :param username: 用户名
        :param reason: 是否需要推理链
        :return: AI返回的消息
        """
        url = f"{self.url}/{CHAT_ROUTE}/{self.session_id}"
        async with httpx.AsyncClient(timeout=600.0) as client:
            # 表单数据格式 (Form Data)
            data = {
                "username": username,       # 可选字段
                "model_type": model_type,
                "load_prompt": load_prompt,
                "recomplete": recomplete,
            }
            if temperature:
                data['temperature'] = temperature
            if message:
                data['text'] = '> SystemInfo:\n> 消息发送时间：{time}\n> Markdown渲染已开启！！！\n\n---\n\n' + message
            response = await client.post(
                url=url,
                data=data  # 使用 data= 表示表单数据
            )
        response = ''
        content = ''
        if response.status_code == 200:
            code = response.status_code
            try:
                result = response.json()
            except json.JSONDecodeError:
                return response.text, code
            content = result.get('response', '')
            reasoning = result.get('reasoning', None)
            logger.debug(f"AI Response: {response}")
            if len(response) > MAX_LENGTH:
                response = '<AI Response Too Long>'
        return reasoning, content, response.text, response.status_code
        
    async def send_message_and_get_image(
        self,
        message: str,
        username: str,
        model_type:str,
        load_prompt:bool=True,
        recomplete:bool=False,
        temperature:Optional[float]=None
    ) -> Tuple[str, str, int, str]:
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
                "username": username,       # 可选字段
                "model_type": model_type,
                "load_prompt": load_prompt,
                "rendering": True,
                "recomplete": recomplete,
            }
            if temperature:
                data['temperature'] = temperature
            if message:
                data['text'] = '> SystemInfo:\n> 消息发送时间：{time}\n> Markdown渲染已开启！！！\n\n---\n\n' + message
            response = await client.post(
                url=url,
                data=data  # 使用 data= 表示表单数据
            )
        filename = ''
        reasoning = ''
        content = ''
        if response.status_code == 200:
            try:
                result = response.json()
            except json.JSONDecodeError:
                return response.text
            filename = result.get('filename', '')
            reasoning = result.get('reasoning', '')
            content = result.get('response', '')
        return f'{self.url}/{DOWNLOAD_RENDERED_IMAGE_ROUTE}/{filename}', response.status_code, response.text, reasoning, content
        
        
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