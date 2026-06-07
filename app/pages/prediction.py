import streamlit as st

from app.models.data_loader import get_feature_labels
from app.models.predictor import get_feature_options, predict

st.set_page_config(page_title="在线预测", page_icon="🔮", layout="wide")

st.title("在线预测")
st.markdown("---")

labels = get_feature_labels()

# Load feature options from trained model
try:
    options = get_feature_options()
except Exception:
    st.warning("模型未训练。请先运行 `python -m app.ml.train` 训练模型。")
    st.stop()

if not options:
    st.warning("模型未训练。请先运行 `python -m app.ml.train` 训练模型。")
    st.stop()

CATEGORICAL_ORDER = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]
NUMERIC_DEFAULTS = {
    "age": (40, 16, 100),
    "duration": (300, 0, 6000),
    "campaign": (2, 0, 60),
    "pdays": (999, 0, 999),
    "previous": (0, 0, 10),
    "emp_var_rate": (0.0, -5.0, 5.0),
    "cons_price_index": (94.0, 90.0, 100.0),
    "cons_conf_index": (-40.0, -60.0, -10.0),
    "lending_rate3m": (2.0, 0.0, 6.0),
    "nr_employed": (5100.0, 4800.0, 5400.0),
}

st.subheader("客户特征输入")

tab1, tab2 = st.tabs(["类别特征", "数值特征"])

features = {}

with tab1:
    cols = st.columns(2)
    for i, col_name in enumerate(CATEGORICAL_ORDER):
        with cols[i % 2]:
            opts = options.get(col_name, [])
            default_idx = 0
            features[col_name] = st.selectbox(
                labels.get(col_name, col_name),
                opts,
                index=default_idx,
                key=f"cat_{col_name}",
            )

with tab2:
    cols = st.columns(2)
    for i, (col_name, (default, min_v, max_v)) in enumerate(NUMERIC_DEFAULTS.items()):
        with cols[i % 2]:
            step = 0.01 if isinstance(default, float) else 1
            features[col_name] = st.number_input(
                labels.get(col_name, col_name),
                min_value=min_v,
                max_value=max_v,
                value=default,
                step=step,
                key=f"num_{col_name}",
            )

st.markdown("---")

col_btn, col_reset = st.columns([1, 3])
with col_btn:
    predict_clicked = st.button("开始预测", type="primary", use_container_width=True)

if predict_clicked:
    try:
        result = predict(features)
        st.markdown("---")
        st.subheader("预测结果")

        if result["subscribe"]:
            st.success("预测结果：**会认购** 定期存款产品")
        else:
            st.warning("预测结果：**不会认购** 定期存款产品")

        prob = result["probability"]
        st.progress(prob, text=f"认购概率: {prob * 100:.1f}%")

        c1, c2, c3 = st.columns(3)
        c1.metric("认购概率", f"{prob * 100:.1f}%")
        c2.metric("置信度", result["confidence"])
        c3.metric("预测标签", "是" if result["subscribe"] else "否")

    except Exception as e:
        st.error(f"预测失败: {e}")
