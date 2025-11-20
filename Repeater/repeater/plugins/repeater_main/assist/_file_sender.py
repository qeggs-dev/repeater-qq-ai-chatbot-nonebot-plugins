from ._stranger_info import StrangerInfo, MessageSource

class FileSender:
    def __init__(self, stranger_info: StrangerInfo):
        self.stranger_info = stranger_info

    async def send_file(self, url: str, file_name: str):
        if self.stranger_info.source == MessageSource.GROUP:
            data = {
                "group_id": self.stranger_info._group_id,
                "file": url,
                "name": file_name,
                "folder_id": None
            }
            await self.stranger_info.bot.upload_group_file(**data)
        elif self.stranger_info.source == MessageSource.PRIVATE:
            data = {
                "user_id": self.stranger_info.user_id,
                "file": url,
                "name": file_name
            }
            await self.stranger_info.bot.upload_private_file(**data)
        