# trae_skills
基于TRAE的skills应用。

Skills把数据分为三层：
- 元数据（Matedata）：类比一本书的目录
- 指令（Instruction）：类比书本的正文
- 资源（Resource）：类比书本的附录

SKILL.md存放元数据和指令，文件夹的其他部分存放资源。在AI使用Skills的时候，先把元数据加载进入提示词，然后根据需要再决定是否查阅指令或资源，这样相比传统Prompt或者MCP方式，大幅度降低了TOKEN的消耗以及提示词的复杂度。

在TRAE，右上角“设置”，找到“规则和技能”，在“技能”中点击“创建”，将包含SKILL.md的zip文件上传（压缩包里的SKILL.md可以在一个子目录下）。
- 其中`---`包括起来的部分是元数据，会固定加载到AI提示词中。
- SKILL.md其他部分按需加载。

# 财报分析案例
- 给TRAE的提示词（跟SOLO Coder对话）：分析该财报：https://www.sec.gov/Archives/edgar/data/1326801/000162828025047240/meta-20250930.htm 用中文输出分析结果

# 讲故事
- 把前面分析的“Meta Platforms 2025年Q3财报分析”的数字结果转换成吸引人的故事线

# 哪些适合封装为Skills
- 反复粘贴的提示词
- 固定多步骤工作流

## 爬爬虾获取github内容的案例
SOLO Coder对话框，提示词如下：

---
创建一个Skill，功能如下：
第一步，爬取今日热门项目前5个 https://github.com/trending 
第二步，获取他们的README文件，
第三步，把前5个项目，总结成一个中文简介摘要，需要包含：项目是什么？解决什么问题？技术栈是什么？Star数量多少等主要内容
第四步，调用python脚本，发送总结的中文摘要邮件到我的邮箱

这个Skill应包含两个Python脚本：
脚本1：爬trending，获取前五5项目的README，把结果保存到一个json文件
脚本2：发送总结邮件 

发送邮箱的核心代码可以参考一下代码，邮件相关变量可以先留空，我后续自行补充
---

注：运行上述提示词之后，得到文件夹github-trending-email，发送邮件存在问题，暂时不可用。

## 个性化网页案例
- 技能地址：https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
    - 按说明进行安装，用CLI模式，在项目目录下，输入命令为：
        - npm install -g uipro-cli
        - uipro init --ai trae



# 参考链接
- Anthropic官方的skills仓库 https://github.com/anthropics/skills
- Anthropic官方另一个仓库 https://github.com/anthropics/claude-cookbooks
    - 分析金融报表的skill https://github.com/anthropics/claude-cookbooks/tree/main/skills/custom_skills/analyzing-financial-statements
- https://github.com/wshobson/agents/tree/main/plugins/business-analytics/skills/data-storytelling ，把原始数据转换为引人入胜的故事。
