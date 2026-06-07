import plotly.graph_objects as go

from app.models.visualizer import (
    CATEGORICAL_FEATURES,
    plot_categorical_count,
    plot_categorical_subscribe_rate,
    plot_correlation_heatmap,
    plot_education_subscribe_heatmap,
    plot_month_subscribe_rate,
    plot_numeric_box_by_subscribe,
    plot_numeric_histogram,
    plot_subscribe_pie,
)


class TestSubscribePie:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_subscribe_pie(sample_df_for_viz)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_has_title(self, sample_df_for_viz):
        fig = plot_subscribe_pie(sample_df_for_viz)
        assert "认购分布" in fig.layout.title.text


class TestCategoricalSubscribeRate:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_categorical_subscribe_rate(sample_df_for_viz, "job")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_all_categorical_features_work(self, sample_df_for_viz):
        for feature in CATEGORICAL_FEATURES:
            fig = plot_categorical_subscribe_rate(sample_df_for_viz, feature)
            assert isinstance(fig, go.Figure)


class TestCategoricalCount:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_categorical_count(sample_df_for_viz, "marital")
        assert isinstance(fig, go.Figure)


class TestNumericHistogram:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_numeric_histogram(sample_df_for_viz, "age")
        assert isinstance(fig, go.Figure)


class TestNumericBoxBySubscribe:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_numeric_box_by_subscribe(sample_df_for_viz, "duration")
        assert isinstance(fig, go.Figure)


class TestCorrelationHeatmap:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_correlation_heatmap(sample_df_for_viz)
        assert isinstance(fig, go.Figure)


class TestEducationHeatmap:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_education_subscribe_heatmap(sample_df_for_viz)
        assert isinstance(fig, go.Figure)


class TestMonthSubscribeRate:
    def test_returns_figure(self, sample_df_for_viz):
        fig = plot_month_subscribe_rate(sample_df_for_viz)
        assert isinstance(fig, go.Figure)
