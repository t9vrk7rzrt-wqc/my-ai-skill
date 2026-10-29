# REA 安装与来源

- 官方源码：https://github.com/morluto/rea
- 用户源码分支：https://github.com/t9vrk7rzrt-wqc/rea
- 官方文档：https://github.com/morluto/rea/blob/main/docs/installation.md
- npm 包：`rea-agents@6.8.0`，MIT；接入日期：2026-10-29。
- 核对的上游 main 提交：`cf9f010dcdc01f1227cb1d3ec8e626a1a3b1054d`。运行包以 npm 6.8.0 和锁文件为准；main 的后续变更不代表已经安装。

## 当前 macOS 本机

独立运行目录：`/Users/yeahmobi/Desktop/REA接入/runtime`。不要删除或移动正在被 MCP 配置引用的目录。

Node：`/Users/yeahmobi/Desktop/REA接入/runtime/node_modules/node/bin/node`。

REA 入口：`/Users/yeahmobi/Desktop/REA接入/runtime/node_modules/rea-agents/scripts/rea.mjs`。

官方技能：`/Users/yeahmobi/Desktop/REA接入/runtime/node_modules/rea-agents/skills/reverse-engineer-anything/SKILL.md`。

CLI 使用上述绝对 Node 路径运行上述 REA 入口，再追加子命令；不要退回版本较旧的系统 Node。

## 其他机器

GitHub 源码副本和本技能不会自动安装本机运行环境。先核对官方 Node 要求，在可信且独立的目录安装固定版 REA；运行 setup 的只读计划，检查路径、备份与变更后按用户已有授权配置指定客户端。保留 `rea` 的显式调用策略，避免安装另一个可自动触发的同用途技能。

更新需用户授权，先查看官方发布说明与运行要求，再验证 CLI、MCP 连接及本入口；不得定时自动更新。
