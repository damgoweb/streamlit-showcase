"""
データ表示コンポーネント
dataframe, table, metric, json の実装
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from typing import Any, Dict, Optional, Union, List
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.base_component import BaseComponent
from utils.code_display import code_display
from utils.sample_data import sample_data


class DataFrameComponent(BaseComponent):
    """st.dataframe コンポーネント"""
    
    def __init__(self):
        super().__init__("dataframe", "data_widgets")
        self.metadata = {
            'id': 'dataframe',
            'name': 'st.dataframe',
            'category': 'data_widgets',
            'description': 'インタラクティブなデータフレーム表示。ソート、フィルタ、列の幅調整が可能。',
            'parameters': [
                {
                    'name': 'data',
                    'type': 'DataFrame/dict/list',
                    'required': True,
                    'description': '表示するデータ'
                },
                {
                    'name': 'use_container_width',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'コンテナの幅に合わせる'
                },
                {
                    'name': 'hide_index',
                    'type': 'bool',
                    'required': False,
                    'default': None,
                    'description': 'インデックス列を非表示'
                },
                {
                    'name': 'column_order',
                    'type': 'list',
                    'required': False,
                    'default': None,
                    'description': '列の表示順序'
                },
                {
                    'name': 'column_config',
                    'type': 'dict',
                    'required': False,
                    'default': None,
                    'description': '列の設定（型、書式など）'
                }
            ],
            'tips': [
                'ユーザーがソート、フィルタ、検索可能',
                '大量データでも高速表示',
                'column_configで詳細なカスタマイズが可能',
                'CSVダウンロード機能付き',
                'セル選択とコピーが可能'
            ],
            'related': ['table', 'data_editor', 'columns'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rows = st.slider("行数", 5, 100, 20, key="df_rows")
                cols_type = st.selectbox(
                    "列タイプ",
                    ["基本", "数値のみ", "混合型", "時系列"],
                    key="df_cols"
                )
                
            with col2:
                use_container = st.checkbox(
                    "コンテナ幅を使用",
                    value=True,
                    key="df_container"
                )
                hide_index = st.checkbox(
                    "インデックスを非表示",
                    value=False,
                    key="df_hide_idx"
                )
                
            with col3:
                highlight = st.checkbox(
                    "ハイライト表示",
                    value=False,
                    key="df_highlight"
                )
                show_config = st.checkbox(
                    "列設定を使用",
                    value=False,
                    key="df_config"
                )
        
        # サンプルデータ生成
        if cols_type == "基本":
            df = sample_data.generate_dataframe(rows=rows)
        elif cols_type == "数値のみ":
            df = pd.DataFrame(
                np.random.randn(rows, 5),
                columns=[f'Col_{i}' for i in range(1, 6)]
            )
        elif cols_type == "混合型":
            df = pd.DataFrame({
                'ID': range(1, rows + 1),
                'Name': [f'User_{i}' for i in range(1, rows + 1)],
                'Score': np.random.randint(60, 100, rows),
                'Rate': np.random.uniform(0.5, 1.5, rows),
                'Active': np.random.choice([True, False], rows)
            })
        else:  # 時系列
            df = sample_data.generate_time_series(days=rows)
        
        # ハイライト設定
        if highlight and cols_type in ["数値のみ", "混合型"]:
            df_styled = df.style.highlight_max(axis=0, color='lightgreen')
            df_styled = df_styled.highlight_min(axis=0, color='lightcoral')
        else:
            df_styled = df
        
        # 列設定
        column_config = None
        if show_config and cols_type == "混合型":
            column_config = {
                "ID": st.column_config.NumberColumn(
                    "ユーザーID",
                    help="一意の識別子",
                    format="%d"
                ),
                "Name": st.column_config.TextColumn(
                    "ユーザー名",
                    help="登録名",
                    max_chars=50
                ),
                "Score": st.column_config.ProgressColumn(
                    "スコア",
                    help="パフォーマンススコア",
                    format="%d",
                    min_value=0,
                    max_value=100
                ),
                "Rate": st.column_config.NumberColumn(
                    "レート",
                    help="成長率",
                    format="%.2f"
                ),
                "Active": st.column_config.CheckboxColumn(
                    "アクティブ",
                    help="アクティブ状態",
                    default=False
                )
            }
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # DataFrameの表示
        st.dataframe(
            df_styled,
            use_container_width=use_container,
            hide_index=hide_index,
            column_config=column_config
        )
        
        # 統計情報
        with st.expander("📊 データ統計"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("行数", len(df))
            with col2:
                st.metric("列数", len(df.columns))
            with col3:
                st.metric("データ型", len(df.dtypes.unique()))
            
            st.write("**基本統計:**")
            st.dataframe(df.describe())
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="dataframe_demo_code")
        
        return df
    
    def get_code(self, level: str = "basic") -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st
import pandas as pd

# DataFrameの作成
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['Tokyo', 'Osaka', 'Kyoto']
})

# DataFrameの表示
st.dataframe(df)

# コンテナ幅を使用
st.dataframe(df, use_container_width=True)

# インデックスを非表示
st.dataframe(df, hide_index=True)"""
        
        elif level == "advanced":
            return """import streamlit as st
import pandas as pd
import numpy as np

# 大規模データフレーム
df = pd.DataFrame(
    np.random.randn(100, 5),
    columns=['A', 'B', 'C', 'D', 'E']
)

# スタイル付きDataFrame
df_styled = df.style.highlight_max(axis=0, color='lightgreen')
st.dataframe(df_styled)

# 列設定のカスタマイズ
st.dataframe(
    df,
    column_config={
        "A": st.column_config.ProgressColumn(
            "進捗",
            help="パフォーマンス指標",
            format="%.2f",
            min_value=-3,
            max_value=3,
        ),
        "B": st.column_config.NumberColumn(
            "値",
            help="測定値",
            format="%.3f"
        )
    },
    hide_index=True
)"""
        
        else:  # full
            return """import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_interactive_dataframe():
    \"\"\"インタラクティブなデータフレーム表示\"\"\"
    
    st.title("📊 データフレームビューアー")
    
    # データ生成オプション
    col1, col2, col3 = st.columns(3)
    with col1:
        data_type = st.selectbox(
            "データタイプ",
            ["売上データ", "ユーザー分析", "時系列データ"]
        )
    with col2:
        rows = st.slider("行数", 10, 1000, 100)
    with col3:
        show_stats = st.checkbox("統計を表示", value=True)
    
    # データ生成
    if data_type == "売上データ":
        df = pd.DataFrame({
            '日付': pd.date_range('2024-01-01', periods=rows, freq='D'),
            '商品ID': [f'P{str(i%20).zfill(3)}' for i in range(rows)],
            '売上': np.random.randint(1000, 10000, rows),
            '数量': np.random.randint(1, 100, rows),
            '利益率': np.random.uniform(0.1, 0.4, rows),
            'カテゴリ': np.random.choice(['電子機器', '衣類', '食品', '書籍'], rows)
        })
        
        # 列設定
        column_config = {
            "売上": st.column_config.NumberColumn(
                "売上高",
                help="日次売上高",
                format="¥%d",
            ),
            "利益率": st.column_config.ProgressColumn(
                "利益率",
                help="売上に対する利益の割合",
                format="%.1%%",
                min_value=0,
                max_value=1,
            ),
            "日付": st.column_config.DateColumn(
                "販売日",
                format="YYYY-MM-DD",
            )
        }
        
    elif data_type == "ユーザー分析":
        df = pd.DataFrame({
            'ユーザーID': [f'U{str(i).zfill(5)}' for i in range(rows)],
            '登録日': pd.date_range(end='2024-01-01', periods=rows),
            'アクティブ': np.random.choice([True, False], rows, p=[0.7, 0.3]),
            'セッション数': np.random.poisson(5, rows),
            'コンバージョン率': np.random.beta(2, 5, rows),
            'LTV': np.random.lognormal(8, 1.5, rows)
        })
        
        column_config = {
            "アクティブ": st.column_config.CheckboxColumn(
                "アクティブ状態",
                default=False,
            ),
            "コンバージョン率": st.column_config.ProgressColumn(
                "CVR",
                format="%.2%%",
                min_value=0,
                max_value=1,
            ),
            "LTV": st.column_config.NumberColumn(
                "生涯価値",
                format="¥%.0f",
            )
        }
        
    else:  # 時系列データ
        dates = pd.date_range('2024-01-01', periods=rows, freq='H')
        df = pd.DataFrame({
            'タイムスタンプ': dates,
            '温度': 20 + 10 * np.sin(np.arange(rows) * 2 * np.pi / 24) + np.random.randn(rows),
            '湿度': 60 + 20 * np.sin(np.arange(rows) * 2 * np.pi / 24 + np.pi/4) + np.random.randn(rows) * 5,
            'CPU使用率': np.clip(50 + np.random.randn(rows) * 20, 0, 100),
            'メモリ使用率': np.clip(40 + np.random.randn(rows) * 15, 0, 100),
            'ステータス': np.random.choice(['正常', '警告', 'エラー'], rows, p=[0.8, 0.15, 0.05])
        })
        
        column_config = {
            "温度": st.column_config.NumberColumn(
                "温度(℃)",
                format="%.1f",
            ),
            "湿度": st.column_config.ProgressColumn(
                "湿度(%)",
                format="%.0f",
                min_value=0,
                max_value=100,
            ),
            "CPU使用率": st.column_config.ProgressColumn(
                "CPU(%)",
                format="%.0f",
                min_value=0,
                max_value=100,
            ),
            "メモリ使用率": st.column_config.ProgressColumn(
                "メモリ(%)",
                format="%.0f",
                min_value=0,
                max_value=100,
            )
        }
    
    # データフレーム表示
    st.subheader("📋 データビュー")
    
    # フィルタリング
    with st.expander("🔍 フィルタ設定"):
        filter_cols = st.multiselect(
            "表示する列",
            options=df.columns.tolist(),
            default=df.columns.tolist()
        )
        df_filtered = df[filter_cols] if filter_cols else df
    else:
        df_filtered = df
    
    # メイン表示
    st.dataframe(
        df_filtered,
        column_config=column_config,
        use_container_width=True,
        hide_index=True
    )
    
    # 統計情報
    if show_stats:
        st.subheader("📊 統計情報")
        
        # 基本統計
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("レコード数", len(df))
        with col2:
            st.metric("列数", len(df.columns))
        with col3:
            null_count = df.isnull().sum().sum()
            st.metric("欠損値", null_count)
        with col4:
            memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024
            st.metric("メモリ使用量", f"{memory_usage:.2f} MB")
        
        # 詳細統計
        st.write("**数値列の統計:**")
        st.dataframe(df_filtered.describe())
    
    # エクスポート
    st.subheader("💾 データエクスポート")
    col1, col2 = st.columns(2)
    with col1:
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            "📥 CSVダウンロード",
            csv,
            "data.csv",
            "text/csv"
        )
    with col2:
        json_str = df_filtered.to_json(orient='records')
        st.download_button(
            "📥 JSONダウンロード",
            json_str,
            "data.json",
            "application/json"
        )

def main():
    create_interactive_dataframe()

if __name__ == "__main__":
    main()"""


