import streamlit as st

st.set_page_config(page_title="银行营销数据分析系统", page_icon=":bank:", layout="wide")

st.title("银行营销数据分析与预测系统")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.page_link("app/main.py", label="首页", icon=":house:")
    st.page_link("app/pages/01_data_analysis.py", label="数据分析", icon=":bar_chart:")

with col2:
    st.page_link("app/pages/02_prediction.py", label="在线预测", icon=":mag:")

st.markdown("---")
st.markdown("### 快速导航")
st.info("点击左侧边栏或上方链接进入功能页面。")
