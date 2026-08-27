# Figma 桌面自动化工作流

用于把结构化设计数据导入 Figma 并保留可编辑图层，以及在导入或重建后诊断、验证和精修画板。用户偏好在权限允许时由代理全自动执行，而不是只提供手动步骤。

## 路线选择

1. 先检查当前会话是否具有已认证且可写的 Figma 工具。若可以直接创建或修改节点，优先使用该工具。
2. 如果只有只读接口、认证失败或没有可写工具，采用本地插件路线：生成数据完全内嵌、无需网络的 Figma 开发插件，再通过桌面端运行。
3. 已确认不可用的路线不要反复重试。历史环境中，REST API（应用程序接口）不能写入文件内容，本地 MCP（模型上下文协议）通常只读，远程 MCP 也可能因 OAuth（开放授权）客户端限制而不可用；但这些属于环境状态，不得在新环境中未经检查便当作永久事实。

## 运行环境与兼容回退

- 先检查 `node`、`jq`、`python3`、`osascript`、`sips`、`base64` 和 `xxd` 是否可用，只检查一次并记录结论。
- 已知受限 macOS 环境可能没有 Node.js 和 jq，系统 `python3` 可能触发 Xcode Command Line Tools（命令行工具）安装弹窗。遇到该环境时，JSON 和文件处理统一用 JXA（JavaScript for Automation，自动化 JavaScript）：`osascript -l JavaScript`。
- JXA 读取文件使用 `$.NSString.stringWithContentsOfFileEncodingError`。大 JSON 含数 MB base64 时，不用 shell `cat` 拼接。
- JXA 的 Objective-C（苹果运行时接口）桥接可能不稳定。若 `NSData.alloc().initWithBase64EncodedStringOptions`、`base64Encode` 或 `memoryRangeRead` 不可用，先用 `NSString.writeToFileAtomicallyEncodingError` 写 `.b64` 文本，再用 `base64 -D -i input.b64 -o output` 解码。
- `NSDictionary` 或 `NSError` 参数传 `null` 可能被桥接成 `NSNull` 并导致 `-[NSNull objectForKey:]` 崩溃；需要空指针时优先传 `$()`。读取文件的 `stringWithContentsOfFileEncodingError(..., null)` 是已知例外；写文件可使用 `dataUsingEncoding().writeToFileAtomically()` 绕开错误指针。
- 图片尺寸、格式转换和裁剪优先使用 `sips`。

## 第一部分：导入可编辑设计

### 解析源数据

- 统计 `FRAME`、`RECTANGLE`、`TEXT` 数量、字体清单和图片 base64 总量。
- 抽样确认字段名和数据形态，包括 `characters`、`fontFamily`、`fontStyle`、`fontSize`、`lineHeight`、`color`、`textAlign`、`cornerRadius` 和 `fills[].dataUri`。
- 明确子节点坐标是相对父级还是画布绝对坐标。od-figma 通常使用相对父级坐标；其他格式必须从样本验证。

### 生成本地插件

- 产出 `manifest.json` 和 `code.js`。纯内嵌数据的清单必须包含：`"networkAccess": {"allowedDomains": ["none"]}`。
- `code.js` 由生成器写入 `const DATA = {...}` 与通用运行时，不手工拼接大段 JSON，避免引号与转义损坏。
- 若当前环境有 JavaScript 运行时，用 `new Function(code)` 做只编译不执行的语法检查；只有输出 `SYNTAX OK` 才进入运行阶段。没有该运行时时，使用可用的等价解析器或在 Figma 运行前明确标注未完成此项验证。

### 插件运行时不变量

- 字体：用 `figma.loadFontAsync` 按 `family/style` 加载并缓存，失败依次回退到 Inter、Roboto。`TEXT` 节点必须先成功加载字体，再赋值 `characters`。
- 图片：base64 data URI（数据地址）经 `figma.base64Decode` 和 `figma.createImage(bytes)` 得到 `imageHash`，然后设置 `fills = [{type: 'IMAGE', scaleMode, imageHash}]`；不能直接把 data URI 塞进 fill。
- 节点：递归渲染 `FRAME`；`RECTANGLE` 支持圆角与 `SOLID`/`IMAGE` 填充；`TEXT` 先设 `fontName` 再设 `characters`，并支持字号、像素行高、对齐、颜色和透明度。
- 坐标：绝对坐标数据必须在生成前减去父级偏移，否则子节点会堆到画板右下方。相对坐标数据可直接使用。
- 摆位：遍历 `figma.currentPage.children` 计算现有内容最右边界，把新画板放在右侧至少 100px；同名精修版本放在同名画板最右边界再加 200px，避免遮挡。
- 完成后用 Figma 通知汇报生成的画板或容器、图片和文本图层数量。

### 运行方式

- 手动兜底：Plugins → Development → Import plugin from manifest…，选择 `manifest.json`，再从 Development 菜单运行插件。
- 自动执行：用 AppleScript 操作 Figma 菜单。菜单项结尾是单个省略号字符 `…`；文件选择框按 `Cmd+Shift+G` 打开“前往文件夹”，输入 manifest 绝对路径，回车选中，再用 Return（key code 36）确认。
- 自动化每个关键步骤后截图并核验当前状态，再继续下一步；不要无验证地连续发送快捷键。

