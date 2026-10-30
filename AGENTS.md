# 智能体工作入口

## 先读通用规范

每个新窗口、每个任务实质性操作前完整读取根目录[SKILL.md](SKILL.md)，它是personal-ai-work的唯一通用规范。用户当前明确要求优先；已有授权内的常规动作直接推进。

## 按工作方向选择一个主技能

优先看[技能索引](skills-index.json)的name、display_name、category、purpose、entry。需要安装、旧名迁移或比较边界时看[README](README.md)。只读取当前任务需要的专项，跨方向任务再组合，不一次加载全部技能。

| 工作方向 | 主技能 |
|---|---|
| 生成/修复位图、真实产品、前后图和保护区核验 | image-editing-standards |
| SVG图标设计、精修、替换及实际尺寸验收 | figma-icon-replacement-qa |
| Figma布局、移动适配、分层与前端素材交付 | figma-visual-handoff |
| Figma对线上页面、标注证据及飞书记录 | ui-visual-audit-feishu |
| 中国GUI外观专利交底、Word与状态图包 | gui-design-patent-cn |
| 网页PPT、演讲配图与封面 | web-ppt-guizang |
| 视频剪辑、字幕、动画与导出 | openfilm |
| 查找、评估和安装技能 | find-skills |
| 应用/发布包分析 | rea，仅限明确立即调用 |

REA只有用户明确说“调用REA开始完成这个工作”或明确要求立即用REA执行时才读取并启动；仅提及、引用口令、讨论未来调用不启动目标分析，不自动后台执行。REA的allow_implicit_invocation必须保持false。

## 单一规则归属与命名

- 通用协作规则只在根目录SKILL.md维护；生图修图细则只在image-editing-standards维护；图标细则只在figma-icon-replacement-qa维护。其他入口引用，不重复维护整套规则。
- 每个专项使用用途明确的独立顶层目录，目录名与frontmatter.name一致，采用小写英文及短横线；界面显示名和描述直说中文用途。第三方工具可保留工具名以便与上游对应。
- 不加数字顺序前缀，不把技能塞入多层分类文件夹；分类体现在README和机器索引，保持入口易于发现。
- 旧名称仅记录在skills-index.json.aliases与README迁移表，不保留第二份重复Skill。更新命名时同步正文链接、显示元数据和索引。
- references、scripts、assets服务于所属技能，不是新增全局技能。先比较名称、描述、用途和内容再去重，不因相近而删掉不同交付能力。

## 来源与同步边界

第三方保留作者、来源和许可证；读取[第三方来源](docs/external-skills.md)再更新。不提交令牌、客户或私有原图、本机聊天记录、任务快照和完整工作区。匿名规则与方法可以收录，真实对比证据留在获授权的项目目录。

GitHub同步和本机安装分别验证。根目录入口在本机通常安装为~/.codex/skills/personal-ai-work/SKILL.md；跨窗口读取依赖本机全局AGENTS配置。本仓库改名不会自动改名现有安装，也不代表其他账号、设备或CODEX_HOME已经更新。