class TableComponent(BaseComponent):
    """st.table コンポーネント"""
    
    def __init__(self):
        super().__init__("table", "data_widgets")
        self.metadata = {
            'id': 'table',
            'name': 'st.table',
            'category': 'data_widgets',
            'description': '静的なテーブル表示。全データを一度に表示し、スクロール不可。',
            'parameters': [
                {
                    'name': 'data',
                    'type': 'DataFrame/dict/list',
                    'required': True,
                    'description': '表示するデータ'
                }
            ],
            'tips': [
                '小さなデータセット向け',
                '全データが一度に表示される',
                'インタラクティブ機能なし',
                'プリント向けの表示',
                'dataframeより軽量'
            ],
            'related': ['dataframe', 'data_editor', 'write'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            data_type = st.selectbox(
                "データタイプ",
                ["シンプル", "統計表", "マトリックス"],
                key="table_type"
            )
        
        # データ生成
        if data_type == "シンプル":
            data = pd.DataFrame({
                '項目': ['りんご', 'バナナ', 'オレンジ', 'ぶどう'],
                '価格': [150, 100, 120, 300],
                '在庫': [50, 100, 80, 30]
            })
        elif data_type == "統計表":
            data = pd.DataFrame({
                '指標': ['平均', '中央値', '最大値', '最小値', '標準偏差'],
                'A列': [10.5, 10.0, 15.0, 5.0, 3.2],
                'B列': [20.3, 19.5, 30.0, 10.0, 5.6],
                'C列': [15.7, 15.0, 25.0, 8.0, 4.1]
            })
        else:  # マトリックス
            data = pd.DataFrame(
                np.random.randint(0, 100, size=(5, 5)),
                columns=[f'Col{i}' for i in range(1, 6)],
                index=[f'Row{i}' for i in range(1, 6)]
            )
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        st.write("**st.table() - 静的テーブル:**")
        st.table(data)
        
        st.write("**比較: st.dataframe() - インタラクティブ:**")
        st.dataframe(data)
        
        # 違いの説明
        with st.expander("📖 table vs dataframe の違い"):
            comparison = pd.DataFrame({
                '機能': ['表示形式', 'ソート', '検索', 'スクロール', 'パフォーマンス', '用途'],
                'st.table': ['静的', '不可', '不可', '不可', '軽量', '小規模データ'],
                'st.dataframe': ['インタラクティブ', '可能', '可能', '可能', '大規模対応', '大規模データ']
            })
            st.table(comparison)
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="table_demo_code")
        
        return data
    
    def get_code(self, level: str = "basic") -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st
import pandas as pd

# データの準備
data = pd.DataFrame({
    '商品': ['商品A', '商品B', '商品C'],
    '価格': [1000, 2000, 1500],
    '在庫': [50, 30, 40]
})

# 静的テーブルとして表示
st.table(data)"""
        else:
            return """import streamlit as st
import pandas as pd
import numpy as np

# 統計サマリーテーブル
stats = pd.DataFrame({
    '統計量': ['件数', '平均', '標準偏差', '最小', '25%', '50%', '75%', '最大'],
    '値': [100, 50.5, 15.2, 10, 35, 50, 65, 90]
})

st.write("### 📊 統計サマリー")
st.table(stats)

# 相関行列
corr_matrix = pd.DataFrame(
    np.random.rand(4, 4),
    columns=['A', 'B', 'C', 'D'],
    index=['A', 'B', 'C', 'D']
)

st.write("### 🔗 相関行列")
st.table(corr_matrix.round(2))"""


class MetricComponent(BaseComponent):
    """st.metric コンポーネント"""
    
    def __init__(self):
        super().__init__("metric", "data_widgets")
        self.metadata = {
            'id': 'metric',
            'name': 'st.metric',
            'category': 'data_widgets',
            'description': 'KPIやメトリクスを大きく見やすく表示。変化量（デルタ）も表示可能。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'description': 'メトリクスのラベル'
                },
                {
                    'name': 'value',
                    'type': 'int/float/str',
                    'required': True,
                    'description': '表示する値'
                },
                {
                    'name': 'delta',
                    'type': 'int/float/str',
                    'required': False,
                    'default': None,
                    'description': '変化量'
                },
                {
                    'name': 'delta_color',
                    'type': 'str',
                    'required': False,
                    'default': 'normal',
                    'description': 'デルタの色設定'
                }
            ],
            'tips': [
                'KPIダッシュボード向け',
                'deltaで前期比などを表示',
                'delta_color="inverse"で色を反転',
                '複数並べてダッシュボード作成',
                'アニメーション効果付き'
            ],
            'related': ['columns', 'container', 'number_input'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                demo_type = st.selectbox(
                    "デモタイプ",
                    ["売上", "ユーザー", "パフォーマンス", "カスタム"],
                    key="metric_type"
                )
                show_delta = st.checkbox(
                    "デルタ表示",
                    value=True,
                    key="metric_delta"
                )
                
            with col2:
                delta_color = st.radio(
                    "デルタカラー",
                    ["normal", "inverse", "off"],
                    key="metric_color"
                )
                animate = st.checkbox(
                    "アニメーション",
                    value=True,
                    key="metric_animate"
                )
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        if demo_type == "売上":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    label="総売上",
                    value="¥2.5M",
                    delta="12%" if show_delta else None,
                    delta_color=delta_color
                )
            with col2:
                st.metric(
                    label="注文数",
                    value="1,234",
                    delta="+89" if show_delta else None,
                    delta_color=delta_color
                )
            with col3:
                st.metric(
                    label="平均単価",
                    value="¥2,028",
                    delta="-5%" if show_delta else None,
                    delta_color=delta_color
                )
            with col4:
                st.metric(
                    label="コンバージョン率",
                    value="3.2%",
                    delta="+0.3%" if show_delta else None,
                    delta_color=delta_color
                )
                
        elif demo_type == "ユーザー":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("アクティブユーザー", "8,234", "+12.3%")
            with col2:
                st.metric("新規登録", "523", "+48")
            with col3:
                st.metric("継続率", "68%", "-2%", delta_color="inverse")
                
        elif demo_type == "パフォーマンス":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("CPU使用率", "45%", "+5%", delta_color="inverse")
            with col2:
                st.metric("メモリ", "2.3GB", "-0.2GB")
            with col3:
                st.metric("レスポンス", "120ms", "-30ms")
            with col4:
                st.metric("エラー率", "0.02%", "-0.01%")
                
        else:  # カスタム
            label = st.text_input("ラベル", "カスタムメトリクス")
            value = st.text_input("値", "100")
            delta = st.text_input("デルタ", "+10") if show_delta else None
            
            st.metric(label, value, delta, delta_color=delta_color)
        
        # 複雑な例
        with st.expander("🎯 高度な使用例"):
            st.write("**リアルタイムダッシュボード風:**")
            
            # ヘッダー
            st.markdown("### 📊 リアルタイムメトリクス")
            
            # メトリクスグリッド
            metrics = sample_data.generate_metrics_data()
            cols = st.columns(len(metrics))
            
            for col, (key, data) in zip(cols, metrics.items()):
                with col:
                    st.metric(
                        label=data["label"],
                        value=data["value"],
                        delta=data["delta"],
                        delta_color=data["delta_color"]
                    )
            
            # プログレスバー付き
            st.markdown("### 📈 目標達成率")
            col1, col2 = st.columns([3, 1])
            with col1:
                progress = 0.73
                st.progress(progress)
            with col2:
                st.metric("達成率", f"{progress*100:.0f}%", "+5%")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="metric_demo_code")
        
        return None
    
    def get_code(self, level: str = "basic") -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st

# 基本的なメトリクス
st.metric(label="温度", value="25.5°C", delta="1.2°C")

# デルタなし
st.metric(label="総売上", value="¥1,234,567")

# 複数のメトリクス
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("売上", "¥1.2M", "+15%")
    
with col2:
    st.metric("ユーザー", "823", "+12")
    
with col3:
    st.metric("評価", "4.8", "-0.1", delta_color="inverse")"""
        
        else:
            return """import streamlit as st
import random
import time

def create_kpi_dashboard():
    \"\"\"KPIダッシュボード\"\"\"
    
    st.title("📊 KPIダッシュボード")
    
    # 自動更新の設定
    placeholder = st.empty()
    
    while True:
        with placeholder.container():
            # リアルタイムメトリクス
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                revenue = random.uniform(1000000, 2000000)
                revenue_delta = random.uniform(-10, 20)
                st.metric(
                    "収益",
                    f"¥{revenue:,.0f}",
                    f"{revenue_delta:+.1f}%",
                    delta_color="normal"
                )
            
            with col2:
                users = random.randint(5000, 10000)
                users_delta = random.randint(-100, 300)
                st.metric(
                    "アクティブユーザー",
                    f"{users:,}",
                    f"{users_delta:+d}",
                    delta_color="normal"
                )
            
            with col3:
                conversion = random.uniform(2, 5)
                conversion_delta = random.uniform(-0.5, 0.8)
                st.metric(
                    "コンバージョン率",
                    f"{conversion:.2f}%",
                    f"{conversion_delta:+.2f}%",
                    delta_color="normal"
                )
            
            with col4:
                satisfaction = random.uniform(4.0, 5.0)
                satisfaction_delta = random.uniform(-0.2, 0.3)
                st.metric(
                    "満足度",
                    f"{satisfaction:.1f}/5.0",
                    f"{satisfaction_delta:+.1f}",
                    delta_color="normal" if satisfaction_delta > 0 else "inverse"
                )
            
            # パフォーマンスメトリクス
            st.subheader("⚡ システムパフォーマンス")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cpu = random.uniform(20, 80)
                st.metric(
                    "CPU使用率",
                    f"{cpu:.1f}%",
                    f"{random.uniform(-5, 5):+.1f}%",
                    delta_color="inverse"  # 低い方が良い
                )
            
            with col2:
                memory = random.uniform(1, 4)
                st.metric(
                    "メモリ使用量",
                    f"{memory:.1f}GB",
                    f"{random.uniform(-0.5, 0.5):+.2f}GB",
                    delta_color="inverse"
                )
            
            with col3:
                response = random.uniform(50, 200)
                st.metric(
                    "応答時間",
                    f"{response:.0f}ms",
                    f"{random.uniform(-20, 20):+.0f}ms",
                    delta_color="inverse"
                )
        
        time.sleep(2)  # 2秒ごとに更新

# 使用例
create_kpi_dashboard()"""


class JsonComponent(BaseComponent):
    """st.json コンポーネント"""
    
    def __init__(self):
        super().__init__("json", "data_widgets")
        self.metadata = {
            'id': 'json',
            'name': 'st.json',
            'category': 'data_widgets',
            'description': 'JSON形式のデータを整形して表示。展開/折りたたみ可能なツリー表示。',
            'parameters': [
                {
                    'name': 'body',
                    'type': 'dict/str',
                    'required': True,
                    'description': '表示するJSONデータ'
                },
                {
                    'name': 'expanded',
                    'type': 'bool/int',
                    'required': False,
                    'default': True,
                    'description': '展開レベル'
                }
            ],
            'tips': [
                'ツリー形式で表示',
                '展開/折りたたみ可能',
                'シンタックスハイライト付き',
                'APIレスポンスの表示に便利',
                'ネストした構造も見やすく表示'
            ],
            'related': ['write', 'code', 'dataframe'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            json_type = st.selectbox(
                "JSONタイプ",
                ["API レスポンス", "設定ファイル", "ネスト構造", "配列"],
                key="json_type"
            )
            expanded = st.checkbox(
                "展開表示",
                value=True,
                key="json_expanded"
            )
        
        # サンプルJSON生成
        if json_type == "API レスポンス":
            json_data = {
                "status": "success",
                "code": 200,
                "data": {
                    "user": {
                        "id": 12345,
                        "name": "John Doe",
                        "email": "john@example.com",
                        "verified": True
                    },
                    "tokens": {
                        "access": "eyJhbGciOiJIUzI1NiIs...",
                        "refresh": "eyJhbGciOiJIUzI1NiIs...",
                        "expires_in": 3600
                    }
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        elif json_type == "設定ファイル":
            json_data = {
                "app": {
                    "name": "MyApp",
                    "version": "1.2.3",
                    "debug": False
                },
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "mydb",
                    "pool_size": 10
                },
                "features": {
                    "authentication": True,
                    "notifications": True,
                    "analytics": False
                }
            }
        elif json_type == "ネスト構造":
            json_data = sample_data.generate_json_data()
        else:  # 配列
            json_data = [
                {"id": i, "value": f"item_{i}", "active": i % 2 == 0}
                for i in range(5)
            ]
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        st.json(json_data, expanded=expanded)
        
        # 他の表示方法との比較
        with st.expander("🔄 他の表示方法との比較"):
            tab1, tab2, tab3 = st.tabs(["st.json", "st.write", "st.code"])
            
            with tab1:
                st.write("**st.json() - 専用ビューア:**")
                st.json(json_data)
            
            with tab2:
                st.write("**st.write() - 汎用表示:**")
                st.write(json_data)
            
            with tab3:
                st.write("**st.code() - コード表示:**")
                st.code(json.dumps(json_data, indent=2), language="json")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="json_demo_code")
        
        return json_data
    
    def get_code(self, level: str = "basic") -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st

# JSONデータの表示
data = {
    "name": "Streamlit",
    "type": "Framework",
    "language": "Python",
    "features": ["Fast", "Easy", "Interactive"]
}

st.json(data)

# 展開レベルの制御
st.json(data, expanded=False)"""
        else:
            return """import streamlit as st
import json
import requests

# APIレスポンスの表示
def display_api_response():
    st.header("API Response Viewer")
    
    # 擬似的なAPIレスポンス
    response = {
        "meta": {
            "request_id": "abc123",
            "timestamp": "2024-01-01T12:00:00Z",
            "version": "v1"
        },
        "data": {
            "items": [
                {
                    "id": 1,
                    "name": "Item 1",
                    "attributes": {
                        "color": "red",
                        "size": "large"
                    }
                },
                {
                    "id": 2,
                    "name": "Item 2",
                    "attributes": {
                        "color": "blue",
                        "size": "medium"
                    }
                }
            ],
            "total": 2,
            "page": 1
        },
        "errors": []
    }
    
    # JSON表示
    st.json(response)
    
    # JSONの一部を抽出
    if st.checkbox("データ部分のみ表示"):
        st.json(response["data"])
    
    # ダウンロード機能
    json_str = json.dumps(response, indent=2)
    st.download_button(
        "JSONファイルをダウンロード",
        json_str,
        "response.json",
        "application/json"
    )

display_api_response()"""


# コンポーネントのエクスポート
__all__ = [
    'DataFrameComponent',
    'TableComponent', 
    'MetricComponent',
    'JsonComponent'
]