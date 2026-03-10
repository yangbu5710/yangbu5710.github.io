# Handbook 文档整理 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将仓库文档手册化到 `handbook/`，统一为中文风格，修复断链/拼写/目录不一致，并提供脚本自动生成索引与做链接校验。

**Architecture:** 以 `handbook/` 作为内容主入口；各业务目录保留轻量 `README.md` 作为“入口/跳转页”；用一个脚本扫描目录结构与 Markdown 标题，自动生成索引页并做链接校验。

**Tech Stack:** Markdown、Node.js（可选，若仓库无 Node 环境则用 Python 实现脚本）、GitHub Pages（静态托管）

---

### Task 1: 建立 handbook 骨架与写作规范

**Files:**
- Create: `handbook/README.md`
- Create: `handbook/style-guide.md`
- Create: `handbook/_index.md`（可选：仅供脚本生成/缓存）

**Step 1: 创建 `handbook/` 目录与首页（手写最小版）**
- 首页包含：仓库定位、如何使用（导航/搜索）、主题列表（先占位）

**Step 2: 创建 `handbook/style-guide.md`**
- 约定：全中文；专有名词/命令保留英文；标题层级；代码块语言标注；链接写法；图片相对路径；目录约定

**Step 3: 本地检查 Markdown 渲染（肉眼）**

---

### Task 2: 修复已知明显问题（拼写/相对链接）

**Files:**
- Modify: `README.md`
- Modify: `ai/prompt/README.md`
- Modify: `sonarqube/README.md`（标题统一）

**Step 1: 修复根 `README.md` 的拼写**
- `artifacotory` → `artifactory`

**Step 2: 修复 `ai/prompt/README.md` 相对链接**
- 当前 `./ai/prompt/code_review/` 在该文件下不成立，改成 `./code_review/`

**Step 3: 统一不合适的顶层 slogan 标题**
- `# Be funny,be optimistic and be seek knowledge` 统一替换为中文且更具体的标题（例如“SonarQube”或“知识库目录”）

**Step 4: 运行链接校验（先用临时脚本/grep 规则）**

---

### Task 3: 自动生成索引与链接校验脚本（v1）

**Files:**
- Create: `scripts/gen-handbook-index.js`（或 `.ts` / `.py`，依赖环境确定后选其一）
- Create: `scripts/check-md-links.js`（可合并到同一个脚本）
- Modify: `README.md`（增加“如何更新索引”的命令）

**Step 1: 选择脚本语言**
- 若存在 `package.json`：Node 脚本
- 否则：用 Python 标准库实现（避免引入依赖）

**Step 2: 生成规则（最小可用）**
- 扫描 `handbook/**.md`
- 生成：
  - `handbook/README.md` 的主题列表（按目录）
  - 每个 `handbook/<topic>/README.md` 的子页面列表（按文件名/标题）

**Step 3: 链接校验规则（最小可用）**
- 解析 Markdown 中的相对链接 `](./...)` / `](../...)`
- 校验目标文件/目录存在
- 输出失败列表并以非 0 退出码

**Step 4: 运行脚本验证**
- 期望：第一次运行可能报错（断链），随后在 Task 4/5 中逐步修复直到通过

---

### Task 4: 内容迁移（从“目录 README”到“主题页面”）

**Files:**
- Create/Modify: `handbook/ai/*.md`
- Create/Modify: `handbook/container/*.md`
- Create/Modify: `handbook/artifactory/*.md`
- Create/Modify: `handbook/sonarqube/*.md`
- Create/Modify: `handbook/dev/*.md`
- Create/Modify: `handbook/linux/*.md`
- Create/Modify: `handbook/git/*.md`
- Modify: 原目录下相关 `README.md`（瘦身为入口页，指向 handbook）

**Step 1: 定义主题映射**
- `ai/**` → `handbook/ai/`
- `container/**` → `handbook/container/`
- `artifactory/**` → `handbook/artifactory/`
- `sonarqube/**` → `handbook/sonarqube/`
- `dev/**` → `handbook/dev/`
- `linux/**` → `handbook/linux/`
- `git/**` → `handbook/git/`

**Step 2: 逐主题迁移**
- 把“命令片段/操作步骤/外链索引”迁到对应主题页
- 保持原意，统一中文风格，纠正明显排版问题（代码块语言、标题层级）

**Step 3: 原目录 README 瘦身**
- 仅保留：简介 + 指向 `handbook/<topic>/` 的入口链接 +（可选）3 条最常用命令

---

### Task 5: 全仓一致性与收尾校验

**Files:**
- Modify: 全仓 `README.md`（按脚本输出/规范统一）
- Modify: 发现断链/错链的 Markdown 文件

**Step 1: 运行索引生成脚本**
- 期望：生成/更新各级索引页

**Step 2: 运行链接校验脚本**
- 期望：0 个断链；若有，修到通过

**Step 3: 快速人工抽检**
- 根入口、`handbook/README.md`、每个主题入口点开能走通

---

### Task 6: Git 提交策略（按里程碑）

**Step 1: 每完成一个主题迁移就单独提交**
- 便于回滚与 review

**Step 2: 最终提交包含**
- `handbook/` 内容
- `scripts/` 自动化脚本
- 根与各目录入口 README 的修复

