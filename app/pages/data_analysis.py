import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st

from app.models.data_loader import get_feature_labels, load_train_data
from app.models.visualizer import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    plot_categorical_count,
    plot_categorical_subscribe_rate,
    plot_correlation_heatmap,
    plot_education_subscribe_heatmap,
    plot_month_subscribe_rate,
    plot_numeric_box_by_subscribe,
    plot_numeric_histogram,
    plot_subscribe_pie,
)

st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")

st.title("数据分析")
st.markdown("---")


@st.cache_data
def load_data():
    return load_train_data()


try:
    df = load_data()
except Exception as e:
    st.error(f"数据加载失败: {e}")
    st.stop()

labels = get_feature_labels()
target_col = "subscribe"

total = len(df)
subscribed = int(df[target_col].eq("yes").sum())
subscribe_rate = round(subscribed / total * 100, 2)

m1, m2, m3, m4 = st.columns(4)
m1.metric("总记录数", f"{total:,}")
m2.metric("认购人数", f"{subscribed:,}")
m3.metric("未认购人数", f"{total - subscribed:,}")
m4.metric("认购率", f"{subscribe_rate}%")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["认购分布", "类别特征分析", "数值特征分析", "相关性分析"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_subscribe_pie(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_month_subscribe_rate(df), use_container_width=True)
    st.subheader("教育水平认购率")
    st.plotly_chart(plot_education_subscribe_heatmap(df), use_container_width=True)

with tab2:
    cat_feature = st.selectbox(
        "选择类别特征",
        CATEGORICAL_FEATURES,
        format_func=lambda f: labels.get(f, f),
        key="cat_select",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_categorical_subscribe_rate(df, cat_feature), use_container_width=True)
    with col2:
        st.plotly_chart(plot_categorical_count(df, cat_feature), use_container_width=True)

with tab3:
    num_feature = st.selectbox(
        "选择数值特征",
        NUMERIC_FEATURES,
        format_func=lambda f: labels.get(f, f),
        key="num_select",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_numeric_histogram(df, num_feature), use_container_width=True)
    with col2:
        st.plotly_chart(plot_numeric_box_by_subscribe(df, num_feature), use_container_width=True)

with tab4:
    st.plotly_chart(plot_correlation_heatmap(df), use_container_width=True)
    st.caption("数值特征之间的 Pearson 相关系数")
