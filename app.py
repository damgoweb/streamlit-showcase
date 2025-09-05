"""
Streamlit UIコンポーネントショーケース
メインアプリケーション - 完全修正版（チャート統合）
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import time
from pathlib import Path
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

# 設定のインポート
from config import (
    APP_NAME, 
    APP_VERSION, 
    APP_DESCRIPTION,
    COMPONENT_CATEGORIES,
    GITHUB_URL,
    SHOW_GITHUB_LINK
)

# ユーティリティのインポート
from utils.state_manager import state_manager
from utils.code_display import code_display
from utils.sample_data import sample_data
from utils.error_handler import error_handler

# ページ設定
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """セッション状態の初期化"""
    if 'initialized' not in st.session_state:
        state_manager._initialize_state()
        st.session_state.initialized = True

def render_sidebar():
    """サイドバーのレンダリング"""
    with st.sidebar:
        # ロゴとタイトル
        st.title(f"🎨 {APP_NAME}")
        st.caption(f"Version {APP_VERSION}")
        
        # GitHubリンク
        if SHOW_GITHUB_LINK:
            st.markdown(f"[📦 GitHub]({GITHUB_URL})")
        
        st.divider()
        
        # 検索ボックス
        search_query = st.text_input(
            "🔍 コンポーネントを検索",
            value=state_manager.get('search_query', ''),
            placeholder="例: text_input, button, chart"
        )
        state_manager.set('search_query', search_query)
        
        st.divider()
        
        # カテゴリ選択
        st.subheader("📚 カテゴリ")
        selected_category = st.selectbox(
            "カテゴリを選択",
            options=list(COMPONENT_CATEGORIES.keys()),
            format_func=lambda x: f"{COMPONENT_CATEGORIES[x]['icon']} {COMPONENT_CATEGORIES[x]['name']}",
            index=list(COMPONENT_CATEGORIES.keys()).index(
                state_manager.get('current_category', 'input_widgets')
            )
        )
        state_manager.set('current_category', selected_category)
        
        # お気に入り
        st.divider()
        st.subheader("⭐ お気に入り")
        
        # お気に入りリストを取得（最新の状態）
        favorites = state_manager.get_favorites()
        
        # お気に入り専用ビューボタン
        if favorites:
            if st.button("📌 お気に入りを表示", use_container_width=True):
                state_manager.set('view_mode', 'favorites')
                st.rerun()
        
        if favorites:
            for fav in favorites[:5]:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    # クリック可能なリンクとして表示
                    if st.button(f"📍 {fav}", key=f"goto_{fav}", use_container_width=True):
                        state_manager.set('current_component', fav)
                        state_manager.set('view_mode', 'component')
                        st.rerun()
                with col2:
                    # コードをコピー
                    if st.button("📋", key=f"copy_{fav}", help="コードをコピー"):
                        st.success("📋")
                with col3:
                    if st.button("❌", key=f"remove_fav_{fav}", help=f"{fav}を削除"):
                        state_manager.toggle_favorite(fav)
                        st.rerun()
            
            if len(favorites) > 5:
                st.caption(f"他 {len(favorites) - 5} 件...")
        else:
            st.caption("お気に入りはまだありません")
            st.caption("コンポーネントの⭐ボタンで追加")
        
        # 統計情報
        st.divider()
        st.subheader("📊 統計")
        
        # 人気のコンポーネント
        popular = state_manager.get_popular_components(3)
        if popular:
            st.caption("**人気のコンポーネント:**")
            for comp_id, count in popular:
                st.caption(f"• {comp_id} ({count}回)")
        
        # テーマ切り替え
        st.divider()
        theme = st.radio(
            "🎨 テーマ",
            ["Light", "Dark"],
            index=0 if state_manager.get('theme', 'light') == 'light' else 1
        )
        state_manager.set('theme', theme.lower())
        
        # フッター
        st.divider()
        st.caption(APP_DESCRIPTION)
        
        # デバッグ情報（開発時のみ）
        with st.expander("🔧 デバッグ"):
            if st.button("状態をリセット"):
                state_manager.reset_state()
                st.rerun()
            
            if st.button("エラーレポート"):
                error_handler.display_error_report()
            
            # 現在のお気に入りを表示
            st.caption("現在のお気に入り:")
            st.json(favorites)

def render_main_content():
    """メインコンテンツのレンダリング"""
    selected_category = state_manager.get('current_category', 'input_widgets')
    search_query = state_manager.get('search_query', '')
    view_mode = state_manager.get('view_mode', 'normal')
    current_component = state_manager.get('current_component', None)
    
    # お気に入りビューモード
    if view_mode == 'favorites':
        render_favorites_view()
        return
    
    # 特定コンポーネントビューモード
    if view_mode == 'component' and current_component:
        render_component_view(current_component)
        return
    
    # 通常のカテゴリビュー
    # カテゴリ情報
    category_info = COMPONENT_CATEGORIES.get(selected_category, {})
    
    # ヘッダー
    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
        st.title(f"{category_info.get('icon', '')} {category_info.get('name', '')}")
    with col2:
        if st.button("🔄", help="更新"):
            st.rerun()
    with col3:
        show_code = st.checkbox("</> Code", value=True, help="コードを表示")
        state_manager.set('show_code', show_code)
    
    st.markdown(category_info.get('description', ''))
    
    # 検索結果の表示
    if search_query:
        st.info(f"🔍 検索中: '{search_query}'")
        # TODO: 実際の検索ロジックを実装
    
    # タブ表示
    tab1, tab2, tab3, tab4 = st.tabs([
        "📺 デモ", "📊 サンプルデータ", "💻 コード例", "📚 ドキュメント"
    ])
    
    with tab1:
        render_demo_tab(selected_category)
    
    with tab2:
        render_sample_data_tab()
    
    with tab3:
        render_code_examples_tab(selected_category)
    
    with tab4:
        render_documentation_tab(selected_category)

def render_favorites_view():
    """お気に入り専用ビュー"""
    # ヘッダー
    col1, col2 = st.columns([10, 1])
    with col1:
        st.title("⭐ お気に入りコンポーネント")
    with col2:
        if st.button("✖️", help="閉じる"):
            state_manager.set('view_mode', 'normal')
            st.rerun()
    
    favorites = state_manager.get_favorites()
    
    if not favorites:
        st.info("お気に入りに登録されたコンポーネントはありません")
        if st.button("🏠 ホームに戻る"):
            state_manager.set('view_mode', 'normal')
            st.rerun()
        return
    
    # お気に入りをグリッド表示
    cols = st.columns(3)
    for idx, fav in enumerate(favorites):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"### 📌 {fav}")
                
                # コンポーネントのプレビュー（簡易版）
                if fav == "text_input":
                    preview = st.text_input("プレビュー", "サンプル", key=f"preview_{fav}")
                elif fav == "number_input":
                    preview = st.number_input("プレビュー", value=100, key=f"preview_{fav}")
                else:
                    st.info("プレビュー準備中")
                
                # アクションボタン
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("開く", key=f"open_{fav}"):
                        state_manager.set('current_component', fav)
                        state_manager.set('view_mode', 'component')
                        st.rerun()
                with col2:
                    if st.button("コード", key=f"code_{fav}"):
                        st.code(f"st.{fav}()")
                with col3:
                    if st.button("削除", key=f"del_{fav}"):
                        state_manager.toggle_favorite(fav)
                        st.rerun()
                
                st.divider()

def render_component_view(component_name: str):
    """特定コンポーネントの詳細ビュー"""
    # ヘッダー
    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
        st.title(f"🔍 {component_name}")
    with col2:
        if st.button("⭐", help="お気に入り切り替え"):
            state_manager.toggle_favorite(component_name)
            st.rerun()
    with col3:
        if st.button("✖️", help="閉じる"):
            state_manager.set('view_mode', 'normal')
            state_manager.set('current_component', None)
            st.rerun()
    
    # コンポーネント詳細
    tabs = st.tabs(["デモ", "コード", "ドキュメント", "例"])
    
    with tabs[0]:
        st.subheader("🎮 インタラクティブデモ")
        if component_name == "text_input":
            # パラメータ設定
            with st.expander("⚙️ パラメータ設定", expanded=True):
                label = st.text_input("ラベル", "テキストを入力")
                value = st.text_input("デフォルト値", "")
                max_chars = st.number_input("最大文字数", min_value=1, value=100)
                placeholder = st.text_input("プレースホルダー", "ここに入力...")
                help_text = st.text_input("ヘルプテキスト", "説明文")
            
            # デモ実行
            st.subheader("実行結果")
            result = st.text_input(
                label,
                value=value,
                max_chars=max_chars,
                placeholder=placeholder,
                help=help_text
            )
            st.success(f"入力値: {result}")
            
        elif component_name == "number_input":
            # パラメータ設定
            with st.expander("⚙️ パラメータ設定", expanded=True):
                label = st.text_input("ラベル", "数値を入力")
                min_value = st.number_input("最小値", value=0)
                max_value = st.number_input("最大値", value=100)
                value = st.number_input("デフォルト値", min_value=min_value, max_value=max_value, value=50)
                step = st.number_input("ステップ", value=1)
            
            # デモ実行
            st.subheader("実行結果")
            result = st.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                value=value,
                step=step
            )
            st.success(f"入力値: {result}")
    
    with tabs[1]:
        st.subheader("💻 コード生成")
        # コード生成ロジック
        if component_name == "text_input":
            code = """import streamlit as st

