# AI工作规范与专项技能

先读通用规范，再按工作方向选专项。每项只有一个规范入口；用中文显示名直观选择，用标准英文名称稳定调用。

- 智能体先看[AGENTS.md](AGENTS.md)与[机器索引skills-index.json](skills-index.json)。
- 工作前通用入口：[personal-ai-work](SKILL.md)。
- 专项技能保持独立顶层目录；按类别展示，不增加会妨碍发现的多层文件夹。

## 图片、图标与Figma

| 中文名称 | 调用名 / 入口 | 适用方向 | 不负责 |
|---|---|---|---|
| 生图即修图规范 | [image-editing-standards](image-editing-standards/SKILL.md) | 位图生图、局部修复、真实组件、透视厚度、清晰度、保护区和前后对照 | 纯SVG重绘、页面布局 |
| Figma图标设计替换与验收 | [figma-icon-replacement-qa](figma-icon-replacement-qa/SKILL.md) | SVG候选、风格统一、局部替换、实际尺寸与素材打包 | 整页适配、照片修复 |
| Figma视觉设计与前端交付 | [figma-visual-handoff](figma-visual-handoff/SKILL.md) | 页面设计、PC转移动、可编辑文字、媒体Frame和前端交付 | 网站编码、位图精修 |
| 网页视觉走查与飞书记录 | [ui-visual-audit-feishu](ui-visual-audit-feishu/SKILL.md) | Figma对线上双端多语言、标注证据、飞书回读 | 直接修改线上页面或设计稿 |

图标规则已经集中在图标Skill；Figma交付只保留分层与适配衔接。生图修图规则集中在image-editing-standards，通用视觉参考只负责路由与品牌语境。

## 文档、演示与视频

| 中文名称 | 调用名 / 入口 | 适用方向 |
|---|---|---|
| GUI外观专利交底与成稿 | [gui-design-patent-cn](gui-design-patent-cn/SKILL.md) | 中国GUI外观设计、界面说明Word、变化状态图包 |
| 网页PPT与演讲配图 | [web-ppt-guizang](web-ppt-guizang/SKILL.md) | 单HTML横向演示、杂志风/瑞士风、配图与封面 |
| OpenFilm视频剪辑与制作 | [openfilm](openfilm/SKILL.md) | 视频、字幕、动态图形、预览与导出 |

网页PPT交付HTML，不等于原生PPTX。照片配图需要时组合生图规范；OpenFilm保留官方名称、原文和许可证。

## 通用、技能维护与应用分析

| 中文名称 | 调用名 / 入口 | 读取或启动条件 |
|---|---|---|
| 通用工作规范 | [personal-ai-work](SKILL.md) | 每个任务开始先完整读取 |
| 技能查找评估与安装 | [find-skills](find-skills/SKILL.md) | 需要发现或补充已有技能时 |
| REA应用与发布包分析（手动） | [rea](rea/SKILL.md) | 用户明确说“调用REA开始完成这个工作”或明确要求立即执行 |

REA保持手动调用，提及、引用或讨论接入不启动分析。find-skills和openfilm的来源及版本见[第三方技能说明](docs/external-skills.md)。

## 旧名迁移

| 原名称 / 目录 | 当前标准名称 | 说明 |
|---|---|---|
| UI走查-飞书 | ui-visual-audit-feishu | 统一为标准英文调用名，中文显示名说明网页走查与飞书记录 |
| guizang-ppt-skill | web-ppt-guizang | 用网页PPT用途作前缀，保留Guizang作者识别与上游归属 |
| codex-workflow-memory | personal-ai-work | 旧协作记忆已合入通用规范，本仓库不再保存重复入口 |
| 原视觉参考中的图片细则 | image-editing-standards | 其他入口按需引用，不各写一套生图修图规范 |
| Figma交付参考中的图标细则 | figma-icon-replacement-qa | 独特规则已合入图标专项，交付参考只保留衔接 |

aliases是检索和迁移线索，不代表同一客户端能自动调用未安装的旧名，也不创建第二份SKILL.md。

## 按需参考

[视觉路由](references/visual-guidelines.md)、[Figma桌面自动化](references/figma-desktop-automation.md)、[文档与表格](references/document-guidelines.md)、[提示词](references/prompt-guidelines.md)、[代码与项目](references/development-guidelines.md)、[技能维护](references/skill-maintenance.md)、[本机总结](references/local-reporting.md)。它们从属于通用规范；专项内references、scripts和assets从属于对应Skill。

## 安装与调用

- 通用规范：将根目录SKILL.md、references、docs、agents和skills-index.json一起安装到personal-ai-work目录，不复制全部兄弟技能。
- 专项：复制整个同名文件夹到客户端技能目录，例如~/.codex/skills/；目录内的资料和脚本一起保留。
- 不把整个仓库当成单个技能安装。目录分类用于查找，调用以客户端实际发现的Skill为准。
- 已装旧目录时先比较用户改动，再迁移到新名称，确认后只保留一个有效入口。本次仓库重命名不自动改动现有客户端安装。
- 自然语言示例：使用生图即修图规范；用Figma图标设计替换与验收；用网页视觉走查与飞书记录检查这个页面。
- 显式调用示例：$image-editing-standards、$ui-visual-audit-feishu、$web-ppt-guizang。

图像检查脚本依赖Python3与Pillow。网页走查原有依赖为lark-cli、Node.js、puppeteer-core、Chrome、Python与Pillow；认证信息只放本机环境。OpenFilm及其他工具按当前专项说明核对环境。

## 证据与隐私

公开同步只包含可复用规则、去标识案例及检查脚本。真实修改前后图片、完整聊天、任务ID和本机审计索引留在获授权的本机项目目录，不随仓库发布。生图规范的去标识案例说明问题与方法；每次实际任务仍需建立真实对照，不能用示例代替验收证据。
