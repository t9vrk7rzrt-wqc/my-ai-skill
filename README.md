# my-ai-skill
我的个人ai工作技能

每个文件夹是一个 skill（`SKILL.md` 格式，Cursor / Codex 通用）。

| skill | 用途 |
|---|---|
| `ui-walkthrough-feishu` | 对照 Figma 与线上网页做 UI 走查：同倍率合并标注图，写入飞书多维表格（页面→尺寸→模块），回读校验，不丢他人数据。触发词：走查、UI验收、还原度、飞书走查表 |
| `personal-ai-work`（根目录 `SKILL.md`） | 个人长期工作偏好 |
| `figma-visual-handoff` / `figma-icon-replacement-qa` | Figma 视觉交付 / 图标替换 QA |
| `gui-design-patent-cn` | 中国大陆 GUI 外观设计专利交底 |
| `guizang-ppt-skill` | 网页横向翻页 PPT |

## 下次调用

```bash
git clone https://github.com/t9vrk7rzrt-wqc/my-ai-skill.git /tmp/my-ai-skill   # 已有则 git pull
cp -R /tmp/my-ai-skill/ui-walkthrough-feishu ~/.cursor/skills/                  # Cursor 个人 skills
cp -R /tmp/my-ai-skill/ui-walkthrough-feishu ~/.codex/skills/                   # Codex（可选）
```

然后对 Cursor 说“用 ui-walkthrough-feishu 走查 XX 页面”，或直接说“做 UI 走查”。

`ui-walkthrough-feishu` 依赖：`lark-cli`（已登录）、`node` + `npm i puppeteer-core` + 本机 Chrome、`python3` + `Pillow`；Figma token 只放环境变量 `FIGMA_TOKEN`，用完撤销。