result = st.text_input(
    label="テキストを入力",
    value="",
    max_chars=100,
    placeholder="ここに入力...",
    help="説明文"
)

st.write(f"入力値: {result}")"""
        else:
            code = f"st.{component_name}()"
        
        st.code(code, language="python")
        if st.button("📋 コピー"):
            st.success("コピーしました！")
    
    with tabs[2]:
        st.subheader("📚 ドキュメント")
        st.markdown(f"""
        ### st.{component_name}
        
        このコンポーネントの詳細な説明...
        
        **パラメータ:**
        - `label`: 表示ラベル
        - `value`: デフォルト値
        - その他...
        """)
    
    with tabs[3]:
        st.subheader("💡 使用例")
        st.code(f"""
# 例1: 基本的な使い方
result = st.{component_name}("ラベル")

# 例2: オプション付き
result = st.{component_name}(
    "ラベル",
    value="デフォルト",
    help="ヘルプテキスト"
)
        """)

def render_demo_tab(category: str):
    """デモタブのレンダリング"""
    st.subheader("コンポーネントデモ")
    
    # カテゴリごとのデモ
    if category == "input_widgets":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Text Input")
            is_favorite_text = state_manager.is_favorite("text_input")
            fav_button_label = "⭐ お気に入りから削除" if is_favorite_text else "⭐ お気に入りに追加"
            
            if st.button(fav_button_label, key="fav_text_input"):
                if state_manager.toggle_favorite("text_input"):
                    st.success("✅ お気に入りに追加しました")
                else:
                    st.info("ℹ️ お気に入りから削除しました")
                st.rerun()
            
            text_value = st.text_input("名前を入力", "太郎")
            st.write(f"入力値: {text_value}")
            view_count = state_manager.increment_view_count("text_input")
            st.caption(f"閲覧回数: {view_count}")
        
        with col2:
            st.markdown("### Number Input")
            is_favorite_number = state_manager.is_favorite("number_input")
            fav_button_label = "⭐ お気に入りから削除" if is_favorite_number else "⭐ お気に入りに追加"
            
            if st.button(fav_button_label, key="fav_number_input"):
                if state_manager.toggle_favorite("number_input"):
                    st.success("✅ お気に入りに追加しました")
                else:
                    st.info("ℹ️ お気に入りから削除しました")
                st.rerun()
            
            number_value = st.number_input("年齢を入力", min_value=0, max_value=120, value=30)
            st.write(f"入力値: {number_value}")
            view_count = state_manager.increment_view_count("number_input")
            st.caption(f"閲覧回数: {view_count}")
    
    elif category == "display_widgets":
        # 表示ウィジェットのデモ
        tab1, tab2, tab3, tab4 = st.tabs(["テキスト表示", "見出し", "メッセージ", "コード"])
        
        with tab1:
            st.markdown("### st.write")
            st.write("これは **st.write** で表示されたテキストです。")
            st.write("複数の要素を一度に:", "文字列", 123, {"key": "value"})
            
            st.markdown("### st.text")
            st.text("これは st.text で表示された固定幅フォントのテキストです")
            
            st.markdown("### st.markdown")
            st.markdown("""
            **太字** と *イタリック*
            - リスト項目1
            - リスト項目2
            
            [リンク](https://streamlit.io)
            """)
        
        with tab2:
            st.title("st.title - タイトル")
            st.header("st.header - ヘッダー")
            st.subheader("st.subheader - サブヘッダー")
            st.caption("st.caption - キャプション（小さな説明文）")
        
        with tab3:
            st.success("✅ 成功メッセージ")
            st.info("ℹ️ 情報メッセージ")
            st.warning("⚠️ 警告メッセージ")
            st.error("❌ エラーメッセージ")
        
        with tab4:
            code_example = '''def hello():
    print("Hello, World!")
    return True'''
            st.code(code_example, language='python')
            
            st.markdown("### LaTeX数式")
            st.latex(r'''
            a^2 + b^2 = c^2
            ''')
    
    elif category == "data_widgets":
        # データ表示ウィジェットのデモ
        tab1, tab2, tab3, tab4 = st.tabs(["DataFrame", "Table", "Metric", "JSON"])
        
        with tab1:
            st.markdown("### st.dataframe")
            df = sample_data.generate_dataframe(rows=10)
            st.dataframe(df, use_container_width=True)
        
        with tab2:
            st.markdown("### st.table")
            table_data = pd.DataFrame({
                '項目': ['A', 'B', 'C'],
                '値': [100, 200, 150]
            })
            st.table(table_data)
        
        with tab3:
            st.markdown("### st.metric")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("売上", "¥1.2M", "+15%")
            with col2:
                st.metric("ユーザー", "1,234", "+89")
            with col3:
                st.metric("評価", "4.8/5.0", "+0.2")
        
        with tab4:
            st.markdown("### st.json")
            json_data = {
                "name": "Streamlit",
                "version": "1.33.0",
                "features": ["Fast", "Easy", "Interactive"]
            }
            st.json(json_data)
    
    elif category == "chart_widgets":
        # チャートウィジェットのデモ
        from components.chart_widgets.basic_charts import BasicCharts, ChartDataGenerator
        
        charts = BasicCharts()
        generator = ChartDataGenerator()
        
        tab1, tab2, tab3, tab4 = st.tabs(["Line Chart", "Bar Chart", "Area Chart", "Real-time"])
        
        with tab1:
            st.markdown("### Line Chart")
            
            col1, col2 = st.columns(2)
            with col1:
                # お気に入りボタン
                is_favorite = state_manager.is_favorite("line_chart")
                fav_label = "⭐ お気に入りから削除" if is_favorite else "⭐ お気に入りに追加"
                if st.button(fav_label, key="fav_line_chart"):
                    state_manager.toggle_favorite("line_chart")
                    st.rerun()
                
                # シンプルな折れ線グラフ
                data = generator.generate_time_series(days=30, columns=["売上"])
                st.line_chart(data)
                
                view_count = state_manager.increment_view_count("line_chart")
                st.caption(f"閲覧回数: {view_count}")
            
            with col2:
                # 複数系列の折れ線グラフ
                data = generator.generate_time_series(
                    days=30, 
                    columns=["売上", "利益", "コスト"]
                )
                st.line_chart(data)
                st.caption("複数系列の表示")
        
        with tab2:
            st.markdown("### Bar Chart")
            
            col1, col2 = st.columns(2)
            with col1:
                # お気に入りボタン
                is_favorite = state_manager.is_favorite("bar_chart")
                fav_label = "⭐ お気に入りから削除" if is_favorite else "⭐ お気に入りに追加"
                if st.button(fav_label, key="fav_bar_chart"):
                    state_manager.toggle_favorite("bar_chart")
                    st.rerun()
                
                # カテゴリデータの棒グラフ
                data = generator.generate_categorical_data(
                    categories=["Q1", "Q2", "Q3", "Q4"],
                    metrics=["売上", "利益"]
                )
                # Categoryを除く数値列のみを表示
                chart_data = data.set_index('Category')
                st.bar_chart(chart_data)
                
                view_count = state_manager.increment_view_count("bar_chart")
                st.caption(f"閲覧回数: {view_count}")
            
            with col2:
                # 別のカテゴリデータ
                data = generator.generate_categorical_data(
                    categories=["東京", "大阪", "名古屋", "福岡"],
                    metrics=["2023年", "2024年"]
                )
                chart_data = data.set_index('Category')
                st.bar_chart(chart_data)
                st.caption("地域別売上")
        
        with tab3:
            st.markdown("### Area Chart")
            
            col1, col2 = st.columns(2)
            with col1:
                # お気に入りボタン
                is_favorite = state_manager.is_favorite("area_chart")
                fav_label = "⭐ お気に入りから削除" if is_favorite else "⭐ お気に入りに追加"
                if st.button(fav_label, key="fav_area_chart"):
                    state_manager.toggle_favorite("area_chart")
                    st.rerun()
                
                # シンプルなエリアチャート
                data = generator.generate_time_series(days=30, columns=["アクセス数"])
                st.area_chart(data)
                
                view_count = state_manager.increment_view_count("area_chart")
                st.caption(f"閲覧回数: {view_count}")
            
            with col2:
                # 積み上げエリアチャート
                data = generator.generate_time_series(
                    days=30,
                    columns=["デスクトップ", "モバイル", "タブレット"]
                )
                st.area_chart(data)
                st.caption("デバイス別アクセス")
        
        with tab4:
            st.markdown("### Real-time Demo")
            
            # リアルタイム更新のデモ
            update_interval = st.slider(
                "更新間隔（秒）",
                min_value=1,
                max_value=5,
                value=2
            )
            
            chart_type = st.radio(
                "チャートタイプ",
                ["Line", "Area", "Bar"],
                horizontal=True
            )
            
            if st.button("リアルタイムデモを開始", type="primary"):
                placeholder = st.empty()
                
                for i in range(5):  # 5回更新
                    data = generator.generate_realtime_data(
                        columns=["センサー1", "センサー2"],
                        points=30
                    )
                    
                    with placeholder.container():
                        if chart_type == "Line":
                            st.line_chart(data)
                        elif chart_type == "Area":
                            st.area_chart(data)
                        else:  # Bar
                            # 最新の10データポイントを表示
                            st.bar_chart(data.tail(10))
                        
                        st.caption(f"更新 {i+1}/5 - {datetime.now().strftime('%H:%M:%S')}")
                    
                    time.sleep(update_interval)
                
                st.success("リアルタイムデモ完了！")
    
    elif category == "select_widgets":
        st.info("🚧 選択ウィジェットのデモは準備中です")
    
    else:
        st.info(f"🚧 {category} のデモは準備中です")

def render_sample_data_tab():
    """サンプルデータタブのレンダリング"""
    st.subheader("サンプルデータ生成")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        data_type = st.selectbox(
            "データタイプ",
            ["DataFrame", "時系列", "チャート", "JSON", "メトリクス"]
        )
        
        if data_type == "DataFrame":
            rows = st.slider("行数", 5, 100, 20)
            if st.button("生成", key="gen_df"):
                st.session_state.sample_df = sample_data.generate_dataframe(rows=rows)
        
        elif data_type == "時系列":
            days = st.slider("日数", 7, 90, 30)
            if st.button("生成", key="gen_ts"):
                st.session_state.sample_ts = sample_data.generate_time_series(days=days)
        
        elif data_type == "チャート":
            chart_type = st.selectbox("チャートタイプ", ["line", "bar", "scatter", "area"])
            points = st.slider("データポイント数", 10, 100, 50)
            if st.button("生成", key="gen_chart"):
                st.session_state.sample_chart = sample_data.generate_chart_data(
                    chart_type=chart_type, points=points
                )
                st.session_state.chart_type = chart_type
        
        elif data_type == "JSON":
            if st.button("生成", key="gen_json"):
                st.session_state.sample_json = sample_data.generate_json_data()
        
        elif data_type == "メトリクス":
            if st.button("生成", key="gen_metrics"):
                st.session_state.sample_metrics = sample_data.generate_metrics_data()
    
    with col2:
        if data_type == "DataFrame" and 'sample_df' in st.session_state:
            st.dataframe(st.session_state.sample_df)
            csv = st.session_state.sample_df.to_csv(index=False)
            st.download_button(
                "📥 CSVダウンロード",
                csv,
                "sample_data.csv",
                "text/csv"
            )
        
        elif data_type == "時系列" and 'sample_ts' in st.session_state:
            st.line_chart(st.session_state.sample_ts.set_index('Date')['Value'])
            st.dataframe(st.session_state.sample_ts.head())
        
        elif data_type == "チャート" and 'sample_chart' in st.session_state:
            df_chart = st.session_state.sample_chart
            chart_type = st.session_state.get('chart_type', 'line')
            
            # デバッグ情報を表示
            with st.expander("📊 データ構造を確認"):
                st.write("**列名:**", df_chart.columns.tolist())
                st.write("**データ型:**")
                st.write(df_chart.dtypes)
                st.write("**最初の5行:**")
                st.dataframe(df_chart.head())
            
            # チャートタイプに応じた表示
            try:
                if chart_type == "line":
                    # 複数列の折れ線グラフ
                    # 'x'列がある場合はそれをインデックスに
                    if 'x' in df_chart.columns:
                        # x以外の数値列を取得
                        y_cols = [col for col in df_chart.columns if col != 'x']
                        if y_cols:
                            chart_data = df_chart.set_index('x')[y_cols]
                            st.line_chart(chart_data)
                        else:
                            st.line_chart(df_chart)
                    else:
                        st.line_chart(df_chart)
                    
                elif chart_type == "bar":
                    # 棒グラフ
                    if 'Category' in df_chart.columns:
                        # カテゴリ列をインデックスに
                        value_cols = [col for col in df_chart.columns if col != 'Category']
                        if value_cols:
                            chart_data = df_chart.set_index('Category')[value_cols]
                            st.bar_chart(chart_data)
                        else:
                            st.bar_chart(df_chart)
                    else:
                        # そのまま表示
                        st.bar_chart(df_chart)
                    
                elif chart_type == "scatter":
                    # 散布図 - Streamlit 1.33.0以降で利用可能
                    if 'x' in df_chart.columns and 'y' in df_chart.columns:
                        # scatter_chartメソッドを使用
                        st.scatter_chart(
                            data=df_chart,
                            x='x',
                            y='y',
                            use_container_width=True
                        )
                    else:
                        # データをそのまま表示
                        st.write("散布図用のx, y列が見つかりません")
                        st.dataframe(df_chart)
                    
                elif chart_type == "area":
                    # エリアチャート
                    if 'Date' in df_chart.columns:
                        # Date列をインデックスに
                        date_cols = [col for col in df_chart.columns if col != 'Date']
                        if date_cols:
                            chart_data = df_chart.set_index('Date')[date_cols]
                            st.area_chart(chart_data)
                        else:
                            st.area_chart(df_chart)
                    elif 'x' in df_chart.columns:
                        # x列をインデックスに
                        area_cols = [col for col in df_chart.columns if col != 'x']
                        if area_cols:
                            chart_data = df_chart.set_index('x')[area_cols]
                            st.area_chart(chart_data)
                        else:
                            st.area_chart(df_chart)
                    else:
                        st.area_chart(df_chart)
                        
            except Exception as e:
                st.error(f"チャート表示エラー: {str(e)}")
                st.write("**生成されたデータ:**")
                st.dataframe(df_chart)
        
        elif data_type == "JSON" and 'sample_json' in st.session_state:
            st.json(st.session_state.sample_json)
        
        elif data_type == "メトリクス" and 'sample_metrics' in st.session_state:
            metrics = st.session_state.sample_metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("収益", metrics["revenue"]["value"], metrics["revenue"]["delta"])
            with col2:
                st.metric("ユーザー数", metrics["users"]["value"], metrics["users"]["delta"])
            with col3:
                st.metric("コンバージョン", metrics["conversion"]["value"], metrics["conversion"]["delta"])
            with col4:
                st.metric("満足度", metrics["satisfaction"]["value"], metrics["satisfaction"]["delta"])

def render_code_examples_tab(category: str):
    """コード例タブのレンダリング"""
    st.subheader("コード例")
    
    code_level = st.radio(
        "コードレベル",
        ["basic", "advanced", "full"],
        horizontal=True
    )
    
    if category == "input_widgets":
        params = {
            "label": "お名前を入力してください",
            "value": "デフォルト値",
            "max_chars": 100,
            "help": "最大100文字まで入力できます"
        }
        
        code = code_display.format_code(
            "st.text_input",
            params,
            level=code_level
        )
        code_display.display_with_copy(code, key=f"code_{category}_{code_level}")
    
    elif category == "display_widgets":
        # 表示ウィジェットのコード例
        if code_level == "basic":
            code = """import streamlit as st

# テキスト表示
st.write("Hello, Streamlit!")
st.text("固定幅フォントのテキスト")
st.markdown("**太字** と *イタリック*")

# 見出し
st.title("タイトル")
st.header("ヘッダー")
st.subheader("サブヘッダー")

# メッセージ
st.success("成功!")
st.info("情報")
st.warning("警告")
st.error("エラー")

# コード
st.code("print('Hello')", language="python")"""
        
        elif code_level == "advanced":
            code = '''import streamlit as st

# Markdownで複雑な表現
st.markdown("""
### 高度なMarkdown表示
- **太字**: `**text**`
- *イタリック*: `*text*`
- [リンク](https://streamlit.io)
- インラインコード: `code`

```python
# コードブロック
def greet(name):
    return f"Hello, {name}!"
```

| 列1 | 列2 |
|-----|-----|
| A   | B   |
""")

# LaTeX数式
st.latex(r"\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}")

# カスタムHTML（unsafe_allow_html=True）
st.markdown(
    "<p style=\\"color:red;\\">赤いテキスト</p>",
    unsafe_allow_html=True
)'''
        
        else:  # full
            code = '''import streamlit as st

def create_documentation():
    """ドキュメントページの作成"""
    
    # ページヘッダー
    st.title("📚 アプリケーションドキュメント")
    st.caption("最終更新: 2024-01-01")
    
    # ナビゲーション
    sections = ["概要", "インストール", "使い方", "API"]
    selected = st.radio("セクション", sections, horizontal=True)
    
    if selected == "概要":
        st.header("概要")
        st.write("""
        このアプリケーションは、Streamlitを使用した
        インタラクティブなデータ分析ツールです。
        
        **主な機能:**
        - データの可視化
        - リアルタイム分析
        - レポート生成
        """)
        
        # 重要な情報をハイライト
        st.info("ℹ️ Python 3.8以上が必要です")
        st.warning("⚠️ 大規模データセットの処理には時間がかかります")
    
    elif selected == "インストール":
        st.header("インストール方法")
        
        st.subheader("1. 依存関係のインストール")
        st.code("""
pip install streamlit pandas numpy plotly
        """, language="bash")
        
        st.subheader("2. アプリケーションの起動")
        st.code("""
streamlit run app.py
        """, language="bash")
        
        st.success("✅ インストール完了！")
    
    elif selected == "使い方":
        st.header("使い方")
        
        # タブで整理
        tab1, tab2, tab3 = st.tabs(["基本", "応用", "Tips"])
        
        with tab1:
            st.write("基本的な使い方...")
        with tab2:
            st.write("応用的な使い方...")
        with tab3:
            st.write("便利なTips...")
    
    else:  # API
        st.header("APIリファレンス")
        
        # エクスパンダーで整理
        with st.expander("関数一覧"):
            st.code("""
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    \"""データを処理する\"""
    pass

def generate_report(data: dict) -> str:
    \"""レポートを生成する\"""
    pass
            """, language="python")

if __name__ == "__main__":
    create_documentation()'''
        
        code_display.display_with_copy(code, key=f"code_{category}_{code_level}")
    
    elif category == "data_widgets":
        # データ表示ウィジェットのコード例
        if code_level == "basic":
            code = """import streamlit as st
import pandas as pd

# DataFrameの表示
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['Tokyo', 'Osaka', 'Kyoto']
})
st.dataframe(df)

# 静的テーブル
st.table(df)

# メトリクス
st.metric("売上", "¥1.2M", "+15%")

# JSON表示
data = {"name": "Streamlit", "version": "1.33.0"}
st.json(data)"""
        
        elif code_level == "advanced":
            code = """import streamlit as st
import pandas as pd
import numpy as np

# カスタマイズされたDataFrame
df = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])

st.dataframe(
    df.style.highlight_max(axis=0),
    column_config={
        "A": st.column_config.ProgressColumn(
            "進捗",
            format="%.2f",
            min_value=-3,
            max_value=3,
        ),
        "B": st.column_config.NumberColumn(
            "値",
            format="%.3f"
        )
    },
    hide_index=True,
    use_container_width=True
)

# 複数のメトリクス
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("売上", "¥2.5M", "12%")
with col2:
    st.metric("ユーザー", "1,234", "+89")
with col3:
    st.metric("評価", "4.8", "-0.1", delta_color="inverse")"""
        
        else:  # full
            code = '''import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_dashboard():
    """ダッシュボードの作成"""
    
    st.title("📊 ビジネスダッシュボード")
    
    # KPIメトリクス
    st.header("主要指標")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("売上", "¥12.5M", "+15.2%")
    with col2:
        st.metric("顧客数", "8,234", "+523")
    with col3:
        st.metric("コンバージョン", "3.2%", "+0.3%")
    with col4:
        st.metric("満足度", "4.8/5", "+0.1")
    
    # データテーブル
    st.header("売上データ")
    
    # サンプルデータ生成
    dates = pd.date_range(end=datetime.now(), periods=30)
    df = pd.DataFrame({
        "日付": dates,
        "売上": np.random.randint(80000, 150000, 30),
        "注文数": np.random.randint(50, 200, 30),
        "平均単価": np.random.randint(1500, 3000, 30)
    })
    
    # DataFrameの表示（スタイル付き）
    st.dataframe(
        df.style.format({
            "売上": "¥{:,.0f}",
            "平均単価": "¥{:,.0f}"
        }).background_gradient(subset=["売上"]),
        use_container_width=True
    )
    
    # 統計サマリー
    st.header("統計サマリー")
    st.table(df.describe().round(0))
    
    # JSON データ
    st.header("設定情報")
    config = {
        "更新頻度": "1時間ごと",
        "データソース": "売上管理システム",
        "最終更新": datetime.now().isoformat(),
        "ステータス": "正常"
    }
    st.json(config)

if __name__ == "__main__":
    create_dashboard()'''
        
        code_display.display_with_copy(code, key=f"code_{category}_{code_level}")
    
    elif category == "chart_widgets":
        # チャートウィジェットのコード例
        if code_level == "basic":
            code = """import streamlit as st
import pandas as pd
import numpy as np

# サンプルデータ生成
dates = pd.date_range('2024-01-01', periods=30)
data = pd.DataFrame({
    'Date': dates,
    'Value': np.random.randn(30).cumsum() + 100
})

# 折れ線グラフ
st.line_chart(data.set_index('Date'))

# 棒グラフ
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]
bar_data = pd.DataFrame({'Category': categories, 'Value': values})
st.bar_chart(bar_data.set_index('Category'))

# エリアチャート
area_data = pd.DataFrame(
    np.random.randn(30, 3).cumsum(axis=0) + 10,
    columns=['Series 1', 'Series 2', 'Series 3']
)
st.area_chart(area_data)"""
        
        elif code_level == "advanced":
            code = """import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# Plotlyを使用した高度なチャート
fig = go.Figure()

# 複数の系列を追加
x = np.linspace(0, 10, 100)
fig.add_trace(go.Scatter(x=x, y=np.sin(x), mode='lines', name='sin(x)'))
fig.add_trace(go.Scatter(x=x, y=np.cos(x), mode='lines', name='cos(x)'))

# レイアウトのカスタマイズ
fig.update_layout(
    title='三角関数のグラフ',
    xaxis_title='X軸',
    yaxis_title='Y軸',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# リアルタイム更新のシミュレーション
placeholder = st.empty()

for i in range(10):
    with placeholder.container():
        # 新しいデータを生成
        new_data = pd.DataFrame(
            np.random.randn(50, 3).cumsum(axis=0),
            columns=['A', 'B', 'C']
        )
        st.line_chart(new_data)
    time.sleep(1)"""
        
        else:  # full
            code = '''import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def create_analytics_dashboard():
    """分析ダッシュボードの作成"""
    
    st.title("📈 データ分析ダッシュボード")
    
    # サイドバーでパラメータ設定
    with st.sidebar:
        st.header("設定")
        days = st.slider("表示期間（日）", 7, 90, 30)
        chart_type = st.selectbox("チャートタイプ", ["Line", "Bar", "Area"])
        show_trend = st.checkbox("トレンドラインを表示", value=True)
    
    # データ生成
    dates = pd.date_range(end=datetime.now(), periods=days)
    df = pd.DataFrame({
        "Date": dates,
        "Sales": np.random.randint(100, 1000, days).cumsum(),
        "Profit": np.random.randint(50, 500, days).cumsum(),
        "Customers": np.random.randint(10, 100, days).cumsum()
    })
    
    # メインチャート
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("売上推移")
        
        if chart_type == "Line":
            fig = px.line(df, x="Date", y=["Sales", "Profit"], 
                         title="売上と利益の推移")
        elif chart_type == "Bar":
            fig = px.bar(df, x="Date", y="Sales", title="日別売上")
        else:
            fig = px.area(df, x="Date", y=["Sales", "Profit"], 
                         title="売上と利益（累積）")
        
        if show_trend:
            # トレンドライン追加
            z = np.polyfit(range(len(df)), df["Sales"], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=df["Date"],
                y=p(range(len(df))),
                mode="lines",
                name="トレンド",
                line=dict(dash="dash")
            ))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("サマリー統計")
        st.metric("総売上", f"¥{df['Sales'].sum():,.0f}")
        st.metric("総利益", f"¥{df['Profit'].sum():,.0f}")
        st.metric("平均顧客数", f"{df['Customers'].mean():.0f}")
        
        # ミニチャート
        st.line_chart(df[["Customers"]].tail(7))
    
    # 詳細分析
    st.subheader("詳細分析")
    tabs = st.tabs(["日次", "週次", "月次"])
    
    with tabs[0]:
        st.dataframe(df.tail(7), use_container_width=True)
    
    with tabs[1]:
        weekly = df.set_index("Date").resample("W").sum()
        st.bar_chart(weekly)
    
    with tabs[2]:
        monthly = df.set_index("Date").resample("M").sum()
        st.area_chart(monthly)

