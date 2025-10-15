import json
from typing import (
    Any,
    Literal,
    AsyncIterator
)

from nonebot import logger
import httpx
from ._response_body import ChatResponse, StreamChatChunkResponse
from ....exit_register import ExitRegister
from ....assist import StrangerInfo, TextRender, RendedImage, Response

from ....core_net_configs import *

exit_register = ExitRegister()

class ChatCore:
    _chat_client = httpx.AsyncClient(timeout=600.0)
    _client = httpx.AsyncClient()
    
    def __init__(self, strangerinfo: StrangerInfo):
        self._strangerinfo = strangerinfo
        self._text_render = TextRender(namespace = self._strangerinfo.namespace)
    
    async def send_message(
        self,
        message: str,
        role_name: str | None = None,
        model_uid: str | None = None,
        load_prompt: bool = True,
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
    ) -> Response[ChatResponse]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param username: 用户名
        :
        :return: AI返回的消息
        """
        url = f"{CHAT_ROUTE}/{self._strangerinfo.namespace_str}"
        data = self._prepare_request_body(
            message = message,
            role_name = role_name,
            model_uid = model_uid,
            load_prompt = load_prompt,
            enable_md_prompt = enable_md_prompt,
            reference_context_id = reference_context_id,
        )
        response = await self._chat_client.post(
            url=url,
            json=data  # 使用 json= 表示请求体数据
        )
        if response.status_code == 200:
            try:
                result:dict = response.json()
            except json.JSONDecodeError:
                return Response(
                    code = response.status_code,
                    text = response.text,
                    data = ChatResponse()
                )
        try:
            response_body = ChatResponse(
                **result
            )
        except Exception as e:
            response_body = ChatResponse()
            
        return Response(
            code = response.status_code,
            text = response.text,
            data = response_body
        )
    
    async def send_stream_message(
        self,
        message: str,
        role_name: str | None = None,
        model_uid: str | None = None,
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
        url = f"{CHAT_ROUTE}/{self._strangerinfo.namespace_str}"
        data = self._prepare_request_body(
            message = message,
            role_name = role_name,
            model_uid = model_uid,
            load_prompt = load_prompt,
            enable_md_prompt = enable_md_prompt,
            reference_context_id = reference_context_id,
            stream = True,
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

                yield StreamChatChunkResponse(**json.loads(line))
    
    def _prepare_request_body(
        self,
        message: str,
        role_name: str | None = None,
        model_uid: str | None = None,
        load_prompt: bool = True,
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
        stream: bool = False,
    ):
        # 表单数据格式 (Form Data)
        data = {
            "user_info": {
                "username" : self._strangerinfo.nickname,
                "nickname" : self._strangerinfo.display_name,
                "age": self._strangerinfo.age,
                "gender": self._strangerinfo.gender,
            },
            "load_prompt": load_prompt,
        }
        if model_uid:
            data['model_uid'] = model_uid
        if role_name:
            data['role_name'] = role_name
        if reference_context_id:
            data['reference_context_id'] = reference_context_id
        if stream:
            data['stream'] = stream
        if message:
            MD_Rendering_Enables_Prompts = "\n> Markdown rendering is turned on!!"
            MD_Rendering_Enables_Prompts = MD_Rendering_Enables_Prompts if enable_md_prompt else ''
            Reference_Enables_Prompts = "\n> Guest mode(User: {user_name})，Citation context is turned on!!"
            Reference_Enables_Prompts = Reference_Enables_Prompts if reference_context_id else ''
            data['message'] = '> SystemInfo:\n> Message sending time:{time}' + (MD_Rendering_Enables_Prompts) + (Reference_Enables_Prompts) + '\n\n---\n\n' + message
        return data
    
    async def text_render(self, text: str) -> RendedImage:
        return await self._text_render.render(text)
    
    async def content_render(self, content: str, reasoning_content: str = "") -> RendedImage:
        text = ""
        if reasoning_content:
            text += ("> " + reasoning_content.replace('\n', '\n> ') + "\n\n---\n\n")
        text += content

        return await self.text_render(text)
    
    exit_register.register()
    async def close(self):
        await self._chat_client.aclose()
        await self._client.aclose()
    # endregion