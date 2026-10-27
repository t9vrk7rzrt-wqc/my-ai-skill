# 参考：字段、命令、陷阱

## 表字段（沿用用户当前的表）

| 字段 | 类型 | 说明 |
|---|---|---|
| 问题描述 | 文本 | 首列；短句，`【模块】…`；用户页（About us/Support）可不带模块前缀 |
| 页面 | 单选 | Branding / About us / Support …，新页面追加选项 |
| 尺寸 | 单选 | PC端 / 移动端（同级，不再用“PC-英文”这类拼名） |
| 所属模块 | 单选 | `01 Header … 15 Footer、16 全局`，序号保证排序正确；非模块化页面可留空 |
| 语言 | 单选 | 英文 / 德语 / 双语（英德共有问题记“双语”或英文） |
| 问题截图 | 附件 | 每条恰好 1 张（可与同组共用同一张合并图） |
| 优先级 | 单选 | P0–P3（见下） |
| 问题类型 | 单选 | 用表里现有选项 |
| 需人工复核 | 勾选 | 默认不勾 |
| 前端是否完成优化 / UI验收是否通过 | 勾选 / 单选 | 默认不勾 / 留空 |
| 备注说明 | 文本 | 只放：德语【优化建议】【建议译文】、【对应图中标注 n】、“宽度相关”说明 |
| 提出时间 | 日期 | 当天 |

视图：分组 `页面 → 尺寸`，排序 `所属模块` 升序（同模块内保持记录原有先后）。用户隐藏的字段不要擅自恢复。
如果用户要求“分开放/合并”，**优先只改视图（分组/筛选/排序/可见字段）**，不动记录。

## 优先级 / 问题类型

- P0：明显错误（如数字动画显示 NaN、核心内容缺失）；P1：大块视觉不符、整块缺蒙版/素材没换、文案错位；P2：明显的尺寸/颜色/排版差异；P3：细小但确实存在
- 问题类型：基础视觉还原（布局/间距/字体/颜色/圆角/图标形状/裁切/背景）、其余视觉还原（结构/排布差异）、切图模糊（分辨率不足/拉伸）、内容更新（文案/翻译/漏译）、适配兼容（折行/溢出/宽度相关）、效果优化（润色级）、其他（尽量少用）。一条里含两类缺陷就拆开

## lark-cli base 速查（均加 `--as user --base-token <T>`）

```
+table-list / +field-list / +view-list
+record-list --table-id X --limit 200        # 落盘 ndjson，read manifest 里的 record_file；select 字段是数组
+record-batch-create --json '{"create_records":[{...}]}'      # ≤200；select 写 ["P2"]；日期 "2026-10-26"
+record-batch-update --json '{"update_records":{"recXXX":{"字段":值}}}'
+record-upload-attachment --record-id R --field-id 问题截图 --file ./相对路径.png   # 必须相对路径，cwd 在文件所在目录
+record-remove-attachment --record-id R --field-id 问题截图 --file-token T --yes
+record-history-list --record-id R             # 谁在何时改了什么（已删除记录查不到）
+view-set-group / +view-set-sort / +view-set-filter / +view-set-visible-fields
+field-create / +field-update（PUT 全量，慎用；改选项名会丢已有值，需要时新建字段迁移）
+record-delete --yes --json '{"record_id_list":[...]}'    # 先得到用户确认
```

陷阱：
- 新建表后检查是否有默认空白行；排序字段为空会让脚本排序报错，先过滤
- 用户会实时改表；所有“序号”类操作前重新拉取，改完再读回
- 附件上传一条约 3–4 秒；几十条用后台脚本并写日志，别阻塞
- wiki 链接先 `lark-cli wiki spaces get_node --params '{"token":"…"}'` 取 `obj_token` 才是 base token
- 用户在飞书改完分组后 `+view-get` 再确认，不凭记忆

## Figma 读取

REST：`GET /v1/files/:key/nodes?ids=<node>&geometry=paths`，header `X-Figma-Token`（环境变量，不落盘不回显）。导出整页 PNG 用 `/v1/images/:key?ids=…&scale=1&format=png`。
- 坐标换算成相对根画板：`x - root.x`, `y - root.y`；模块边界按画板里的区块容器或 y 区间
- 同名文字可能出现多份（隐藏的备用画板）：用 `scripts/figma_boxes.py` 默认过滤不可见祖先
- 设计稿里常有“浏览器界面图片”等不属于网站的元素（如顶部约 74px），不与网页高度直接比

## 线上采集

`scripts/capture_live.js`：固定视口 1920×1000 / 390×844，`deviceScaleFactor=1`；滚动到底触发懒加载再回顶；等待 `document.fonts.ready`；输出每个叶子元素的 rect + 计算样式（含祖先累乘 opacity）。
宽度敏感性判断：另取 1440/375/430 等宽度，对比各元素样式（`wdiff` 思路：基准 vs 其它宽度）。样式几乎不随宽度变的问题=宽度无关，直接记；只在窄屏出现的溢出/折行=宽度相关，备注说明。

## 多语言（德语为例）

- 德语页常见问题：复合词折行/溢出（Branchenführend）、品牌名+名词缺连字符（LONGi-Produkte）、称呼 Sie/du 混用、Footer/法律页英文未译（Impressum/Datenschutzerklärung/AGB/Widerrufsrecht）、数字格式（1.000 / 634,26 GW / Nr. 1）、动画把 “Nr.” 当数字导致 NaN
- 图文对应：奖项/国家名称必须与图片一一对应
- 建议译文只给有把握的；其余写“需母语者确认”；不编造替代词

## 去重与小问题判据

- “小问题”=肉眼在 100% 缩放下几乎看不出、且不影响品牌/可读性（例：标题与副标题基线差 1–3px、非关键间距差 2px）。用户点名一类后，同类全部清除
- 同一根因影响多个实例（5 个圆形图标）合并成一条，在图里标第一个并写“其余同”

## 回读校验清单

- 条数与预期一致，差异可逐条解释（谁增/删）
- 每条恰 1 附件；无空白描述；模块序号随顺序单调不降（按页面+尺寸分别判断）
- 抽查 2–3 条：描述、页面、尺寸、模块、附件文件名
- 视图：分组/排序/可见字段符合用户要求
