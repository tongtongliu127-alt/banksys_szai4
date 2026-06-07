# PROGRESS · banksys_szai4 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-06-07 · by AI)

- **六步流程阶段**: `初始化规划 — 等待用户确认（第 ① 步之前）`
- **上一步完成**: 填写 `00-project-context.md` 和 `01-requirements.md`，确定项目技术栈与需求
- **下一步 (TODO 第一条)**: 建仓（第 ① 步）
- **阻塞项**: 无（等待用户确认后开始执行）

---

## 待办清单 (TODO,按优先级)

### 第一批：初始化项目工程化与 CI（US-1）

- [ ] **① 建仓**
  - [ ] 使用 `gh` 创建 GitHub 仓库 `banksys_szai4`
  - [ ] 初始化本地 git，提交占位结构到 main
  - [ ] **✋ 确认门**：报仓库地址
- [ ] **② 开 feature 分支**
  - [ ] 从 main 切出 `feature/1-init-ci`
  - [ ] **✋ 确认门**：报分支名
- [ ] **③ 本地模块化开发（逐模块汇报）**
  - [ ] 模块 A：创建目录结构（`app/`、`app/pages/`、`app/models/`、`app/ml/`、`app/utils/`、`tests/`）
  - [ ] 模块 B：`pyproject.toml`（ruff 配置）
  - [ ] 模块 C：`requirements.txt` + `requirements-dev.txt`
  - [ ] 模块 D：`Dockerfile`
  - [ ] 模块 E：`.github/workflows/ci.yml`（ruff format + ruff check + pytest --cov + docker build）
  - [ ] 模块 F：`.gitignore`
  - [ ] 模块 G：`app/main.py` 最小 Streamlit 入口（页面导航 + 健康检查）
  - [ ] 模块 H：基础测试 `tests/test_main.py`
  - [ ] **✋ 确认门**：每个模块完成后汇报
- [ ] **④ 本地 CI 自检（AI 执行）**
  - [ ] `ruff format --check .`
  - [ ] `ruff check .`
  - [ ] `pytest --cov --cov-fail-under=80`
  - [ ] **✋ 确认门**：全绿后汇报，进入下一步
- [ ] **⑤ 触发 PR**
  - [ ] `git push` 分支
  - [ ] `gh pr create` 发起 PR
  - [ ] **✋ 确认门**：报 PR 链接 + CI 状态
- [ ] **⑥ 人工审核 → 合并 → 本地 Docker 验证**
  - [ ] **✋ AI 在此硬停**：等待人工 Review 和合并
  - [ ] 合并后本地 `docker build -t banksys . && docker run -d --name banksys -p 8004:8501 banksys`
  - [ ] **✋ 确认门**：报本地访问 URL `http://localhost:8004`

### 第二批：数据加载与预处理模块（US-2）

- [ ] 实现 `app/models/data_loader.py`（加载 CSV、处理缺失值）
- [ ] 编写 `tests/test_data_loader.py`（正常加载、文件不存在、列校验）
- [ ] 本地自检 + 提 PR

### 第三批：数据分析交互页面（US-3）

- [ ] 实现 `app/models/visualizer.py`（图表生成逻辑，与页面解耦）
- [ ] 实现 `app/pages/01_data_analysis.py`（数据概览、年龄分布、职业认购率、教育热力图等）
- [ ] 编写 `tests/test_visualizer.py`
- [ ] 本地自检 + 提 PR

### 第四批：模型训练脚本（US-4）

- [ ] 实现 `app/ml/train.py`（特征编码 + 模型训练 + 输出 model.pkl/encoder.pkl）
- [ ] 配置 `ml/model/` 加入 `.gitignore`
- [ ] CI 增加模型训练检查
- [ ] 本地自检 + 提 PR

### 第五批：预测服务核心逻辑（US-5）

- [ ] 实现 `app/models/predictor.py`（加载模型、特征编码、返回预测结果）
- [ ] 编写 `tests/test_predictor.py`（正常预测、模型缺失、非法输入）
- [ ] 本地自检 + 提 PR

### 第六批：在线预测页面（US-6）

- [ ] 实现 `app/pages/02_prediction.py`（点选式表单 + 预测结果展示）
- [ ] 端到端验证：Docker 启动后页面可访问、预测功能正常
- [ ] 本地自检 + 提 PR

### 第七批：测试覆盖与质量门禁完善（US-7 & US-8）

- [ ] 补充测试覆盖率到 ≥80%
- [ ] 验证完整 CI 流程
- [ ] 最终本地验收（docker run → 页面访问 → 分析 + 预测均正常）

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-06-07 | 选择 Streamlit 作为 Web 框架 | 快速构建数据应用；适合数据分析与模型演示场景 |
| 2026-06-07 | 模型训练离线，预测在线 | 训练是重操作不适合实时请求；预测是轻操作需快速响应 |
| 2026-06-07 | 数据集进 Git，模型产物不进 Git | 教学用公开数据；模型产物二进制大文件不进版本控制 |
| 2026-06-07 | 端口 8004（主机）→ 8501（容器） | 课程指定；Streamlit 默认 8501，Docker 映射 |
| 2026-06-07 | **不做 CD / 远程部署** | 用户明确要求仅 CI + 本地部署 |

---

## 已知坑 (GOTCHAS)

- 暂无（开始开发后记录）

---

## 里程碑 (DONE)

- [x] 2026-06-07：填写 `00-project-context.md`，确定技术栈（Python 3.11 + Streamlit + pytest + ruff + Docker）、目录地图、质量门槛
- [x] 2026-06-07：填写 `01-requirements.md`，定义 8 个用户故事（US-1 ~ US-8），覆盖完整开发流程
- [x] 2026-06-07：初始化 `PROGRESS.md`，列出第一批 TODO

> 反臃肿:里程碑超过 15 条时,把更早内容合并成一行摘要,保持本文件可快速阅读。
