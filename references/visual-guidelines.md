# 视觉任务路由与品牌语境

本页只负责专项选择与品牌语境。通用沟通、修改边界、版本保护和交付原则由根目录SKILL.md维护。

| 任务 | 唯一专项规范 | 组合条件 |
|---|---|---|
| 位图生成、修图、真实产品替换、同尺寸增强、前后核验 | image-editing-standards · 生图即修图规范 | 生图/编辑时读取当前环境imagegen |
| SVG图标候选、精修、统一、替换和实际尺寸验收 | figma-icon-replacement-qa | 写入Figma前读取figma-use |
| Figma页面、移动适配、图片Frame与文字分层 | figma-visual-handoff | 图标或图片另进入对应专项 |
| Figma对线上页面、标注证据、飞书记录 | ui-visual-audit-feishu | 静态范围、视口、语言以当轮要求为准 |
| HTML网页PPT、杂志风/瑞士风演讲配图与封面 | web-ppt-guizang | 配图执行生图规范，不把演示稿整体生为图片 |

按当前环境实际技能名称发现；仓库有文件不代表已安装。不因任务含图片就一次加载全部视觉技能。

## 品牌网站语境

- 德国太阳能、阳台光伏和家庭能源网站，先理解模块目的、人群、产品形态与当地使用场景；其他市场按本轮要求判断。
- 竞品只用于理解行业场景、信息层级和构图，不复制图片、品牌元素、具体版式或可识别创意。
- 位图真实性、来源、局部保护、透视厚度、文字区、网页裁切和放大验收，统一在image-editing-standards维护。
- 图标语义、线宽、颜色、端点、光学居中、实际尺寸、候选与SVG打包，统一在figma-icon-replacement-qa维护。

## Figma工具衔接

写入或程序化结构检查前读取当前figma-use，接口以当前文档为准；页面与导出结构按figma-visual-handoff验收。涉及结构化导入、本地插件、桌面自动化、inspect/preview、像素扫描或空白边带裁剪时，补读[Figma桌面自动化](figma-desktop-automation.md)。
