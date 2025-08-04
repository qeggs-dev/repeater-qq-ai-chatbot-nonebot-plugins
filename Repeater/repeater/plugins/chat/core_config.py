# 服务端配置


# ==== CHAT API ==== #
CHAT_API = "http://localhost"
CHAT_PORT = 7645
CHAT_ROUTE = "chat/completion"
NPCHAT_ROUTE = "chat/completion/noprompt"

# ==== SESSION API ==== #
DOWNLOAD_SESSION_ROUTE = "session/download"
DELETE_CONTEXT_ROUTE = "userdata/context/delete"
GET_CONTEXT_LENGTH_ROUTE = "userdata/context/length"
INJECT_CONTEXT_ROUTE = "session/inject"
WIHTDRAW_CONTEXT_ROUTE = "session/withdraw"
CHANGE_CONTEXT_BRANCH_ROUTE = "userdata/context/change"
DELETE_SUBSESSION_ROUTE = "session/subsession/delete"
CLONE_SESSION_ROUTE = "session/clone"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = "userdata/prompt/set"
CHANGE_PROMPT_BRANCH_ROUTE = "userdata/prompt/change"
DELETE_PROMPT_ROUTE = "userdata/prompt/delete"
DELETE_SUBSESSION_PROMPT_ROUTE = "prompt/subsession/delete"
CLONE_PROMPT_ROUTE = "prompt/clone"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = "userdata/config/set"
CLONE_CONFIG_ROUTE = "config/clone"
CHANGE_CONFIG_BRANCH_ROUTE = "userdata/config/change"
DELETE_CONFIG_ROUTE = "userdata/config/delete"
DELETE_SUBSESSION_CONFIG_ROUTE = "config/subsession/delete"
SET_SUMT_ROUTE = "sumt/set"

# ==== Download User Data File ==== #

DOWNLOAD_USER_DATA_FILE_ROUTE = "userdata/file"

# ==== RENDER API ==== #
DOWNLOAD_RENDERED_IMAGE_ROUTE = "file/render"
TEXT_RENDER_ROUTE = "render"

# ==== ONLINE CHECK API ==== #
ONLINE_CHECK_ROUTE = "server/online"

# ==== README API ==== #
HTML_README_FILE_ROUTE = "readme.html"

# ==== Balance API ==== #
BALANCE_ROUTE = "balance_query"

# ==== VARIABLE EXPANSION API ==== #
VARIABLE_EXPANSION = "userdata/variable/expand"

# ==== CONFIG ==== #
MAX_LENGTH = 200
MAX_SINGLE_LINE_LENGTH = 10
MIN_RENDER_IMAGE_TEXT_LINE = 5
RepeaterDebugMode = False # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

