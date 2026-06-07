import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from app.models.data_loader import TARGET_COLUMN, get_feature_labels

CATEGORICAL_FEATURES = [
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

NUMERIC_FEATURES = [
    "age",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]


def _label(feature: str) -> str:
    labels = get_feature_labels()
    return labels.get(feature, feature)


def plot_subscribe_pie(df: pd.DataFrame) -> Figure:
    counts = df[TARGET_COLUMN].value_counts().reset_index()
    counts.columns = ["subscribe", "count"]
    counts["label"] = counts["subscribe"].map({"yes": "认购", "no": "未认购"})
    fig = px.pie(
        counts,
        values="count",
        names="label",
        title="认购分布",
        color_discrete_sequence=["#2ca02c", "#d62728"],
    )
    fig.update_traces(textinfo="percent+value")
    return fig


def plot_categorical_subscribe_rate(df: pd.DataFrame, feature: str) -> Figure:
    rates = (
        df.groupby(feature)[TARGET_COLUMN].apply(lambda x: (x == "yes").mean() * 100).reset_index()
    )
    rates.columns = [feature, "subscribe_rate"]
    rates = rates.sort_values("subscribe_rate", ascending=True)
    fig = px.bar(
        rates,
        x="subscribe_rate",
        y=feature,
        orientation="h",
        title=f"{_label(feature)} — 认购率(%)",
        text_auto=".1f",
    )
    fig.update_layout(xaxis_title="认购率(%)", yaxis_title=_label(feature))
    return fig


def plot_categorical_count(df: pd.DataFrame, feature: str) -> Figure:
    counts = df[feature].value_counts().reset_index()
    counts.columns = [feature, "count"]
    fig = px.bar(
        counts, x=feature, y="count", title=f"{_label(feature)} — 数量分布", text_auto=True
    )
    fig.update_layout(xaxis_title=_label(feature), yaxis_title="数量")
    return fig


def plot_numeric_histogram(df: pd.DataFrame, feature: str) -> Figure:
    fig = px.histogram(
        df, x=feature, nbins=30, title=f"{_label(feature)} — 分布直方图", marginal="box"
    )
    fig.update_layout(xaxis_title=_label(feature), yaxis_title="频次")
    return fig


def plot_numeric_box_by_subscribe(df: pd.DataFrame, feature: str) -> Figure:
    fig = px.box(df, x=TARGET_COLUMN, y=feature, title=f"{_label(feature)} — 按认购分组")
    fig.update_layout(xaxis_title="认购", yaxis_title=_label(feature))
    return fig


def plot_correlation_heatmap(df: pd.DataFrame) -> Figure:
    corr = df[NUMERIC_FEATURES].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        title="数值特征相关性热力图",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )
    fig.update_layout(height=600)
    return fig


def plot_education_subscribe_heatmap(df: pd.DataFrame) -> Figure:
    ct = pd.crosstab(df["education"], df[TARGET_COLUMN])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    yes_pct = ct_pct.get("yes", pd.Series(dtype=float)).sort_values(ascending=False)
    fig = px.bar(
        x=yes_pct.values,
        y=yes_pct.index,
        orientation="h",
        title="教育水平 — 认购率(%)",
        text_auto=".1f",
    )
    fig.update_layout(xaxis_title="认购率(%)", yaxis_title="教育水平")
    return fig


def plot_month_subscribe_rate(df: pd.DataFrame) -> Figure:
    month_order = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    rates = (
        df.groupby("month")[TARGET_COLUMN].apply(lambda x: (x == "yes").mean() * 100).reset_index()
    )
    rates.columns = ["month", "subscribe_rate"]
    rates["month"] = pd.Categorical(rates["month"], categories=month_order, ordered=True)
    rates = rates.sort_values("month")
    fig = px.line(rates, x="month", y="subscribe_rate", markers=True, title="各月份 — 认购率趋势")
    fig.update_layout(xaxis_title="月份", yaxis_title="认购率(%)")
    return fig
