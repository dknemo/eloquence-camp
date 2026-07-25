# 口才训练营 · 开发贡献规范 (CONTRIBUTING)

> 本规范基于 SCALE OS 工程方法论适配。所有门禁在 `HERMES.md` 与 CI 中强制执行。

## 1. 任务分级
| 级别 | 含义 | 要求 |
| --- | --- | --- |
| S | 单文件/配置/文案小改 | 跑相关命令验证即可 |
| M | 多文件功能/bugfix | 探索→规划→执行→验证→交付 |
| L | 跨模块/架构/重构 | 含运行时证据、回滚计划 |

## 2. 提交规范 (Conventional Commits)
格式: `<type>(<scope>): <subject>`
- type: `feat` / `fix` / `docs` / `style` / `refactor` / `test` / `chore`
- scope: `mini` / `h5` / `admin` / `server` / `config`
- 例: `fix(server): 用户接口匿名降级避免网络异常弹窗`

提交信息由 `commitlint` 校验（G16 提交纪律）。

## 3. 代码红线 (CODE_RULES)
- 禁止空 catch 块（至少 log）
- 禁止硬编码密钥（用 `.env`，已 gitignore）
- Python 函数必须有类型标注
- 小程序 API 地址集中在 `src/api/request.js` + `App.vue getBaseUrl()`，禁止散落 IP
- 后端用户接口需兼容匿名访问，返回结构与登录态一致

## 4. 验证门禁 (GATES)
每次推送/PR 必须真实跑过：
- **G4 Lint**: `ruff check server/` + `npx prettier --check` (前端)
- **G5 Test**: `cd server && pytest`
- **G6 Build**: miniapp/h5/admin `npm run build` 不报错
- **G7 Security**: 无密钥硬编码（CI secret scan）

## 5. 分支策略
- `main` 为保护分支，禁止直接 push，必须走 PR
- PR 需通过 CI（lint/test/build/security）
- 单人开发也走 PR 流程，保留决策记录

## 6. 不做的过度工程
- 不为不可能场景加错误处理
- 不引入未要求的抽象/配置
- 不照搬他人商业小程序代码（侵权 + 审核风险）
