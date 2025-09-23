# 服务端配置

# ==== CHAT API ==== #
CHAT_API = "http://localhost"
CHAT_PORT = 7645
CHAT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/chat/completion"
NPCHAT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/chat/completion/noprompt"

# ==== CONTEXT API ==== #
DELETE_CONTEXT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/context/delete"
GET_CONTEXT_LENGTH_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/context/length"
INJECT_CONTEXT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/session/inject"
WIHTDRAW_CONTEXT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/context/withdraw"
CHANGE_CONTEXT_BRANCH_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/context/change"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/prompt/set"
CHANGE_PROMPT_BRANCH_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/prompt/change"
DELETE_PROMPT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/prompt/delete"
DELETE_SUBSESSION_PROMPT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/prompt/subsession/delete"
CLONE_PROMPT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/prompt/clone"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/config/set"
GET_CONFIG_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/config/get"
REMOVE_CONFIG_KEY_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/config/delkey"
CLONE_CONFIG_ROUTE = f"{CHAT_API}:{CHAT_PORT}/config/clone"
CHANGE_CONFIG_BRANCH_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/config/change"
DELETE_CONFIG_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/config/delete"
DELETE_SUBSESSION_CONFIG_ROUTE = f"{CHAT_API}:{CHAT_PORT}/config/subsession/delete"
SET_SUMT_ROUTE = f"{CHAT_API}:{CHAT_PORT}/sumt/set"

# ==== Download User Data File ==== #

DOWNLOAD_USER_DATA_FILE_ROUTE = f"{CHAT_API}:{CHAT_PORT}/userdata/file"

# ==== RENDER API ==== #
DOWNLOAD_RENDERED_IMAGE_ROUTE = f"{CHAT_API}:{CHAT_PORT}/file/render"
TEXT_RENDER_ROUTE = f"{CHAT_API}:{CHAT_PORT}/render"

# ==== ONLINE CHECK API ==== #
ONLINE_CHECK_ROUTE = f"{CHAT_API}:{CHAT_PORT}/server/online"

# ==== README API ==== #
README_FILE_ROUTE = f"{CHAT_API}:{CHAT_PORT}/readme.md"
HTML_README_FILE_ROUTE = f"{CHAT_API}:{CHAT_PORT}/readme.html"

# ==== Balance API ==== #
BALANCE_ROUTE = f"{CHAT_API}:{CHAT_PORT}/balance_query"

# ==== VARIABLE EXPANSION API ==== #
VARIABLE_EXPANSION = f"{CHAT_API}:{CHAT_PORT}/userdata/variable/expand"

# ==== CONFIG ==== #
MAX_LENGTH = 400
MAX_SINGLE_LINE_LENGTH = 64
MIN_RENDER_IMAGE_TEXT_LINE = 5
RepeaterDebugMode = False # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

