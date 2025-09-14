from dataclasses import dataclass
from enum import Enum

class MessageSource(Enum):
    GROUP = "group"
    PRIVATE = "private"

@dataclass
class Namespace:
    mode: MessageSource = MessageSource.GROUP
    group_id: str | None = None
    user_id: str = ""

    @property
    def namespace(self) -> str:
        if self.mode == MessageSource.GROUP:
            if self.group_id is None:
                raise ValueError("group_id cannot be None when mode is GROUP")
            return f"Group:{self.group_id}:{self.user_id}"
        else:
            return f"Private:{self.user_id}"
    
    @property
    def public_space_id(self):
        if self.mode == MessageSource.GROUP:
            if self.group_id is None:
                raise ValueError("group_id cannot be None when mode is GROUP")
            return f"Group:{self.group_id}_Public_Space"
        else:
            return f"Private:{self.user_id}_Public_Space"
    
    def __str__(self) -> str:
        return self.namespace