## AppleScript 操作 Figma

- `System Events` 前台执行可能被 TCC（透明度、同意与控制权限）拒绝并提示不允许辅助功能访问；使用已获授权的后台执行方式，并等待进程完成。
- 菜单点击偶发 `-10000` 无效事件错误时可有限重试；连续失败后停止并报告，不无限循环。
- `scrollAndZoomIntoView` 定位画板较可靠；禁止连续 Zoom In，避免视图漂移。
- 运行新插件会自动关闭旧插件 UI（用户界面），无需额外关闭。
- Figma Electron（桌面壳）通常不暴露完整 AX（辅助功能）元素，不能依赖 UI 脚本定位图层或插件面板；全局快捷键也可能误触画布工具或选中无关图层。
- AppleScript 驱动属于外部界面操作，执行前仍遵循当前会话的权限和确认要求。

## 第二部分：验证与精修

### inspect 诊断插件

- 只读运行，不修改画布。
- 用大字号等宽文本列出目标画板顶层节点的坐标和尺寸，并进行重叠检测。
- 对精修目标建立明确断言，例如四角圆角、高度、接缝间距、字体族、字号、行高和颜色，逐项输出 `PASS` 或 `FAIL`。
- od-figma 的 `TEXT` 属性位于节点顶层字段，不在 `style` 子对象中。

### preview 整页核验插件

- 对目标画板调用 `exportAsync` 导出 PNG，再用 `base64Encode` 在 `showUI` 中显示整页预览。
- 插件 iframe（内嵌页面）通常无法可靠接收桌面键盘焦点，因此不要向面板发送 Home、PageDown 等按键。
- 在 UI 内注入 JavaScript 自动循环滚动；步长不超过视口高度的一半，滚到底后回到顶部。每个区段截图核验，避免漏段。
- 桌面截图后用 `sips` 按当次实际测量的面板坐标裁出预览区域；不要复用上次浮动坐标。

### 幂等重建修改插件

- 参数修正后重建画板时，先识别并清理本次目标位置的旧生成结果或散落图层，再按新数据重建。
- 清理范围必须精确限定在本插件生成且属于当前目标的节点；不删除用户原稿、已确认版本或无关画板。
- 覆盖导入路径中的 `code.js` 后重新运行同一开发插件，结果应可重复执行而不累计重复层。

## 图片空白边带测量与裁剪

1. 用 `sips -s format bmp` 转为位图。注意 `sips` 可能生成 top-down（自上而下行序）的负高度 BMP。
2. 对每一行做全宽像素扫描，不使用单列或少列采样。行偏移公式：`off = dataoff + y * rowSize + x * 3`，其中 `rowSize = ((w * 3) + 3) & ~3`，像素为 BGR 顺序。
3. 可用 `xxd -p -l rowBytes -s off` 读取整行十六进制，再用 `awk` 逐像素比较；macOS `awk` 没有 `strtonum` 时实现 `h2d` 十六进制转换函数。
4. 多模态模型可能对窄长裁片补全并不存在的内容，因此空白判断以像素扫描为准，视觉查看只用于粗定位和复核。
5. 裁剪前确认内容没有只出现在中间列；例如底部标语条属于内容，不可误判为空白。
6. 只裁到卡片底边线的外侧，保留边线与圆角。使用 `sips --cropToHeightWidth H W --cropOffset Y X` 时先在副本上验证坐标含义。
7. 裁剪后的缩放公式：`s = FRAME_W / (w0 - cl - cr)`。

## 精修不变量

- 文本高度：创建文本后按 `resize(w, h)` → `textAutoResize = 'HEIGHT'` → `characters` 的顺序设置，确保多行文本获得真实高度。若先设 auto-resize 再 resize，可能锁定约 10px 高度并导致后续文本重叠。
- 渐变方向：top→bottom 时，`gradientTransform [[0,-1,1],[1,0,0]]` 表示 stop0 在顶部；`[[0,1,0],[-1,0,1]]` 表示 stop0 在底部。
- 动手前解析原始设计文件核对字体、圆角、颜色和坐标；不得凭截图猜可直接读取的数据。
- 先检查 View → Outline（轮廓）模式。若用户报告图片消失或只剩线框，可能是误触 `Cmd+Shift+O`，切回后再排查画布数据。
- 不向插件 iframe 发送键盘事件；滚动由 UI 内脚本完成。

## 验收标准

- 生成：`code.js` 通过语法编译检查并输出 `SYNTAX OK`。
- 导入：Figma 通知显示生成数量，且没有字体替代警告；图层保留原始命名，可逐个选择和编辑。
- 结构：inspect 的圆角、高度、间距和字体规格断言全部 `PASS`，重叠检测无异常。
- 视觉：preview 自动滚动覆盖整页，逐段截图无重叠、空白断层、裁切错误、模糊、字体替换或边框中断。
- 桌面：最终全屏截图确认画板位置、版本关系和整体效果。
- 交付：清楚列出已验证项目；任何未能实际运行的检查必须标明，不能用推测代替完成声明。
