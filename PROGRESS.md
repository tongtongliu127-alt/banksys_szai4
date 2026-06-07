# PROGRESS · 项目进度 〔活记忆 · AI 维护〕

> **作用**:记录当前状态、下一步 TODO、已做决策、踩过的坑。按时间倒序，新进展加在最上面。
> **更新时机**:每完成一个模块、每次 CI 红绿变化、每次遇到坑并解决后。

---

## 当前状态

- **六步流程位置**: 第⑤步 — 准备触发 PR
- **当前分支**: `feature/1-init-ci`
- **US-1（项目初始化与 CI）状态**: 本地开发完成，准备推送
- **CI 状态**: 本地自检全绿，待推送后触发 CI

---

## 已完成

- [x] 仓库初始化 + 项目骨架（`cb52297`）
- [x] standards/ 规范文件就位（00~06）
- [x] 数据文件入库（data/train.csv、data/test.csv）
- [x] 目录骨架创建
- [x] Streamlit 主入口 `app/main.py`（多页导航）
- [x] 页面占位：`app/pages/data_analysis.py`、`app/pages/prediction.py`
- [x] 数据加载模块 `app/models/data_loader.py`
  - `load_train_data()` / `load_test_data()`
  - 处理 `unknown`/`nonexistent` 缺失值
  - 空文件、文件不存在错误处理
- [x] 测试 `tests/conftest.py` + `tests/test_data_loader.py` + `tests/test_main.py`
- [x] 本地 CI 自检全绿：
  - `ruff format --check .` ✅
  - `ruff check .` ✅
  - `pytest --cov=app --cov-fail-under=80` ✅ (11 passed, 96% coverage)
- [x] 00-project-context.md、01-requirements.md 填写完毕
- [x] PROGRESS.md 初始化

---

## 下一步 TODO

- [ ] 推送 `feature/1-init-ci` 分支
- [ ] 创建 PR 并等待 CI 全绿
- [ ] 人合并 PR
- [ ] US-2: 数据加载与预处理模块增强（如有新需求）
- [ ] US-3: 数据分析交互页面

---

## 决策记录 (ADR)

### ADR-1: 模型选型
- **决定**: 使用 scikit-learn RandomForestClassifier 作为默认模型
- **理由**: 对类别特征友好、无需大量调参即可获得可接受 AUC、可输出概率

### ADR-2: 数据不进 .gitignore
- **决定**: data/ 目录的数据文件直接入库
- **理由**: 教学公开数据，非敏感信息；CI runner 上可直接使用

### ADR-3: 模型产物不进 Git
- **决定**: ml/model/ 目录加入 .gitignore
- **理由**: 模型文件体积大（.pkl），应在 CI/本地训练时生成

### ADR-4: 页面文件命名不带数字前缀
- **决定**: `app/pages/` 下的页面使用 `data_analysis.py` / `prediction.py` 而非 `01_data_analysis.py`
- **理由**: Python 模块名不能以数字开头，数字前缀文件名会导致测试 import 失败

---

## 踩坑记录 (GOTCHAS)

### GOTCHA-1: pandas EmptyDataError vs ValueError
- **现象**: 空 CSV 文件调用 `pd.read_csv()` 抛出 `EmptyDataError`，而非返回空 DataFrame
- **修复**: 在 `_read_csv()` 中捕获 `pd.errors.EmptyDataError`，转为 `ValueError`
