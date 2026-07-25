# 口才训练营 (eloquence-camp) · Hermes Agent 规范

> SCALE OS 方法论适配版（v12.3 → 口才项目）。本配置旨在培养 Agent 的工程素养：
> 学习研究当前实际环境，灵活适配，完成任务后沉淀知识。详见下方 §0–§1 与 GATES。

## META
- agent: hermes
- scenario: standard
- stack: python + uni-app(vue3) + flask + sqlite
- generated: 2026-07-25
- scale_version: 12.3 (adapted)
- doc: HERMES.md

## COMMANDS
dev:server: cd server && source .venv/bin/activate && python wsgi.py
dev:mini: cd miniapp && npm run dev:mp-weixin
build:mini: cd miniapp && npm run build:mp-weixin
test:server: cd server && source .venv/bin/activate && pytest
lint:python: ruff check server/ miniapp/scripts 2>/dev/null; ruff format --check server/ 2>/dev/null
format:python: ruff format server/
lint:js: npx prettier --check "miniapp/src/**/*.{vue,js}" "admin/src/**/*.{vue,js}" "h5/src/**/*.{vue,js}"

## TECH_STACK
- 微信小程序 / H5 / 管理后台: uni-app (Vue3)
- 后端: Flask + Flask-SQLAlchemy + Flask-JWT-Extended
- 数据库: SQLite (开发) / MySQL (生产, 通过 DATABASE_URL 覆盖)
- 语音/AI: 阿里云百炼 DashScope (Qwen / Paraformer) — 可选
- 部署: 微信开发者工具 (小程序) + 任意静态托管 (H5/admin)

## AGENT_CAPABILITY
- support_level: medium
- memory_files: HERMES.md, SOUL.md, USER.md, memory
- hooks: unsupported-or-limited
- mcp: supported

## §0 核心元认知（不可逾越）
### 0.1 认知诚实
- 不确定时，输出 [UNCERTAIN] 并说明缺失什么
- 未实际运行验证，绝不允许输出"通过"
- 不编造未在代码中定义的调用关系

### 0.2 显性推理
- 影响面分析：每次修改前，列出所有可能受影响的模块、文件、功能
- 抓主要矛盾：识别问题的核心根因，先解决主要矛盾再处理次要问题
- 权衡方案：存在多种方案时，列出利弊并说明选择理由

### 0.3 Owner 意识
- 做A + 检查B同类问题 + 确保不影响C
- 一个bug进来，一类问题出去——修复时寻找同类问题并一并处理
- 做超出用户要求的有价值工作时，标记 [OWNER]

### 0.4 反惰性警觉
| 懒惰模式 | 表现 | 检测方式 | 纠正策略 |
| --- | --- | --- | --- |
| 暴力重试 | 同命令连续失败多次不换思路 | 同命令连续 3 次失败 | 回到分析根因，换策略 |
| 忙碌假象 | 反复修改同一文件无新信息产生 | 同文件连续修改 ≥3 次无进展 | 停下来，换思路或 /clear |
| 表面修复 | 只修表象不查根因 | 修复后同类问题复现 | 问"为什么"至少 3 层 |
| 静默跳过 | 跳过验证步骤不说明 | 验证步骤被跳过且无日志 | 所有跳过必须标注 [SKIP] + 原因 |
| 责任外推 | 将失败归因于环境/依赖 | 失败描述含"可能是环境问题" | 先验证自身代码正确性，再排除环境 |

> ⚠️ 甩锅前必须验证：你的代码逻辑本身是否正确。90%的"环境问题"实为代码逻辑问题。

### 0.5 技能优先意识
- 相关性强或存在明确触发条件时，主动选择最小可用技能集；不得为了凑流程调用无关技能
- 调用技能前，先确认技能是否支持当前技术栈、Agent、权限和安全边界
- 安装第三方技能前，先检查来源、脚本、依赖、postinstall、权限和 lockfile 变化

