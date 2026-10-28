# 我的 AI 工作规范与专项技能

先读通用规范，再按任务调用技能。仓库按“读取时机”和“工作类型”分组；保留现有技能目录和调用路径。

## 一、工作前必须读：通用规范

| 文件 | 作用 | 读取时机 |
|---|---|---|
| [AGENTS.md](AGENTS.md) | 仓库工作入口，说明必读顺序和分类 | 在本仓库工作时首先遵循 |
| [SKILL.md](SKILL.md) · `personal-ai-work` | 长期偏好、中文沟通、修改边界、版本保护、自查交付、历史文件复用 | 每个新窗口、每个新任务，实质性操作前完整读取 |

根目录 `SKILL.md` 是唯一主规范。专项技能和补充规范按下面的触发条件读取。

## 二、按任务读取：专项技能

| 分组 | 技能入口 | 什么时候用 |
|---|---|---|
| Figma 视觉交付 | [figma-visual-handoff](figma-visual-handoff/SKILL.md) | 移动适配、图片与文字分层、可编辑图层和前端素材交付 |
| Figma 图标 | [figma-icon-replacement-qa](figma-icon-replacement-qa/SKILL.md) | 图标候选、替换、统一风格与实际尺寸验收 |
| UI 走查与飞书 | [UI走查-飞书](UI走查-飞书/SKILL.md) | Figma 对照线上页面、标注差异、写入飞书走查表并回读 |
| GUI 专利与文档 | [gui-design-patent-cn](gui-design-patent-cn/SKILL.md) | 中国 GUI 外观设计专利、界面说明 Word、配套状态图 |
| 网页 PPT | [guizang-ppt-skill](guizang-ppt-skill/SKILL.md) | 横向翻页网页演示、杂志风或瑞士风 PPT |
| 视频剪辑与制作 | [openfilm](openfilm/SKILL.md) | 剪视频、字幕、动态图形、预览检查与导出 |
| 技能发现 | [find-skills](find-skills/SKILL.md) | 寻找已有技能、评估来源、补充当前缺少的能力 |

Figma 视觉交付和图标技能用途不同；图标任务可组合读取，不互相替代。旧 `codex-workflow-memory` 的长期规则已经合入 `personal-ai-work`，本仓库不再增加重复副本。

## 三、按任务读取：主规范的补充细则

| 细则 | 读取条件 |
|---|---|
| [视觉规范](references/visual-guidelines.md) | Figma、品牌图片、SVG、局部精修 |
| [Figma 桌面自动化](references/figma-desktop-automation.md) | 涉及桌面自动化、结构化导入、检查与预览等原有触发条件 |
| [文档与表格规范](references/document-guidelines.md) | 表格、Word、翻译或文档编辑 |
| [提示词规范](references/prompt-guidelines.md) | 编写可复用提示词 |
| [代码与项目规范](references/development-guidelines.md) | 编码、Android 或项目修改 |
| [插件与技能维护](references/skill-maintenance.md) | 技能发现、安装更新、GitHub 同步与去重 |
| [本机记录与周会](references/local-reporting.md) | 周会、总结、经验回顾或工作量统计，执行本机来源及统计基线限制 |

技能目录内的 `references/`、`scripts/`、`assets/` 是对应技能的资料、工具和模板，按其入口指令使用。

## 安装与调用

本机 Codex 的默认入口保持为 `/Users/yeahmobi/.codex/skills/personal-ai-work/SKILL.md`。仓库更新不会自动安装到本机或其他设备。

安装主规范时，将根目录 `SKILL.md`、`references/` 和 `docs/` 一起放入 `personal-ai-work/`。安装某个专项技能时，只复制它的整个同名文件夹到客户端的技能目录；例如 `~/.codex/skills/` 或 `~/.cursor/skills/`。不要把整个仓库当成单个技能复制，否则会混入不相关的技能与资源。

调用时可以说“用 UI走查-飞书 走查这个页面”“用 OpenFilm 剪这个视频”“查找适合这项工作的 skill”。按当前环境已安装的技能选择，不把仓库中有文件当成已经安装成功。

`UI走查-飞书` 的原有依赖：已登录的 `lark-cli`、Node.js、`puppeteer-core`、本机 Chrome、Python 和 Pillow。Figma token 使用环境变量 `FIGMA_TOKEN`，不提交到仓库。

`find-skills` 和 `openfilm` 的官方来源、保存版本、许可证和更新办法见 [第三方技能说明](docs/external-skills.md)。本仓库没有配置自动持续更新。
