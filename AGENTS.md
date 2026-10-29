# 本仓库工作入口

## 工作前必须读

每个新窗口、每个新任务开始，在执行实质性操作前完整读取根目录 [SKILL.md](SKILL.md)。它是 `personal-ai-work` 的唯一主规范，包含沟通方式、修改边界、版本保护、自查交付和历史文件复用要求。

当前用户明确指令优先；与已有授权一致的常规动作直接完成。不要因为任务涉及多个文件就重复索要确认。

## 按工作类型读取

按根目录 `SKILL.md` 的“阅读顺序与任务分组”表选择补充规范和专项技能。只加载当前任务需要的内容；不要把某个专项技能里的步骤推广到所有工作。

- 视觉与设计：`figma-visual-handoff`、`figma-icon-replacement-qa`、`UI走查-飞书`。
- 专利文档：`gui-design-patent-cn`。
- 网页演示：`guizang-ppt-skill`。
- 视频剪辑与制作：`openfilm`。
- 查找技能：`find-skills`。
- REA：仅当用户明确说“调用REA开始完成这个工作”或明确要求立即用 REA 执行时，读取 `rea/SKILL.md`。仅提及、引用口令或讨论未来调用不启动分析；不自动后台执行。

每个专项技能的 `references/`、`scripts/`、`assets/` 只服务于该技能，不是额外的全局规范。

## 维护边界

保留现有技能目录名和调用路径。先核对本机与远端版本、名称和用途再同步；不把功能相近直接当成重复，不复制已经合入主规范的旧记忆技能。

第三方技能保留来源和许可证，更新时对照 [第三方技能说明](docs/external-skills.md) 的版本记录核实。不得把令牌、私有素材或本机聊天记录提交到仓库。

## 本机全局生效范围

本文件自动约束该仓库范围内的工作。跨项目、跨窗口的默认读取依赖本机 `/Users/yeahmobi/.codex/AGENTS.md`，入口为 `/Users/yeahmobi/.codex/skills/personal-ai-work/SKILL.md`；更新 GitHub 不会自动替换这些本机文件。其他机器、其他客户端和不同 `CODEX_HOME` 需要分别配置。
