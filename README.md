# @复读机Repeater
**- Only Chat, Focus Chat. -**

*注：本仓库仅为NoneBot插件，需要配合[后端项目](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-backend)使用*

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
 - 本服务由一位 `16岁自学开发者` 使用AI协作开发，公益项目，如果你愿意捐赠，可以在机器人的**QQ空间**中找到赞赏码以支持项目运营(或是支持开发者)。
 - 初始服务仅作为实验项目运行，不保证服务稳定性（存在维修断电以及临时消息丢失的可能，但这与项目本身无关，~~只是我不懂运维罢了~~），有需要可自行部署。
 - 项目随时可能会因为开发者个人原因，或API额度耗尽等因素而被迫中止。
 - 仅供学习和非商业用途。使用者需确认生成内容的合法性，并自行承担使用本服务可能产生的风险。
 - 如果你觉得这个Bot非常好用，请去看一下[`Deepseek`](https://www.deepseek.com/)的官网吧，这个Bot最初就是基于他们的模型API开发的。

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

## 依赖
| Name       | Version   | License      | License Text Link                                              | Where it is used |
|------------|-----------|--------------|----------------------------------------------------------------|------------------|
| httpx      | 0.28.1    | BSD License  | [BSD-3-Clause](https://opensource.org/license/bsd-3-clause/)   | `chat` Plugins   |
| nonebot    | 2.4.2     | MIT License  | [MIT](https://github.com/nonebot/nonebot2/blob/master/LICENSE) | *Entire Project* |

---

## 配置
> 在目录下执行 `setup.bat` 或 `bash setup.sh`
> ###### 使用脚手架(nb-cli)创建项目环境
> > 1. 选择simple模板
> > 2. 给项目起个名字（比如`Repeater`）
> > 3. 建议使用FastAPI驱动器
> > 4. **至少必须选择OneBot V11适配器**
> > 5. 输入Yes安装默认依赖
> > 6. 输入Yes安装虚拟环境
> > 7. 如果需要，可以选择内置插件，如echo
> > 8. 在项目目录下，找到`.env`文件
> > 9. 填写 `PORT`(数字), `ONEBOT_ACCESS_TOKEN`(字符串) 等字段配置项
> > 10. 将复读机的NoneBot插件放入项目目录下（通常是`plugins`文件夹下）
> 执行`{项目名称}/.venv/pip install httpx`安装唯一依赖（此处这个大括号要去掉）
> 运行`run.bat`或`bash run.sh`启动程序`

---

## Markdown图片渲染样式

| 风格 | 译名 |
| :---: | :---: |
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

## 模型

| 模型 | 描述 |
| :---: | :---: |
| `deepseek-chat` | 聊天 |
| `deepseek-reasoner` | 推理 |
| `deekpseek-coder` | 编码 |
| `deepseek-r1` | DeepSeek R1模型 |
| `deepseek-v3` | DeepSeek V3模型 |
| `kimi-k2` | Kimi K2模型 |

PS: 使用`sdm`命令带着模型ID设置你需要的模型。

---

## 命令表

| 命令                       | 别名    | 全名                      | 类型        | 功能描述                       | 参数描述                                   | 加入版本 | 命令版本          | 备注 |
| :---                       | :---   | :---                      | :---:       | :---:                         | :---:                                     | :---:    | :---:            | :---: |
| `chat`                     | `c`    | `Chat`                    | `CHAT`      | 与机器人对话                   | 自然语言输入                               | 4.0 Beta | 1.0              | 默认命令，可被`to_me`消息调起 |
| `keepAnswering`            | `ka`   | `KeepAnswering`           | `CHAT`      | 持续对话(常规)                 | 无                                        | 4.0 Beta | 1.0              | 无须输入，AI再次回复 |
| `keepReasoning`            | `kr`   | `KeepReasoning`           | `CHAT`      | 持续对话(推理)                 | 无                                        | 4.0 Beta | 1.0              | 无须输入，AI再次使用推理回复 |
| `renderChat`               | `rc`   | `RenderChat`              | `CHAT`      | 渲染Markdown回复               | 自然语言输入                               | 4.0 Beta | 1.0              | 强制渲染图片输出 |
| `setRenderStyle`           | `srs`  | `SetRenderStyle`          | `RENDER`    | 设置渲染样式                   | [渲染样式](#Markdown图片渲染样式)           | 4.0 Beta | 1.0              | 设置Markdown图片渲染样式 |
| `npChat`                   | `np`   | `NoPromptChat`            | `CHAT`      | 不加载提示词进行对话            | 自然语言输入                               | 4.0 Beta | 1.0              | 使用常规模型 |
| ~~`prover`~~               | ~~`p`~~| ~~`Prover`~~              | `CHAT`      | 使用Prover模型进行数学形式化证明 | 自然语言输入                               | 4.0 Beta | ~~1.0~~(已弃用)  | 使用`Prover`模型(已弃用) |
| `reason`                   | `r`    | `Reason`                  | `CHAT`      | 使用Reasoner模型进行推理        | 自然语言输入                               | 4.0 Beta | 1.0             | 使用`Reasoner`模型 |
| `recomplete`               | `rcm`  | `Recomplete`              | `CHAT`      | 重新进行对话补全                | 无                                        | 4.0 Beta | 1.0             | 重新生成 |
| `setFrequencyPenalty`      | `sfp`  | `SetFrequencyPenalty`     | `CONFIG`    | 设置频率惩罚                   | `-2`\~`2`的浮点数 或`-200%`\~`200%`的百分比 | 4.0 Beta | 1.0             | 控制着模型输出重复相同内容的可能性 |
| `setPresencePenalty`       | `spp`  | `SetPresencePenalty`      | `CONFIG`    | 设置存在惩罚                   | `-2`\~`2`的浮点数 或`-200%`\~`200%`的百分比 | 4.0 Beta | 1.0             | 控制着模型谈论新主题的可能性 |
| `setTemperature`           | `st`   | `SetTemperature`          | `CONFIG`    | 设置温度                       | `0`\~`2`的浮点数 或`-100%`\~`100%`的百分比 | 4.0 Beta | 1.0             | 控制着模型生成内容的不确定性 |
| `setPrompt`                | `sp`   | `SetPrompt`               | `PROMPT`    | 设置提示词                     | 自然语言输入                               | 4.0 Beta | 1.0             | 设置提示词 |
| `changeDefaultPersonality` | `cdp`  | `ChangeDefaultPersonality`| `CONFIG`    | 修改默认人格                   | [人格预设](#人格预设)                       | 4.0 Beta | 1.0             | 修改默认人格路由 |
| `deletePrompt`             | `dp`   | `DeletePrompt`            | `PROMPT`    | 删除提示词                     | 无                                        | 4.0 Beta | 1.0             | 删除提示词 |
| `deleteContext`            | `dc`   | `DeleteContext`           | `CONTEXT`   | 删除上下文                     | 无                                        | 4.0 Beta | 1.0             | 删除上下文 |
| `deleteSession`            | `ds`   | `DeleteSession`           | `CONTEXT`   | 删除上下文(兼容的旧版命令)      | 无                                        | 4.0 Beta | 1.0             | 删除上下文(兼容旧版命令，与上条命令功能一致) |
| `varExpand`                | `ve`   | `VarExpand`               | `VAREXPAND` | 变量展开                       | 文本模板(使用大括号作为[变量](#变量表)标记)  | 4.0 Beta | 1.0             | 变量展开 |
| `setDefaultModel`          | `sdm`  | `SetDefaultModel`         | `CONFIG`    | 设置默认模型                   | [模型](#模型)                              | 4.0 Beta | 1.0             | 设置默认使用的模型 |
| `setTopP`                  | `stp`  | `SetTopP`                 | `CONFIG`    | 设置Top_P参数                  | 0\~1的浮点数 或`0%`\~`100%`的百分比         | 4.0.1 Beta | 1.0           | 设置Top_P参数 |
| `setMaxTokens`             | `stm`  | `SetMaxTokens`            | `CONFIG`    | 设置最大生成tokens数           | 0\~4096的整数                               | 4.0.1 Beta | 1.0           | 设置最大生成tokens数 |
| `getContextTotalLength`    | `gctl` | `GetContextTotalLength`   | `CONTEXT`   | 获取上下文总长度               | 无                                         | 4.0.1 Beta | 1.0           | 获取上下文总长度 |
| `publicSpaceChat`          | `psc`  | `PublicSpaceChat`         | `CHAT`      | 公共空间聊天                   | 自然语言输入                                | 4.0.2.1 Beta | 1.0         | 公共空间聊天 |
| `deletePublicSpaceContext` | `dpsc` | `DeletePublicSpaceContext`| `CONTEXT`   | 删除公共空间上下文             | 无                                         | 4.0.2.1 Beta | 1.0         | 删除公共空间上下文 | 
| `sendUserDataFile`         | `sudf` | `SendUserDataFile`        | `USERFILE`  | 发送用户数据文件               | 无                                         | 4.0.2.1 Beta | 1.0         | 发送用户数据文件 |
| `changeContextBranch`      | `ccb`  | `ChangeContextBranch`     | `CONTEXT`   | 切换上下文分支                 | 分支名称                                    | 4.1.2.0      | 1.0         | 切换上下文分支 |
| `changePromptBranch`       | `cppb` | `ChangePromptBranch`      | `PROMPT`    | 切换提示词分支                 | 分支名称                                    | 4.1.2.0      | 1.0         | 切换提示词分支 |
| `changeConfigBranch`       | `ccfgb`| `ChangeConfigBranch`      | `CONFIG`    | 切换配置分支                   | 分支名称                                    | 4.1.2.0      | 1.0         | 切换配置分支 |
| `reference`                | `ref`  | `Reference`               | `CHAT`      | 引用上下文                     | 用户ID                                     | 4.1.2.0      | 1.0         | 引用其他用户的上下文并追加到当前上下文 |
| `chooseGroupMember`        | `cgm`  | `ChooseGroupMember`       | `OTHER`     | 抽取群组成员                   | 抽取数量                                    | 4.1.2.0      | 1.0         | 抽取群组成员 |