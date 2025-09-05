"""
基本チャートコンポーネント
- line_chart: 折れ線グラフ
- bar_chart: 棒グラフ  
- area_chart: エリアチャート
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
import plotly.graph_objects as go
import plotly.express as px


class BasicCharts:
    """基本チャートコンポーネント"""
    
    @staticmethod
    def line_chart(
        data: pd.DataFrame,
        x: Optional[str] = None,
        y: Optional[Union[str, List[str]]] = None,
        title: str = "Line Chart",
        use_container_width: bool = True,
        height: Optional[int] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        折れ線グラフを表示
        
        Args:
            data: 表示するDataFrame
            x: X軸のカラム名
            y: Y軸のカラム名（複数可）
            title: チャートのタイトル
            use_container_width: コンテナ幅を使用
            height: チャートの高さ
            color: 色分けに使用するカラム名
            **kwargs: その他のStreamlit line_chartオプション
        """
        with st.container():
            st.subheader(title)
            
            # データの検証
            if data.empty:
                st.warning("データがありません")
                return
            
            # Streamlitネイティブのline_chartを使用（シンプルケース）
            if x is None and y is None and color is None:
                st.line_chart(
                    data,
                    use_container_width=use_container_width,
                    height=height,
                    **kwargs
                )
            else:
                # Plotlyを使用（詳細な制御が必要な場合）
                fig = go.Figure()
                
                if x is None:
                    x_data = data.index
                else:
                    x_data = data[x]
                
                if y is None:
                    y_cols = data.select_dtypes(include=[np.number]).columns.tolist()
                elif isinstance(y, str):
                    y_cols = [y]
                else:
                    y_cols = y
                
                # 色分けがある場合
                if color and color in data.columns:
                    for value in data[color].unique():
                        mask = data[color] == value
                        for col in y_cols:
                            fig.add_trace(go.Scatter(
                                x=x_data[mask],
                                y=data[mask][col],
                                mode='lines',
                                name=f"{col} ({value})"
                            ))
                else:
                    # 各Y軸カラムに対してトレースを追加
                    for col in y_cols:
                        fig.add_trace(go.Scatter(
                            x=x_data,
                            y=data[col],
                            mode='lines',
                            name=col
                        ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=x if x else "Index",
                    yaxis_title="Value",
                    height=height,
                    hovermode='x unified'
                )
                
                st.plotly_chart(
                    fig,
                    use_container_width=use_container_width,
                    **kwargs
                )
    
    @staticmethod
    def bar_chart(
        data: pd.DataFrame,
        x: Optional[str] = None,
        y: Optional[Union[str, List[str]]] = None,
        title: str = "Bar Chart",
        orientation: str = "vertical",
        use_container_width: bool = True,
        height: Optional[int] = None,
        color: Optional[str] = None,
        stacked: bool = False,
        **kwargs
    ) -> None:
        """
        棒グラフを表示
        
        Args:
            data: 表示するDataFrame
            x: X軸のカラム名
            y: Y軸のカラム名（複数可）
            title: チャートのタイトル
            orientation: "vertical" または "horizontal"
            use_container_width: コンテナ幅を使用
            height: チャートの高さ
            color: 色分けに使用するカラム名
            stacked: 積み上げ棒グラフ
            **kwargs: その他のオプション
        """
        with st.container():
            st.subheader(title)
            
            # データの検証
            if data.empty:
                st.warning("データがありません")
                return
            
            # Streamlitネイティブのbar_chartを使用（シンプルケース）
            if x is None and y is None and not stacked and orientation == "vertical":
                st.bar_chart(
                    data,
                    use_container_width=use_container_width,
                    height=height,
                    **kwargs
                )
            else:
                # Plotlyを使用（詳細な制御が必要な場合）
                fig = go.Figure()
                
                if x is None:
                    x_data = data.index
                else:
                    x_data = data[x]
                
                if y is None:
                    y_cols = data.select_dtypes(include=[np.number]).columns.tolist()
                elif isinstance(y, str):
                    y_cols = [y]
                else:
                    y_cols = y
                
                # 積み上げモードの設定
                barmode = 'stack' if stacked else 'group'
                
                # 水平/垂直の設定
                if orientation == "horizontal":
                    for col in y_cols:
                        fig.add_trace(go.Bar(
                            x=data[col],
                            y=x_data,
                            name=col,
                            orientation='h'
                        ))
                else:
                    for col in y_cols:
                        fig.add_trace(go.Bar(
                            x=x_data,
                            y=data[col],
                            name=col
                        ))
                
                fig.update_layout(
                    title=title,
                    barmode=barmode,
                    xaxis_title=x if x else "Index",
                    yaxis_title="Value",
                    height=height,
                    hovermode='x unified'
                )
                
                st.plotly_chart(
                    fig,
                    use_container_width=use_container_width,
                    **kwargs
                )
    
    @staticmethod
    def area_chart(
        data: pd.DataFrame,
        x: Optional[str] = None,
        y: Optional[Union[str, List[str]]] = None,
        title: str = "Area Chart",
        use_container_width: bool = True,
        height: Optional[int] = None,
        stacked: bool = True,
        **kwargs
    ) -> None:
        """
        エリアチャートを表示
        
        Args:
            data: 表示するDataFrame
            x: X軸のカラム名
            y: Y軸のカラム名（複数可）
            title: チャートのタイトル
            use_container_width: コンテナ幅を使用
            height: チャートの高さ
            stacked: 積み上げエリアチャート
            **kwargs: その他のオプション
        """
        with st.container():
            st.subheader(title)
            
            # データの検証
            if data.empty:
                st.warning("データがありません")
                return
            
            # Streamlitネイティブのarea_chartを使用（シンプルケース）
            if x is None and y is None:
                st.area_chart(
                    data,
                    use_container_width=use_container_width,
                    height=height,
                    **kwargs
                )
            else:
                # Plotlyを使用（詳細な制御が必要な場合）
                fig = go.Figure()
                
                if x is None:
                    x_data = data.index
                else:
                    x_data = data[x]
                
                if y is None:
                    y_cols = data.select_dtypes(include=[np.number]).columns.tolist()
                elif isinstance(y, str):
                    y_cols = [y]
                else:
                    y_cols = y
                
                # スタックグループの設定
                stackgroup = 'one' if stacked else None
                
                # 各Y軸カラムに対してトレースを追加
                for col in y_cols:
                    fig.add_trace(go.Scatter(
                        x=x_data,
                        y=data[col],
                        mode='lines',
                        name=col,
                        fill='tonexty' if stacked else 'tozeroy',
                        stackgroup=stackgroup
                    ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=x if x else "Index",
                    yaxis_title="Value",
                    height=height,
                    hovermode='x unified'
                )
                
                st.plotly_chart(
                    fig,
                    use_container_width=use_container_width,
                    **kwargs
                )


class ChartDataGenerator:
    """チャート用のサンプルデータ生成"""
    
    @staticmethod
    def generate_time_series(
        days: int = 30,
        columns: List[str] = ["Sales", "Revenue", "Cost"],
        seed: Optional[int] = None
    ) -> pd.DataFrame:
        """
        時系列データの生成
        
        Args:
            days: 日数
            columns: カラム名のリスト
            seed: 乱数シード
        
        Returns:
            時系列DataFrame
        """
        if seed is not None:
            np.random.seed(seed)
        
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=days-1),
            end=datetime.now(),
            freq='D'
        )
        
        data = {}
        for col in columns:
            # トレンドとランダム成分を組み合わせる
            trend = np.linspace(100, 150, days)
            noise = np.random.normal(0, 10, days)
            seasonal = 10 * np.sin(np.arange(days) * 2 * np.pi / 7)
            data[col] = trend + noise + seasonal + np.random.randint(-5, 5)
            data[col] = np.maximum(data[col], 0)  # 負の値を避ける
        
        return pd.DataFrame(data, index=dates)
    
    @staticmethod
    def generate_categorical_data(
        categories: List[str] = ["A", "B", "C", "D"],
        metrics: List[str] = ["Value1", "Value2"],
        seed: Optional[int] = None
    ) -> pd.DataFrame:
        """
        カテゴリデータの生成
        
        Args:
            categories: カテゴリのリスト
            metrics: メトリクスのリスト
            seed: 乱数シード
        
        Returns:
            カテゴリDataFrame
        """
        if seed is not None:
            np.random.seed(seed)
        
        data = {"Category": categories}
        for metric in metrics:
            data[metric] = np.random.randint(10, 100, len(categories))
        
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_realtime_data(
        columns: List[str] = ["Sensor1", "Sensor2"],
        points: int = 100
    ) -> pd.DataFrame:
        """
        リアルタイム風データの生成
        
        Args:
            columns: カラム名のリスト
            points: データポイント数
        
        Returns:
            リアルタイムDataFrame
        """
        # 現在時刻から過去に向かってpoints個の時刻を生成
        now = datetime.now()
        timestamps = [now - timedelta(seconds=i) for i in range(points-1, -1, -1)]
        
        data = {}
        for col in columns:
            # ランダムウォーク（points個の値を生成）
            values = np.cumsum(np.random.randn(points)) + 50
            data[col] = values
        
        return pd.DataFrame(data, index=pd.DatetimeIndex(timestamps))


