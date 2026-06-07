# PROGRESS · 项目进度 〔活记忆 · AI 维护〕

---

## 当前状态

- **六步流程位置**: 第⑤步 — PR #3 等待创建
- **当前分支**: `feature/3-data-analysis`
- **CI 状态**: 本地自检全绿，待推送
- **应用**: http://localhost:8004 运行中

---

## 已完成

- [x] US-1: 项目初始化与 CI（PR #1 已合并）
- [x] US-2: 数据加载与预处理模块（PR #2 已合并）
- [x] US-3: 数据分析交互页面（当前 PR）
  - `app/models/visualizer.py`: 9 个图表函数（饼图/柱状/直方/箱线/热力图/折线）
  - `app/pages/data_analysis.py`: 4 个 Tab 页（认购分布/类别分析/数值分析/相关性）
  - 交互式特征选择器，图表实时切换
  - 测试: 29/29 通过，覆盖率 95%

---

## 下一步 TODO

- [ ] US-4: 模型训练脚本
- [ ] US-5: 预测服务核心逻辑
- [ ] US-6: 在线预测页面
- [ ] US-7: 健康检查验证
- [ ] US-8: 质量门禁收尾

---

## 决策记录 (ADR)

### ADR-1: 模型选型
RandomForestClassifier，对类别特征友好，可输出概率。

### ADR-4: 页面文件命名不带数字前缀
Python 模块名不能以数字开头，使用 `data_analysis.py` / `prediction.py`。

### ADR-5: 可视化使用 plotly
交互式图表，Streamlit 原生支持 `st.plotly_chart`，比 matplotlib 静态图更适合数据探索。

---

## 踩坑记录

### GOTCHA-1: pandas EmptyDataError
空 CSV 调用 `pd.read_csv()` 抛出 `EmptyDataError`，在 `_read_csv()` 中捕获后转为 `ValueError`。

### GOTCHA-2: Streamlit 1.57 emoji shortcode 不支持
`st.page_link(icon=":house:")` 报错，改用实际 emoji 字符。
