# 服务端配置

# ==== CHAT API ==== #
CHAT_API = "http://localhost"
CHAT_PORT = 3198
CHAT_ROUTE = "chat/completion"
NPCHAT_ROUTE = "chat/completion/noprompt"

# ==== SESSION API ==== #
DOWNLOAD_SESSION_ROUTE = "session/download"
DELETE_CONTENT_ROUTE = "session/delete"
INJECT_CONTEXT_ROUTE = "session/inject"
WIHTDRAW_CONTEXT_ROUTE = "session/withdraw"
CHANGE_SUBSESSION_ROUTE = "session/subsession/change"
DELETE_SUBSESSION_ROUTE = "session/subsession/delete"
CLONE_SESSION_ROUTE = "session/clone"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = "prompt/set"
CHANGE_SUBSESSION_PROMPT_ROUTE = "prompt/subsession/change"
DELETE_PROMPT_ROUTE = "prompt/delete"
DELETE_SUBSESSION_PROMPT_ROUTE = "prompt/subsession/delete"
CLONE_PROMPT_ROUTE = "prompt/clone"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = "config/set"
CLONE_CONFIG_ROUTE = "config/clone"
CHANGE_SUBSESSION_CONFIG_ROUTE = "config/subsession/change"
DELETE_CONFIG_ROUTE = "config/delete"
DELETE_SUBSESSION_CONFIG_ROUTE = "config/subsession/delete"
SET_SUMT_ROUTE = "sumt/set"

# ==== NOTE API ==== #
SET_NOTE_ROUTE = "note/set"
CLONE_NOTE_ROUTE = "note/clone"
DELETE_SESSION_NOTE_ROUTE = "note/delete"
CHANGE_SUBSESSION_NOTE_ROUTE = "note/subsession/change"
DELETE_SUBSESSION_NOTE_ROUTE = "note/subsession/delete"

# ==== RENDER API ==== #
DOWNLOAD_RENDERED_IMAGE_ROUTE = "renders"

# ==== ONLINE CHECK API ==== #
ONLINE_CHECK_ROUTE = "server/online"

# ==== README API ==== #
HTML_README_FILE_ROUTE = "readme.html"

# ==== Balance API ==== #
BALANCE_ROUTE = "balance_query"

# ==== CONFIG ==== #
MAX_LENGTH = 1000
RepeaterDebugMode = False # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作