def render_basic_charts_demo():
    """基本チャートのデモ"""
    st.header("📊 Basic Charts Demo")
    
    # タブで各チャートタイプを表示
    tabs = st.tabs(["Line Chart", "Bar Chart", "Area Chart", "Real-time Demo"])
    
    charts = BasicCharts()
    generator = ChartDataGenerator()
    
    # Line Chart Demo
    with tabs[0]:
        st.markdown("### Line Chart Examples")
        
        col1, col2 = st.columns(2)
        with col1:
            # シンプルな折れ線グラフ
            data = generator.generate_time_series(days=30, columns=["Sales"])
            charts.line_chart(data, title="Simple Line Chart")
        
        with col2:
            # 複数系列の折れ線グラフ
            data = generator.generate_time_series(days=30, columns=["Sales", "Revenue", "Cost"])
            charts.line_chart(data, title="Multiple Series Line Chart")
        
        # カスタマイズオプション
        st.markdown("### Customization Options")
        with st.expander("Line Chart Options"):
            height = st.slider("Chart Height", 200, 600, 400)
            show_grid = st.checkbox("Show Grid", value=True)
            
            data = generator.generate_time_series(days=60)
            charts.line_chart(
                data,
                title="Customized Line Chart",
                height=height
            )
    
    # Bar Chart Demo
    with tabs[1]:
        st.markdown("### Bar Chart Examples")
        
        col1, col2 = st.columns(2)
        with col1:
            # 垂直棒グラフ
            data = generator.generate_categorical_data(
                categories=["Q1", "Q2", "Q3", "Q4"],
                metrics=["Sales", "Revenue"]
            )
            charts.bar_chart(
                data,
                x="Category",
                y=["Sales", "Revenue"],
                title="Vertical Bar Chart"
            )
        
        with col2:
            # 積み上げ棒グラフ
            charts.bar_chart(
                data,
                x="Category",
                y=["Sales", "Revenue"],
                title="Stacked Bar Chart",
                stacked=True
            )
        
        # 水平棒グラフ
        st.markdown("### Horizontal Bar Chart")
        data = generator.generate_categorical_data(
            categories=["Product A", "Product B", "Product C", "Product D", "Product E"],
            metrics=["2023", "2024"]
        )
        charts.bar_chart(
            data,
            x="Category",
            y=["2023", "2024"],
            title="Horizontal Bar Chart",
            orientation="horizontal",
            height=300
        )
    
    # Area Chart Demo
    with tabs[2]:
        st.markdown("### Area Chart Examples")
        
        col1, col2 = st.columns(2)
        with col1:
            # シンプルなエリアチャート
            data = generator.generate_time_series(days=30, columns=["Volume"])
            charts.area_chart(data, title="Simple Area Chart")
        
        with col2:
            # 積み上げエリアチャート
            data = generator.generate_time_series(
                days=30,
                columns=["Desktop", "Mobile", "Tablet"]
            )
            charts.area_chart(
                data,
                title="Stacked Area Chart",
                stacked=True
            )
        
        # 非積み上げエリアチャート
        st.markdown("### Non-Stacked Area Chart")
        data = generator.generate_time_series(days=60, columns=["A", "B", "C"])
        charts.area_chart(
            data,
            title="Overlapping Area Chart",
            stacked=False,
            height=400
        )
    
    # Real-time Demo
    with tabs[3]:
        st.markdown("### Real-time Data Visualization")
        
        # リアルタイム更新のシミュレーション
        update_interval = st.slider(
            "Update Interval (seconds)",
            min_value=1,
            max_value=10,
            value=2
        )
        
        chart_type = st.radio(
            "Chart Type",
            ["Line", "Area", "Bar"],
            horizontal=True
        )
        
        # データ生成とプロット
        placeholder = st.empty()
        
        if st.button("Start Real-time Demo", type="primary"):
            try:
                for i in range(10):  # 10回更新
                    data = generator.generate_realtime_data(
                        columns=["Sensor1", "Sensor2", "Sensor3"],
                        points=50
                    )
                    
                    with placeholder.container():
                        if chart_type == "Line":
                            charts.line_chart(
                                data,
                                title=f"Real-time Line Chart - {datetime.now().strftime('%H:%M:%S')}"
                            )
                        elif chart_type == "Area":
                            charts.area_chart(
                                data,
                                title=f"Real-time Area Chart - {datetime.now().strftime('%H:%M:%S')}"
                            )
                        else:
                            # 最新の10データポイントを棒グラフで表示
                            bar_data = data.tail(10).T
                            charts.bar_chart(
                                bar_data,
                                title=f"Real-time Bar Chart - {datetime.now().strftime('%H:%M:%S')}"
                            )
                    
                    # 最後の更新でない場合のみsleep
                    if i < 9:
                        import time
                        time.sleep(update_interval)
                
                st.success("Real-time demo completed!")
                
            except Exception as e:
                st.error(f"Error during real-time demo: {str(e)}")
                st.info("Please try again.")
        
        # 統計情報の表示
        with st.expander("Data Statistics"):
            sample_data = generator.generate_realtime_data()
            st.write("Sample Data Shape:", sample_data.shape)
            st.write("Data Summary:")
            st.dataframe(sample_data.describe())


if __name__ == "__main__":
    # スタンドアロンテスト
    st.set_page_config(page_title="Basic Charts Demo", layout="wide")
    render_basic_charts_demo()