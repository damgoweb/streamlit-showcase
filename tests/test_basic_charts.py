"""
基本チャートコンポーネントのテスト
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# プロジェクトルートをパスに追加
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

# Streamlitをモック化
sys.modules['streamlit'] = MagicMock()

from components.chart_widgets.basic_charts import BasicCharts, ChartDataGenerator


class TestBasicCharts:
    """BasicChartsクラスのテスト"""
    
    @pytest.fixture
    def sample_data(self):
        """サンプルデータの生成"""
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        return pd.DataFrame({
            'Date': dates,
            'Value1': np.random.randint(10, 100, 10),
            'Value2': np.random.randint(20, 80, 10),
            'Category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
        })
    
    @patch('components.chart_widgets.basic_charts.st')
    def test_line_chart_with_empty_data(self, mock_st):
        """空のデータでline_chartが正常に処理されることを確認"""
        charts = BasicCharts()
        empty_df = pd.DataFrame()
        
        # モックの設定
        mock_st.container.return_value.__enter__ = Mock(return_value=mock_st)
        mock_st.container.return_value.__exit__ = Mock(return_value=None)
        
        # エラーが発生しないことを確認
        charts.line_chart(empty_df, title="Empty Data Test")
        
        # 警告が表示されることを確認
        mock_st.warning.assert_called_once_with("データがありません")
    
    @patch('components.chart_widgets.basic_charts.st')
    def test_bar_chart_with_data(self, mock_st, sample_data):
        """データを含むbar_chartのテスト"""
        charts = BasicCharts()
        
        # モックの設定
        mock_st.container.return_value.__enter__ = Mock(return_value=mock_st)
        mock_st.container.return_value.__exit__ = Mock(return_value=None)
        
        # エラーが発生しないことを確認
        charts.bar_chart(
            sample_data,
            x='Category',
            y=['Value1', 'Value2'],
            title="Test Bar Chart"
        )
        
        # サブヘッダーが呼ばれたことを確認
        mock_st.subheader.assert_called_once_with("Test Bar Chart")
    
    @patch('components.chart_widgets.basic_charts.st')
    def test_area_chart_with_data(self, mock_st, sample_data):
        """データを含むarea_chartのテスト"""
        charts = BasicCharts()
        
        # モックの設定
        mock_st.container.return_value.__enter__ = Mock(return_value=mock_st)
        mock_st.container.return_value.__exit__ = Mock(return_value=None)
        
        # エラーが発生しないことを確認
        charts.area_chart(
            sample_data[['Value1', 'Value2']],
            title="Test Area Chart"
        )
        
        # サブヘッダーが呼ばれたことを確認
        mock_st.subheader.assert_called_once_with("Test Area Chart")


class TestChartDataGenerator:
    """ChartDataGeneratorクラスのテスト"""
    
    def test_generate_time_series(self):
        """時系列データ生成のテスト"""
        generator = ChartDataGenerator()
        
        # デフォルトパラメータでのテスト
        data = generator.generate_time_series()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 30  # デフォルトは30日
        assert list(data.columns) == ["Sales", "Revenue", "Cost"]
        
        # カスタムパラメータでのテスト
        data = generator.generate_time_series(
            days=7,
            columns=["Test1", "Test2"],
            seed=42
        )
        
        assert len(data) == 7
        assert list(data.columns) == ["Test1", "Test2"]
        
        # 再現性の確認（同じシード）- インデックスを除外して比較
        data2 = generator.generate_time_series(
            days=7,
            columns=["Test1", "Test2"],
            seed=42
        )
        
        # 値のみを比較（インデックスの時刻は微妙に異なる可能性がある）
        pd.testing.assert_frame_equal(
            data.reset_index(drop=True), 
            data2.reset_index(drop=True)
        )
    
    def test_generate_categorical_data(self):
        """カテゴリデータ生成のテスト"""
        generator = ChartDataGenerator()
        
        # デフォルトパラメータでのテスト
        data = generator.generate_categorical_data()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 4  # デフォルトは4カテゴリ
        assert "Category" in data.columns
        assert "Value1" in data.columns
        assert "Value2" in data.columns
        
        # カスタムパラメータでのテスト
        data = generator.generate_categorical_data(
            categories=["X", "Y", "Z"],
            metrics=["Metric1", "Metric2", "Metric3"],
            seed=42
        )
        
        assert len(data) == 3
        assert list(data["Category"]) == ["X", "Y", "Z"]
        assert all(metric in data.columns for metric in ["Metric1", "Metric2", "Metric3"])
    
    def test_generate_realtime_data(self):
        """リアルタイムデータ生成のテスト"""
        generator = ChartDataGenerator()
        
        # デフォルトパラメータでのテスト
        data = generator.generate_realtime_data()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 100  # デフォルトは100ポイント
        assert list(data.columns) == ["Sensor1", "Sensor2"]
        
        # インデックスがDatetimeIndexであることを確認
        assert isinstance(data.index, pd.DatetimeIndex)
        
        # カスタムパラメータでのテスト
        data = generator.generate_realtime_data(
            columns=["A", "B", "C"],
            points=50
        )
        
        assert len(data) == 50
        assert list(data.columns) == ["A", "B", "C"]
        
        # インデックスと値の長さが一致することを確認（重要）
        for col in data.columns:
            assert len(data[col]) == len(data.index), f"Column {col} length mismatch with index"
        
        # さまざまなpoints値でテスト
        for points in [1, 10, 30, 100, 500]:
            data = generator.generate_realtime_data(points=points)
            assert len(data) == points, f"Failed for points={points}"
            assert len(data.index) == points, f"Index length mismatch for points={points}"
            # インデックスと各列の長さが一致
            for col in data.columns:
                assert len(data[col]) == points, f"Column {col} length mismatch for points={points}"
    
    def test_data_value_ranges(self):
        """生成されるデータの値の範囲をテスト"""
        generator = ChartDataGenerator()
        
        # 時系列データの値が妥当な範囲内にあることを確認
        data = generator.generate_time_series(days=100, seed=42)
        
        # すべての値が非負であることを確認
        assert (data >= 0).all().all()
        
        # カテゴリデータの値が指定範囲内にあることを確認
        cat_data = generator.generate_categorical_data(seed=42)
        
        # Value1とValue2が10-100の範囲内にあることを確認
        assert (cat_data[["Value1", "Value2"]] >= 10).all().all()
        assert (cat_data[["Value1", "Value2"]] < 100).all().all()


class TestChartIntegration:
    """チャートコンポーネントの統合テスト"""
    
    @patch('components.chart_widgets.basic_charts.st')
    def test_charts_with_generated_data(self, mock_st):
        """生成データを使用したチャートのテスト"""
        generator = ChartDataGenerator()
        charts = BasicCharts()
        
        # モックの設定
        mock_st.container.return_value.__enter__ = Mock(return_value=mock_st)
        mock_st.container.return_value.__exit__ = Mock(return_value=None)
        
        # 時系列データでline_chartをテスト
        time_data = generator.generate_time_series(days=7)
        charts.line_chart(time_data, title="Time Series Test")
        
        # カテゴリデータでbar_chartをテスト
        cat_data = generator.generate_categorical_data()
        charts.bar_chart(
            cat_data,
            x="Category",
            y=["Value1", "Value2"],
            title="Category Test"
        )
        
        # リアルタイムデータでarea_chartをテスト
        realtime_data = generator.generate_realtime_data(points=20)
        charts.area_chart(realtime_data, title="Realtime Test")
        
        # 各チャートメソッドが呼ばれたことを確認
        assert mock_st.subheader.call_count >= 3
    
    @patch('components.chart_widgets.basic_charts.st')
    @patch('components.chart_widgets.basic_charts.go')
    def test_chart_options(self, mock_go, mock_st):
        """チャートオプションのテスト"""
        generator = ChartDataGenerator()
        charts = BasicCharts()
        data = generator.generate_time_series(days=10)
        
        # モックの設定
        mock_st.container.return_value.__enter__ = Mock(return_value=mock_st)
        mock_st.container.return_value.__exit__ = Mock(return_value=None)
        mock_fig = MagicMock()
        mock_go.Figure.return_value = mock_fig
        
        # 各種オプションでエラーが発生しないことを確認
        test_cases = [
            # Line chart options
            {"method": "line_chart", "params": {"height": 300}},
            {"method": "line_chart", "params": {"use_container_width": False}},
            
            # Bar chart options  
            {"method": "bar_chart", "params": {"orientation": "horizontal"}},
            {"method": "bar_chart", "params": {"stacked": True}},
            
            # Area chart options
            {"method": "area_chart", "params": {"stacked": False}},
            {"method": "area_chart", "params": {"height": 500}},
        ]
        
        for test in test_cases:
            method = getattr(charts, test["method"])
            # エラーが発生しないことを確認
            method(data, title="Option Test", **test["params"])


if __name__ == "__main__":
    # テストの実行
    pytest.main([__file__, "-v"])