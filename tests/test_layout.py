"""
レイアウトコンポーネントのテスト
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import pandas as pd
import numpy as np

# プロジェクトルートをパスに追加
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

# Streamlitをモック化
sys.modules['streamlit'] = MagicMock()

from components.layout_widgets.layout import LayoutComponents, LayoutPatterns


class TestLayoutComponents:
    """LayoutComponentsクラスのテスト"""
    
    @patch('components.layout_widgets.layout.st')
    def test_columns_demo_basic(self, mock_st):
        """基本的なカラムレイアウトのテスト"""
        # モックの設定
        mock_cols = [MagicMock() for _ in range(3)]
        mock_st.columns.return_value = mock_cols
        
        # 各カラムのコンテキストマネージャーをモック
        for col in mock_cols:
            col.__enter__ = Mock(return_value=mock_st)
            col.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.columns_demo(num_columns=3, gap="medium", example_type="basic")
        
        # 検証
        mock_st.columns.assert_called_once_with(3, gap="medium")
        mock_st.subheader.assert_called_once_with("📏 3 Columns Layout")
        # 各カラムでメトリクスが表示されることを確認
        assert mock_st.metric.call_count >= 3
    
    @patch('components.layout_widgets.layout.st')
    def test_columns_demo_weighted(self, mock_st):
        """重み付きカラムレイアウトのテスト"""
        # モックの設定
        mock_cols = [MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        
        for col in mock_cols:
            col.__enter__ = Mock(return_value=mock_st)
            col.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.columns_demo(num_columns=2, gap="large", example_type="weighted")
        
        # 検証
        mock_st.columns.assert_called_once_with([2, 1], gap="large")
    
    @patch('components.layout_widgets.layout.st')
    def test_container_demo_basic(self, mock_st):
        """基本的なコンテナのテスト"""
        # モックの設定
        mock_container = MagicMock()
        mock_st.container.return_value = mock_container
        mock_container.__enter__ = Mock(return_value=mock_st)
        mock_container.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.container_demo(example_type="basic", show_border=True)
        
        # 検証
        mock_st.container.assert_called_with(border=True)
        mock_st.subheader.assert_called_once_with("📦 Container Layout")
    
    @patch('components.layout_widgets.layout.st')
    def test_container_demo_dynamic(self, mock_st):
        """動的コンテナのテスト"""
        # モックの設定
        mock_container = MagicMock()
        mock_st.container.return_value = mock_container
        mock_container.__enter__ = Mock(return_value=mock_st)
        mock_container.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.container_demo(example_type="dynamic", show_border=False)
        
        # 検証
        mock_st.container.assert_called_with(border=False)
        # 動的コンテンツの追加を確認
        mock_st.success.assert_called_once_with("Dynamic content insertion")
    
    @patch('components.layout_widgets.layout.st')
    def test_expander_demo_basic(self, mock_st):
        """基本的なエクスパンダーのテスト"""
        # モックの設定
        mock_expander = MagicMock()
        mock_st.expander.return_value = mock_expander
        mock_expander.__enter__ = Mock(return_value=mock_st)
        mock_expander.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.expander_demo(example_type="basic", expanded_by_default=True)
        
        # 検証
        mock_st.expander.assert_called_with("Click to expand", expanded=True)
        mock_st.subheader.assert_called_with("📂 Expander Layout")
    
    @patch('components.layout_widgets.layout.st')
    def test_expander_demo_multiple(self, mock_st):
        """複数エクスパンダーのテスト"""
        # モックの設定
        mock_expander = MagicMock()
        mock_st.expander.return_value = mock_expander
        mock_expander.__enter__ = Mock(return_value=mock_st)
        mock_expander.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.expander_demo(example_type="multiple", expanded_by_default=False)
        
        # 検証
        # 3つのエクスパンダーが作成されることを確認
        assert mock_st.expander.call_count >= 3
    
    @patch('components.layout_widgets.layout.st')
    def test_tabs_demo_basic(self, mock_st):
        """基本的なタブのテスト"""
        # モックの設定
        mock_tabs = [MagicMock() for _ in range(3)]
        mock_st.tabs.return_value = mock_tabs
        
        for tab in mock_tabs:
            tab.__enter__ = Mock(return_value=mock_st)
            tab.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.tabs_demo(example_type="basic", num_tabs=3)
        
        # 検証
        mock_st.tabs.assert_called_once_with(['Tab 1', 'Tab 2', 'Tab 3'])
        mock_st.subheader.assert_called_with("📑 Tabs Layout")
    
    @patch('components.layout_widgets.layout.st')
    def test_tabs_demo_icons(self, mock_st):
        """アイコン付きタブのテスト"""
        # モックの設定
        mock_tabs = [MagicMock() for _ in range(4)]
        mock_st.tabs.return_value = mock_tabs
        
        for tab in mock_tabs:
            tab.__enter__ = Mock(return_value=mock_st)
            tab.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.tabs_demo(example_type="icons", num_tabs=3)
        
        # 検証
        mock_st.tabs.assert_called_once_with(["📊 Data", "📈 Charts", "🎯 Metrics", "⚙️ Settings"])


class TestLayoutPatterns:
    """LayoutPatternsクラスのテスト"""
    
    @patch('components.layout_widgets.layout.st')
    def test_dashboard_layout(self, mock_st):
        """ダッシュボードレイアウトパターンのテスト"""
        # モックの設定
        mock_cols = [MagicMock() for _ in range(4)]
        mock_st.columns.return_value = mock_cols
        
        for col in mock_cols:
            col.__enter__ = Mock(return_value=mock_st)
            col.__exit__ = Mock(return_value=None)
        
        mock_tabs = [MagicMock() for _ in range(3)]
        mock_st.tabs.return_value = mock_tabs
        
        for tab in mock_tabs:
            tab.__enter__ = Mock(return_value=mock_st)
            tab.__exit__ = Mock(return_value=None)
        
        # テスト実行
        patterns = LayoutPatterns()
        patterns.dashboard_layout()
        
        # 検証
        mock_st.header.assert_called_with("📊 Dashboard Layout Pattern")
        # メトリクスが表示されることを確認
        assert mock_st.metric.call_count >= 4
        # タブが作成されることを確認
        assert mock_st.tabs.called
    
    @patch('components.layout_widgets.layout.st')
    def test_form_layout(self, mock_st):
        """フォームレイアウトパターンのテスト"""
        # モックの設定
        mock_container = MagicMock()
        mock_st.container.return_value = mock_container
        mock_container.__enter__ = Mock(return_value=mock_st)
        mock_container.__exit__ = Mock(return_value=None)
        
        mock_cols = [MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols
        
        for col in mock_cols:
            col.__enter__ = Mock(return_value=mock_st)
            col.__exit__ = Mock(return_value=None)
        
        mock_expander = MagicMock()
        mock_st.expander.return_value = mock_expander
        mock_expander.__enter__ = Mock(return_value=mock_st)
        mock_expander.__exit__ = Mock(return_value=None)
        
        # テスト実行
        patterns = LayoutPatterns()
        patterns.form_layout()
        
        # 検証
        mock_st.header.assert_called_with("📝 Form Layout Pattern")
        mock_st.container.assert_called_with(border=True)
        # フォーム要素が作成されることを確認
        assert mock_st.text_input.called
        assert mock_st.selectbox.called
        assert mock_st.checkbox.called
        assert mock_st.button.called
    
    @patch('components.layout_widgets.layout.st')
    def test_card_layout(self, mock_st):
        """カードレイアウトパターンのテスト"""
        # モックの設定
        mock_cols = [MagicMock() for _ in range(3)]
        mock_st.columns.return_value = mock_cols
        
        for col in mock_cols:
            col.__enter__ = Mock(return_value=mock_st)
            col.__exit__ = Mock(return_value=None)
        
        mock_container = MagicMock()
        mock_st.container.return_value = mock_container
        mock_container.__enter__ = Mock(return_value=mock_st)
        mock_container.__exit__ = Mock(return_value=None)
        
        mock_expander = MagicMock()
        mock_st.expander.return_value = mock_expander
        mock_expander.__enter__ = Mock(return_value=mock_st)
        mock_expander.__exit__ = Mock(return_value=None)
        
        # テスト実行
        patterns = LayoutPatterns()
        patterns.card_layout()
        
        # 検証
        mock_st.header.assert_called_with("🃏 Card Layout Pattern")
        mock_st.columns.assert_called_with(3, gap="medium")
        # カードコンテンツが作成されることを確認
        assert mock_st.subheader.call_count >= 3
        assert mock_st.image.called
        assert mock_st.button.called


class TestLayoutIntegration:
    """レイアウトコンポーネントの統合テスト"""
    
    @patch('components.layout_widgets.layout.st')
    def test_nested_layouts(self, mock_st):
        """ネストされたレイアウトのテスト"""
        # モックの設定
        mock_parent_cols = [MagicMock(), MagicMock()]
        mock_sub_cols = [MagicMock(), MagicMock()]
        
        # columns呼び出しを区別
        mock_st.columns.side_effect = [mock_parent_cols, mock_sub_cols, mock_sub_cols]
        
        for col in mock_parent_cols + mock_sub_cols:
            col.__enter__ = Mock(return_value=mock_st)
            col.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.columns_demo(num_columns=2, gap="medium", example_type="nested")
        
        # 検証
        # 親カラムと子カラムが作成されることを確認
        assert mock_st.columns.call_count >= 2
    
    @patch('components.layout_widgets.layout.st')
    def test_combined_layout_components(self, mock_st):
        """複数のレイアウトコンポーネントを組み合わせたテスト"""
        # モックの設定
        mock_container = MagicMock()
        mock_st.container.return_value = mock_container
        mock_container.__enter__ = Mock(return_value=mock_st)
        mock_container.__exit__ = Mock(return_value=None)
        
        mock_tabs = [MagicMock() for _ in range(3)]
        mock_st.tabs.return_value = mock_tabs
        
        for tab in mock_tabs:
            tab.__enter__ = Mock(return_value=mock_st)
            tab.__exit__ = Mock(return_value=None)
        
        mock_expander = MagicMock()
        mock_st.expander.return_value = mock_expander
        mock_expander.__enter__ = Mock(return_value=mock_st)
        mock_expander.__exit__ = Mock(return_value=None)
        
        # テスト実行
        layout = LayoutComponents()
        layout.tabs_demo(example_type="nested", num_tabs=3)
        
        # 検証
        # メインタブとサブタブが作成されることを確認
        assert mock_st.tabs.call_count >= 2


if __name__ == "__main__":
    # テストの実行
    pytest.main([__file__, "-v"])