# @复读机Repeater
**- Only Chat, Focus Chat. -**

*注：本仓库仅为NoneBot插件，需要配合[后端项目](#相关仓库)使用*

一个基于[`NoneBot`](https://nonebot.dev/)和[`OpenAI SDK`](https://pypi.org/project/openai/)开发的**实验性**QQ聊天机器人
**此仓库仅为后端实现，NoneBot插件部分请查看[`Repater-Nonebot-Plugin`](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)**
将原始会话数据的处理直接公开给用户使用
接近直接操作API的灵活度体验

与其他QQ机器人相比，复读机具有以下特点：

 - 平行数据管理：支持平行数据管理，用户可以随意切换平行数据，而不需要担心数据丢失。
 - 多模型支持：支持OpenAI接口的模型即可调用，可以根据需要选择不同的模型进行对话。
 - 超高自由度：用户可以自定义会话注入、切换、删除，以及自定义提示词
 - MD图片渲染：可以将回复以图片的形式渲染发送，降低其妨碍用户正常聊天的程度（但鬼知道为什么这东西竟然不支持Emoji渲染！！！）
 - 命令别名触发：不管是缩写还是全文，都可以触发命令操作
 - 用户自治设计：用户可以自己管理自己的所有用户数据
 - 多预设人设：复读机支持多预设人设，用户可以自由选择自己喜欢的人设进行对话
> 注：拟人化并非复读机的赛道，复读机不对拟人化需求做过多保证，如有需要请自行引导或编写提示词。

## 注意事项:
 - 本服务由一位 `16岁自学开发者`(现在17了) 使用AI协作开发，公益项目，如果你愿意捐赠，可以在机器人的**QQ空间**中找到赞赏码以支持项目运营(或是支持开发者)。
 - 初始服务仅作为实验项目运行，不保证服务稳定性（存在维修断电以及临时消息丢失的可能，但这与项目本身无关，~~只是我不懂运维罢了~~），有需要可自行部署。
 - 项目随时可能会因为开发者个人原因，或API额度耗尽等因素而被迫中止。
 - 使用者需确认生成内容的合法性，并自行承担使用本服务可能产生的风险。
 - 如果你觉得这个Bot非常好用，请去看一下[`Deepseek`](https://www.deepseek.com/)的官网吧，这个Bot最初就是基于他们的模型API开发的。

---

## Length Score
长度评分系统，用于判断回复是否过长，过长则自动发送图片
长度评分系统由`main_api.json/text_length_score_config`定义，其包含以下参数：
 - `lines`：回复的最大行数
 - `single_line_max`：单行的最大长度
 - `mean_line_max`：平均行的最大长度
 - `total_length`：总长度
 - `threshold`：长度评分阈值，包含`group`和`private`两个参数，分别表示群聊和私聊的阈值

长度评分系统通过以下公式计算：
```python
length_score = (
    len(text) / lines +
    (
        max(len(line) for line in text.splitlines()) / single_line_max +
        sum(len(line) for line in text.splitlines()) / len(text.splitlines()) / mean_line_max
    ) / 2 +
    len(text) / total_length
) / 3
```
如果长度评分超过阈值，则会向后端请求将文本渲染为图片，以保证不会影响其他用户正常聊天。

---

## ENV配置

| Name                         | Default                                                                  | Description |
|------------------------------|--------------------------------------------------------------------------|-------------|
| REPEATER_LOGGER_LEVEL        | "INFO"                                                                   | 日志等级，可选值：`TRACE`, `DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` |
| REPEATER_LOGGER_FORMAT       | "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[module]} - {message}" | 到文件的日志格式，与控制台无关 |
| REPEATER_LOGGER_PATH         | "logs/repeater-log-{time:YYYY-MM-DD-HH-mm-ss}.log"                       | 日志文件的路径 |
| REPEATER_LOGGER_ENABLE_QUEUE | true                                                                     | 是否启用队列模式 |
| REPEATER_LOGGER_DELAY        | true                                                                     | 是否在第一条日志输出时才创建日志文件 |
| REPEATER_LOGGER_ROTATION     | "100 MB"                                                                 | 日志文件的轮换条件，可填时长、大小等数据 |
| REPEATER_LOGGER_RETENTION    | "1 month"                                                                | 日志文件的保留条件，可填时长、大小等数据 |
| REPEATER_LOGGER_COMPRESSION  | "zip"                                                                    | 日志文件的处理方式 |
| STORAGE_BASE_PATH            | "./storage"                                                              | 存储文件的基础路径 |
| ENVIRONMENT                  | "dev"                                                                    | 该值的内容将决定了程序会进一步读取哪个环境变量文件，如`prod`就是读取`.env.prod`，`dev`就是读取`.env.dev` |
| HOST                         | "0.0.0.0"                                                                | 主机地址 |
| PORT                         | 8080                                                                     | 端口号 |
| COMMAND_START                | ["/"]                                                                    | 用于触发命令的开始字符 |
| COMMAND_SEP                  | ["."]                                                                    | 用于触发命令的分隔符 |
| ONEBOT_ACCESS_TOKEN          | ""                                                                       | OneBot的访问令牌 |
| SUPERUSERS                   | [""]                                                                     | 超级用户列表 |

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

## 依赖
| Name       | Version | License      | License Text Link                                                    | Where it is used              |
|------------|---------|--------------|----------------------------------------------------------------------|-------------------------------|
| httpx      | 0.28.1  | BSD License  | [BSD-3-Clause](https://opensource.org/license/bsd-3-clause/)         | *Entire Project*              |
| nonebot    | 2.4.3   | MIT License  | [MIT](https://github.com/nonebot/nonebot2/blob/master/LICENSE)       | *Entire Project*              |
| pydantic   | 2.12.0  | MIT License  | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)        | *Entire Project*              |
| aiofiles   | 25.1.0  | MIT License  | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)   | `storage`                     |
| pyyaml     | 6.0.3   | MIT License  | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)              | `storage`                     |
| orjson     | 3.11.3  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `storage` |
| numpy      | 2.3.4   | BSD License  | [BSD-3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt) | `command._clients._chat_core` |
| loguru     | 0.7.3   | MIT License  | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)          | *Entire Project*              |


---

## 配置
在目录下执行 `setup.bat` 或 `bash setup.sh`
###### 使用脚手架(nb-cli)创建项目环境
> 1. 选择simple模板
> 2. 给项目起个名字（比如`Repeater`）
> 3. 建议使用FastAPI驱动器
> 4. **至少必须选择OneBot V11适配器**
> 5. 输入Yes安装默认依赖
> 6. 输入Yes安装虚拟环境
> 7. 如果需要，可以选择内置插件，如echo
> 8. 在项目目录下，找到`.env`文件
> 9. 填写 `PORT`(数字), `ONEBOT_ACCESS_TOKEN`(字符串) 等字段配置项
> 10. 将复读机的NoneBot插件放入项目目录下（通常是`plugins`文件夹下）
执行`{项目名称}/.venv/pip install httpx`安装唯一依赖（此处这个大括号要去掉）
运行`run.bat`或`bash run.sh`启动程序`

---

## 连接

### 连接OneBot
1. 找到项目目录下的`.env`文件
2. 填写PORT(数字), ONEBOT_ACCESS_TOKEN(字符串) 等字段配置项
3. 执行`run.bat`或`bash run.sh`启动程序
4. 打开OneBot客户端，选择反向WebSocket(部分客户端上称为`WebSocket 客户端`)
5. 填写 `ws_url`(字符串，通常是`ws://127.0.0.1:PORT`，其中`PORT`是你在`.env`文件中填写的端口号)，`token`(字符串，需要与上面的`ONEBOT_ACCESS_TOKEN`一致)
6. 看到NoneBot日志输出中出现`connection open`时, 表示连接成功

### 链接后端
1. 找到项目目录下的`.env`文件
2. 填写`BACKEND_HOST`和`BACKEND_PORT`字段配置项 (其中HOST是后端服务主机的IP地址，PORT是后端服务主端口号，需要你和后端配置中编写的一致)
3. 执行`run.bat`或`bash run.sh`启动程序

PS: 由于OneBot客户端通常为入站服务，所以默认情况下所有服务都不需要配置公网IP访问
但你需要保证后端可以连接到你设定的API端口，OneBot客户端可以连接到指定社交平台的服务器

---

## Markdown图片渲染样式

| 风格 | 译名 |
| --- | :---: |
| **`light`** | 亮色 |
| `dark` | 暗色 |
| `red` | 红色 |
| `pink` | 粉色 |
| `blue` | 蓝色 |
| `green` | 绿色 |
| `purple` | 紫色 |
| `yellow` | 黄色 |
| `orange` | 橙色 |
| `dark-red` | 暗红色 |
| `dark-pink` | 暗粉色 |
| `dark-blue` | 暗蓝色 |
| `dark-green` | 暗绿色 |
| `dark-purple` | 暗紫色 |
| `dark-yellow` | 暗黄色 |
| `dark-orange` | 暗橙色 |

---

## 命令表

| Command                    | Abridge | Full Name                 | Type        | Joined Version | Description                   | Parameter Description                     | Remarks |
| :---                       | :---    | :---                      | :---:       | :---:          | :---:                         | :---:                                     | :---:   |
| `chat`                     | `c`     | `Chat`                    | `CHAT`      | 4.0 Beta       | 与机器人对话                   | 自然语言输入                               | 默认命令，可被`to_me`消息调起 |
| `keepAnswering`            | `ka`    | `KeepAnswering`           | `CHAT`      | 4.0 Beta       | 持续对话(常规)                 | 无                                        | 无须输入，AI再次回复 |
| `keepReasoning`            | `kr`    | `KeepReasoning`           | `CHAT`      | 4.0 Beta       | 持续对话(推理)                 | 无                                        | 无须输入，AI再次使用推理回复 |
| `renderChat`               | `rc`    | `RenderChat`              | `CHAT`      | 4.0 Beta       | 渲染Markdown回复               | 自然语言输入                               | 强制渲染图片输出 |
| `setRenderStyle`           | `srs`   | `SetRenderStyle`          | `CONFIG`    | 4.0 Beta       | 设置渲染样式                   | [渲染样式](#Markdown图片渲染样式)           | 设置Markdown图片渲染样式 |
| `npChat`                   | `np`    | `NoPromptChat`            | `CHAT`      | 4.0 Beta       | 不加载提示词进行对话            | 自然语言输入                               | 使用常规模型 |
| `reason`                   | `r`     | `Reason`                  | `CHAT`      | 4.0 Beta       | 使用Reasoner模型进行推理        | 自然语言输入                               | 调用模型由`reason_model_uid`字段控制，默认`deepseek-reasoner` |
| `recomplete`               | `rcm`   | `Recomplete`              | `CHAT`      | 4.0 Beta       | 重新进行对话补全                | 无                                        | 重新生成 |
| `setFrequencyPenalty`      | `sfp`   | `SetFrequencyPenalty`     | `CONFIG`    | 4.0 Beta       | 设置频率惩罚                   | `-2`\~`2`的浮点数 或`-200%`\~`200%`的百分比 | 控制着模型输出重复相同内容的可能性 |
| `setPresencePenalty`       | `spp`   | `SetPresencePenalty`      | `CONFIG`    | 4.0 Beta       | 设置存在惩罚                   | `-2`\~`2`的浮点数 或`-200%`\~`200%`的百分比 | 控制着模型谈论新主题的可能性 |
| `setTemperature`           | `st`    | `SetTemperature`          | `CONFIG`    | 4.0 Beta       | 设置温度                       | `0`\~`2`的浮点数 或`0%`\~`200%`的百分比  | 控制着模型生成内容的不确定性 |
| `setPrompt`                | `sp`    | `SetPrompt`               | `PROMPT`    | 4.0 Beta       | 设置提示词                     | 自然语言输入                               | 设置提示词 |
| `changeDefaultPersonality` | `cdp`   | `ChangeDefaultPersonality`| `CONFIG`    | 4.0 Beta       | 修改默认人格                   | [人格预设](#人格预设)                       | 修改默认人格路由 |
| `deletePrompt`             | `dp`    | `DeletePrompt`            | `PROMPT`    | 4.0 Beta       | 删除提示词                     | 无                                        | 删除提示词 |
| `deleteContext`            | `dc`    | `DeleteContext`           | `CONTEXT`   | 4.0 Beta       | 删除上下文                     | 无                                        | 删除上下文 |
| `varExpand`                | `ve`    | `VarExpand`               | `VAREXPAND` | 4.0 Beta       | 变量展开                       | 文本模板(使用大括号作为[变量](#变量表)标记)  | 变量展开 |
| `setDefaultModel`          | `sdm`   | `SetDefaultModel`         | `CONFIG`    | 4.0 Beta       | 设置默认模型                   | [模型](#模型)                              | 设置默认使用的模型 |
| `setTopP`                  | `stp`   | `SetTopP`                 | `CONFIG`    | 4.0.1 Beta     | 设置Top_P参数                  | 0\~1的浮点数 或`0%`\~`100%`的百分比         | 设置Top_P参数 |
| `setMaxTokens`             | `stm`   | `SetMaxTokens`            | `CONFIG`    | 4.0.1 Beta     | 设置最大生成tokens数           | 0\~4096的整数                              | 设置最大生成tokens数 |
| `getContextTotalLength`    | `gctl`  | `GetContextTotalLength`   | `CONTEXT`   | 4.0.1 Beta     | 获取上下文总长度               | 无                                         | 获取上下文总长度 |
| `publicSpaceChat`          | `psc`   | `PublicSpaceChat`         | `CHAT`      | 4.0.2.1 Beta   | 公共空间聊天                   | 自然语言输入                                | 公共空间聊天 |
| `deletePublicSpaceContext` | `dpsc`  | `DeletePublicSpaceContext`| `CONTEXT`   | 4.0.2.1 Beta   | 删除公共空间上下文             | 无                                         | 删除公共空间上下文 | 
| `sendUserDataFile`         | `sudf`  | `SendUserDataFile`        | `USERFILE`  | 4.0.2.1 Beta   | 发送用户数据文件               | 无                                         | 发送用户数据文件 |
| `changeContextBranch`      | `ccb`   | `ChangeContextBranch`     | `CONTEXT`   | 4.1.2.0        | 切换上下文分支                 | 分支名称                                   | 切换上下文分支 |
| `changePromptBranch`       | `cppb`  | `ChangePromptBranch`      | `PROMPT`    | 4.1.2.0        | 切换提示词分支                 | 分支名称                                   | 切换提示词分支 |
| `changeConfigBranch`       | `ccfgb` | `ChangeConfigBranch`      | `CONFIG`    | 4.1.2.0        | 切换配置分支                   | 分支名称                                   | 切换配置分支 |
| `reference`                | `ref`   | `Reference`               | `CHAT`      | 4.1.2.0        | 引用上下文                     | 用户ID                                    | 引用其他用户的上下文并追加到当前上下文 |
| `chooseGroupMember`        | `cgm`   | `ChooseGroupMember`       | `OTHER`     | 4.1.2.0        | 抽取群组成员                   | 抽取数量                                   | 抽取群组成员 |
| `withdraw`                 | `w`     | `Withdraw`                | `CONTEXT`   | 4.2.3.0        | 撤回消息                       | 无                                        | 删除复读机上下文中保存的最新一回合对话 |
| `recentSpeakingRanking`    | `rsr`   | `RecentSpeakingRanking`   | `OTHER`     | 4.2.3.0        | 最近发言排行                   | 无                                        | 获取群组内最近发言的成员列表 |
| `setAutoShrinkLength`      | `sasl`  | `SetAutoShrinkLength`     | `CONFIG`    | 4.2.4.0        | 设置自动缩减长度上限            | 整数                                      | 如果你的聊天条数超过该值，系统会尝试自动删除最旧的部分 ||
| `deleteSession`            | `ds`    | `DeleteSession`           | `MIXED`     | 4.2.5.0        | 删除所有用户数据               | 无                                        | 删除所有用户数据 |
| `raw`                      | `raw`   | `Raw`                     | `CHAT`      | 4.2.5.1        | 发送消息且不包含任何元数据      | 自然语言输入                               | 发送消息且不包含任何元数据 |
| `changeSession`            | `cs`    | `ChangeSession`           | `MIXED`     | 4.2.5.1        | 让所有的数据同时切换到一个分支   | 分支名称                                  | 让`Context`、`Prompt`、`Config`同时切换到一个分支 |

## 相关仓库
- [Repeater Backend](https://github.com/qeggs-dev/repeater-ai-chatbot-backend)