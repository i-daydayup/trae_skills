# trae_skills
基于TRAE的skills应用。

Skills把数据分为三层：
- 元数据（Matedata）：类比一本书的目录
- 指令（Instruction）：类比书本的正文
- 资源（Resource）：类比书本的附录

SKILL.md存放元数据和指令，文件夹的其他部分存放资源。在AI使用Skills的时候，先把元数据加载进入提示词，然后根据需要再决定是否查阅指令或资源，这样相比传统Prompt或者MCP方式，大幅度降低了TOKEN的消耗以及提示词的复杂度。

在TRAE，右上角“设置”，找到“规则和技能”，在“技能”中点击“创建”，将包含SKILL.md的zip文件上传（压缩包里的SKILL.md可以在一个子目录下）。
- 其中`---`包括起来的部分是元数据，会固定加载到AI提示词中。


# 参考链接
- Anthropic官方的skills仓库 https://github.com/anthropics/skills
- Anthropic官方另一个仓库 https://github.com/anthropics/claude-cookbooks
    - 分析金融报表的skill https://github.com/anthropics/claude-cookbooks/tree/main/skills/custom_skills/analyzing-financial-statements