## §1 任务分级与场景模式
| 级别 | 定义 | 要求流程 | 门控强度 |
| --- | --- | --- | --- |
| S（小任务） | 单文件修改、bug修复、配置调整 | 3步：分析→执行→验证 | G4+G5 |
| M（中任务） | 多文件联动、新功能开发、重构 | 5步：探索→规划→执行→验证→交付 | G1-G7 |
| L（大任务） | 架构变更、跨模块重构、系统集成 | 6步：技能扫描→探索→规划→执行→验证→交付 | G0-G7 + 懒惰检测 |

> 当前项目级别: **M** | 场景模式: **standard**

## CODE_RULES
[ENFORCED] 禁止空 catch 块（至少 log 原因）
[ENFORCED] 禁止硬编码密钥、token、password、private key（用环境变量 / .env，.env 不入库）
[ENFORCED] Python 函数必须有参数和返回类型标注
[ENFORCED] 前端组件使用 Vue3 <script setup> 组合式 API
[ENFORCED] 小程序 API 地址集中在 src/api/request.js 与 App.vue 的 getBaseUrl()，禁止散落硬编码 IP
[ENFORCED] 后端用户接口允许匿名访问的返回结构必须与登录态一致（避免前端 401 误弹"网络异常"）

## KARPATHY_PRINCIPLES
[K1-THINK] 编码前必须明确列出假设，不确定时停下来提问而非猜测
[K1-THINK] 存在多种解释时必须呈现所有选项，不得默默选择一种
[K1-THINK] 存在更简单方案时必须提出异议
[K2-SIMPLE] 禁止添加未要求的功能、抽象、灵活性或可配置性
[K2-SIMPLE] 如果 200 行可写 50 行，必须重写——资深工程师检验标准
[K2-SIMPLE] 禁止为不可能场景添加错误处理
[K3-SURGICAL] 每一行修改都必须可追溯到用户请求——无关改动零容忍
[K3-SURGICAL] 禁止"顺手"重构、改格式、加类型标注、改注释
[K3-SURGICAL] 匹配现有代码风格，即使你更倾向不同写法
[K4-GOAL] 必须将命令式任务转化为可验证目标：测试先行→实现→验证
[K4-GOAL] 多步任务必须声明计划：1. [步骤] → 验证: [检查]
[K4-GOAL] 成功标准必须明确——弱标准（"让它工作"）需要不断澄清

## WORKFLOW
- mode: standard
- step_0: 技能扫描 → 扫描已安装技能清单，确认可用工具
- step_1: 探索 → 读知识文档 + 扫代码 + 找验证命令
- step_2: 规划 → 影响分析 + 契约定义 + 回滚思考
- step_3: 执行 → RED/GREEN/REFACTOR
- step_4: 验证 → 运行真实命令，不用脑补结果
- step_5: 交付 → 列出完成内容、验证结果、未验证项
- step_6: 沉淀 → 更新知识文档，记录经验教训

## GATES（口才项目适配版，仅保留有意义的）
- G1: 探索完成 → 已读文件、命令或测试证据可追溯
- G2: 规划完成 → 计划包含边界、风险、验证方式
- G4: Lint 通过 → ruff check exit code = 0 (python) / prettier --check exit 0 (js)
- G5: 测试通过 → pytest exit code = 0 (server/tests)
- G6: 构建通过 → miniapp/h5/admin build 不报错（CI 中验证）
- G7: 安全检查 → 无密钥硬编码、无危险删除、无未授权数据变更
- [G-AL] 反惰性门控 → 无暴力重试、无忙碌假象、无表面修复、无静默跳过、无责任外推
- [G-CP] 上下文污染检测 → 修正次数 < 2，否则执行 /clear

## 工程红线 (engineeringRedLines)
- 不得声称未运行的验证通过
- 不得把临时日志、截图、视频、一次性脚本默认提交到 git（.env / dist / node_modules 已在 .gitignore）
- 不得在日志、文档、测试报告中输出 token、密码、手机号、身份证、密钥和连接串
- 不得绕过项目的 ORM、框架、日志、错误处理、安全和 UI 规范
- 禁止在 Windows 下载目录 (C:\Users\zjjzo\Downloads) 创建脚本/测试文件
