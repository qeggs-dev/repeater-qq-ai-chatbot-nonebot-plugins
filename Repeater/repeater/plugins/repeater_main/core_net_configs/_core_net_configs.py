# 服务端配置
from ._net_config import net_config
from ._storage_configs import storage_config

# ==== CHAT API ==== #
BACKEND_HOST = net_config.backend_host
BACKEND_PORT = net_config.backend_port
CHAT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/chat/completion"
NPCHAT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/chat/completion/noprompt"

# ==== CONTEXT API ==== #
DELETE_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/delete"
GET_CONTEXT_LENGTH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/length"
INJECT_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/session/inject"
WIHTDRAW_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/withdraw"
CHANGE_CONTEXT_BRANCH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/change"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/prompt/set"
CHANGE_PROMPT_BRANCH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/prompt/change"
DELETE_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/prompt/delete"
DELETE_SUBSESSION_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/prompt/subsession/delete"
CLONE_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/prompt/clone"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/set"
GET_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/get"
REMOVE_CONFIG_KEY_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/delkey"
CLONE_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/config/clone"
CHANGE_CONFIG_BRANCH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/change"
DELETE_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/delete"
DELETE_SUBSESSION_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/config/subsession/delete"
SET_SUMT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/sumt/set"

# ==== Download User Data File ==== #

DOWNLOAD_USER_DATA_FILE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/file"

# ==== RENDER API ==== #
DOWNLOAD_RENDERED_IMAGE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/file/render"
TEXT_RENDER_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/render"

# ==== ONLINE CHECK API ==== #
ONLINE_CHECK_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/server/online"

# ==== README API ==== #
README_FILE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/readme.md"
HTML_README_FILE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/readme.html"

# ==== Balance API ==== #
BALANCE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/balance_query"

# ==== VARIABLE EXPANSION API ==== #
VARIABLE_EXPANSION = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/variable/expand"

# ==== CONFIG ==== #
HELLO_CONTENT = storage_config.hello_content
MAX_LENGTH = storage_config.max_text_length
MIN_RENDER_SINGLE_LINE_LENGTH = storage_config.max_single_line_length
MIN_RENDER_IMAGE_TEXT_LINES = storage_config.max_text_lines
RepeaterDebugMode = net_config.repeater_debug_mode # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

