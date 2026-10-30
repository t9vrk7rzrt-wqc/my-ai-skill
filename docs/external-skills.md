# 第三方技能来源与调用

核对日期：2026-10-28（北京时间）。两个技能均保存官方入口原文和 MIT 许可证，未加入账号信息或运行时依赖。实际使用前按当前官方说明核验环境。

## find-skills

- 用途：查找、评估和协助安装已有技能。先检查当前可用技能，避免重复安装。
- 官方仓库：[vercel-labs/skills](https://github.com/vercel-labs/skills)。
- 入口：[find-skills/SKILL.md](https://github.com/t9vrk7rzrt-wqc/my-ai-skill/blob/main/find-skills/SKILL.md)。
- 上游路径：`skills/find-skills/SKILL.md`。
- 保存版本：[`699d35b21bd3c97dbc0edeae062b2698898bb2e5`](https://github.com/vercel-labs/skills/commit/699d35b21bd3c97dbc0edeae062b2698898bb2e5)。
- 许可证：[MIT](https://github.com/t9vrk7rzrt-wqc/my-ai-skill/blob/main/find-skills/LICENSE)。
- 技能目录：[skills.sh](https://skills.sh/)。

```bash
npx skills find <关键词>
npx skills check
npx skills update
```

`check` 检查可用更新，`update` 执行更新；它们针对 Skills CLI 管理的安装记录。这里保存的是官方文件快照，更新本仓库仍需从上游指定路径比较、同步并提交，不能假设工具会自动更新仓库副本。没有配置后台定时更新。

用户提到“约 380 万安装”，该数字未独立核验，不作为固定事实。推荐前核查实际指令、来源、依赖与权限，安装量只作参考。

## openfilm

- 用途：视频剪辑与制作、字幕、动态图形，以及 OpenFilm 项目的检查和导出。
- 官网：[openfilm.dev](https://openfilm.dev/)。
- 官方仓库：[openfilm/openfilm](https://github.com/openfilm/openfilm)。
- 入口：[openfilm/SKILL.md](https://github.com/t9vrk7rzrt-wqc/my-ai-skill/blob/main/openfilm/SKILL.md)。
- 上游路径：`skills/openfilm/SKILL.md`。
- 保存版本：[`ea8cf6dcbb367065ce16d75e9784dbe2ab3e013c`](https://github.com/openfilm/openfilm/commit/ea8cf6dcbb367065ce16d75e9784dbe2ab3e013c)。
- 许可证：[MIT](https://github.com/t9vrk7rzrt-wqc/my-ai-skill/blob/main/openfilm/LICENSE)。
- 操作手册：[官方手册](https://openfilm.dev/docs/manual/)。

官方技能入口会运行 `npx -y openfilm@latest` 读取当前手册，因此运行时手册可以随软件发布更新；本仓库入口文件仍是有版本记录的快照。仅核对并收录技能，本次未运行该命令或下载视频运行环境。

官方当前说明：命令行运行需要 Node.js 22.2+、FFmpeg，Studio 版本保存还用到 Git；首次运行可能下载 Chromium。实际使用时重新核对所安装版本的要求。生成配音、音乐或图像等外部服务需要用户自己的服务连接；收录技能不代表这些服务已经可用。

常见调用：

```bash
npx -y openfilm@latest          # 读取当前手册
npx -y openfilm@latest skills   # 列出当前内置剪辑流程和风格
```

长视频剪短片、屏幕录制演示等细分流程，以工具当时列出的技能为准，需要时再读取，避免把全部视频说明放进工作前必读规范。

## Guizang网页PPT分支

- 本仓库按工作方向命名为`web-ppt-guizang`，界面名称“网页PPT与演讲配图”。
- 上游身份保留为`guizang-ppt-skill`，来源为已有README记录的[op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)。
- 作者署名、MIT许可证、模板、脚本和参考文件保留；当前变更为目录/入口用途命名与中文发现元数据，不宣称已更新到最新上游版本。
- 两份上游README保留其官方安装命令，并在开头说明本仓库调用名与上游原名的区别。本仓库安装以根README和skills-index.json为准。

## 更新办法

1. 读取上述官方路径，对照记录的提交版本，确认变更和依赖。
2. 比较当前仓库已有修改后同步 `SKILL.md` 与适用许可证，保留用户规范。
3. 更新本页的提交版本和核对日期，校验技能格式及引用，再提交。

不执行全量安装、自动购买、上传素材或为所有技能安排后台更新。
