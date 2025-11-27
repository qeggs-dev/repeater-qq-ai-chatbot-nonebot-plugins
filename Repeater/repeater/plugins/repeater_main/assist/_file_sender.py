from ._persona_info import PersonaInfo, MessageSource

class FileSender:
    def __init__(self, persona_info: PersonaInfo):
        self.persona_info = persona_info

    async def send_file(self, url: str, file_name: str):
        if self.persona_info.source == MessageSource.GROUP:
            data = {
                "group_id": self.persona_info._group_id,
                "file": url,
                "name": file_name,
                "folder_id": None
            }
            await self.persona_info.bot.upload_group_file(**data)
        elif self.persona_info.source == MessageSource.PRIVATE:
            data = {
                "user_id": self.persona_info.user_id,
                "file": url,
                "name": file_name
            }
            await self.persona_info.bot.upload_private_file(**data)
        