if __name__ == "__main__":
    create_analytics_dashboard()'''
        
        code_display.display_with_copy(code, key=f"code_{category}_{code_level}")
    
    else:
        st.info(f"🚧 {category} のコード例は準備中です")

def render_documentation_tab(category: str):
    """ドキュメントタブのレンダリング"""
    st.subheader("ドキュメント")
    
    with st.expander("📖 基本的な使い方", expanded=True):
        if category == "input_widgets":
            st.markdown("""
            ### Input Widgets
            
            入力ウィジェットは、ユーザーからの入力を受け取るためのコンポーネントです。
            
            **主なコンポーネント:**
            - `st.text_input()` - 単一行テキスト入力
            - `st.text_area()` - 複数行テキスト入力
            - `st.number_input()` - 数値入力
            - `st.date_input()` - 日付選択
            - `st.time_input()` - 時刻選択
            - `st.file_uploader()` - ファイルアップロード
            """)
        
        elif category == "display_widgets":
            st.markdown("""
            ### Display Widgets
            
            表示ウィジェットは、情報を表示するためのコンポーネントです。
            
            **テキスト表示:**
            - `st.write()` - 汎用表示（自動判定）
            - `st.text()` - プレーンテキスト
            - `st.markdown()` - Markdown形式
            - `st.latex()` - LaTeX数式
            
            **見出し:**
            - `st.title()` - ページタイトル
            - `st.header()` - セクション見出し
            - `st.subheader()` - サブセクション見出し
            - `st.caption()` - 小さな説明文
            
            **メッセージ:**
            - `st.success()` - 成功メッセージ（緑）
            - `st.info()` - 情報メッセージ（青）
            - `st.warning()` - 警告メッセージ（黄）
            - `st.error()` - エラーメッセージ（赤）
            
            **コード:**
            - `st.code()` - シンタックスハイライト付きコード
            - `st.echo()` - コードと実行結果を表示
            """)
        
        elif category == "data_widgets":
            st.markdown("""
            ### Data Display Widgets
            
            データ表示ウィジェットは、構造化データを表示するためのコンポーネントです。
            
            **主なコンポーネント:**
            - `st.dataframe()` - インタラクティブなテーブル（ソート・フィルタ可能）
            - `st.table()` - 静的なテーブル
            - `st.metric()` - KPI表示（変化量付き）
            - `st.json()` - JSON形式のデータ表示
            
            **特徴:**
            - **st.dataframe**: 大規模データ対応、検索・ソート機能
            - **st.table**: 小規模データ向け、シンプルな表示
            - **st.metric**: ダッシュボード向け、デルタ表示
            - **st.json**: API応答やconfig表示に最適
            """)
        
        elif category == "chart_widgets":
            st.markdown("""
            ### Chart Widgets
            
            チャートウィジェットは、データを視覚化するためのコンポーネントです。
            
            **基本チャート:**
            - `st.line_chart()` - 折れ線グラフ
            - `st.bar_chart()` - 棒グラフ
            - `st.area_chart()` - エリアチャート
            - `st.scatter_chart()` - 散布図
            
            **高度なチャート:**
            - `st.plotly_chart()` - Plotlyチャート
            - `st.altair_chart()` - Altairチャート
            - `st.vega_lite_chart()` - Vega-Liteチャート
            - `st.pyplot()` - Matplotlib図
            
            **特徴:**
            - インタラクティブなズーム・パン機能
            - レスポンシブデザイン
            - リアルタイム更新対応
            """)
        
        else:
            st.info(f"🚧 {category} のドキュメントは準備中です")
    
    with st.expander("💡 Tips & Tricks"):
        if category == "display_widgets":
            st.markdown("""
            - `st.write()`は最も汎用的で、DataFrameやグラフも自動で適切に表示
            - Markdown内でHTMLを使いたい場合は`unsafe_allow_html=True`を設定
            - メッセージ系は処理結果の通知に便利
            - `st.code()`は自動的にコピーボタンが付く
            """)
        elif category == "data_widgets":
            st.markdown("""
            - `st.dataframe()`の`column_config`で列ごとに表示形式をカスタマイズ可能
            - `st.metric()`の`delta_color="inverse"`で色の意味を反転（低い方が良い場合）
            - DataFrameのスタイル（`.style`）も適用可能
            - `use_container_width=True`でコンテナ幅いっぱいに表示
            """)
        elif category == "chart_widgets":
            st.markdown("""
            - データフレームのインデックスがX軸として自動的に使用される
            - 複数の列がある場合は自動的に複数系列として表示
            - `use_container_width=True`でレスポンシブに
            - Plotlyチャートの方が高度なカスタマイズが可能
            """)
        else:
            st.markdown("""
            - パラメータ `key` を使用して、ウィジェットを一意に識別
            - `help` パラメータでツールチップを追加
            - `on_change` コールバックで変更を検知
            """)
    
    with st.expander("⚠️ よくある問題"):
        if category == "display_widgets":
            st.markdown("""
            - **問題**: Markdownで改行が反映されない
            - **解決**: 行末に2つのスペースを追加するか、空行を入れる
            
            - **問題**: HTMLが表示されない
            - **解決**: `unsafe_allow_html=True`パラメータを追加
            """)
        elif category == "data_widgets":
            st.markdown("""
            - **問題**: DataFrameが見切れる
            - **解決**: `use_container_width=True`を使用
            
            - **問題**: metricのdeltaが意図と逆の色
            - **解決**: `delta_color="inverse"`を設定
            """)
        elif category == "chart_widgets":
            st.markdown("""
            - **問題**: チャートが表示されない
            - **解決**: データフレームの形式を確認（数値列が必要）
            
            - **問題**: X軸が意図通りにならない
            - **解決**: DataFrameのインデックスを設定
            """)
        else:
            st.markdown("""
            - **問題**: ページリロード時に値がリセットされる
            - **解決**: `st.session_state` を使用して値を保持
            """)

@error_handler.error_boundary(message="アプリケーションエラーが発生しました")
def main():
    """メインアプリケーション"""
    # セッション状態の初期化
    initialize_session_state()
    
    # サイドバー
    render_sidebar()
    
    # メインコンテンツ
    render_main_content()
    
    # フッター
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"© 2024 {APP_NAME}")
    with col2:
        st.caption(f"Version {APP_VERSION}")
    with col3:
        st.caption("Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main()