import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.models.data_loader import get_data_summary, get_feature_columns, get_feature_labels

st.set_page_config(page_title="银行营销数据分析系统", page_icon="🏦", layout="wide")

st.title("银行营销数据分析与预测系统")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.page_link("app/main.py", label="首页", icon="🏠")
    st.page_link("app/pages/data_analysis.py", label="数据分析", icon="📊")

with col2:
    st.page_link("app/pages/prediction.py", label="在线预测", icon="🔮")

st.markdown("---")

st.header("数据概览")

try:
    summary = get_data_summary()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("总记录数", f"{summary['total_records']:,}")
    m2.metric("特征数量", summary["feature_count"])
    m3.metric("认购人数", f"{summary['subscribed']:,}")
    m4.metric("认购率", f"{summary['subscribe_rate']}%")

    st.markdown("---")
    st.subheader("特征列表")
    labels = get_feature_labels()
    features = get_feature_columns()
    cols = st.columns(4)
    for i, f in enumerate(features):
        cols[i % 4].caption(f"{labels.get(f, f)} ({f})")

except FileNotFoundError as e:
    st.error(f"数据文件未找到: {e}")
except Exception as e:
    st.error(f"加载数据失败: {e}")
