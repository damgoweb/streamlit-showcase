"""
Streamlit UIコンポーネントショーケース
メインアプリケーション - 検索機能統合版
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
from utils.search import search_engine, SearchMode

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
        st.session_state.show_search_results = False

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
        
        # 検索ボックス（改良版）
        search_query = st.text_input(
            "🔍 コンポーネントを検索",
            value=state_manager.get('search_query', ''),
            placeholder="例: text, chart, button",
            help="コンポーネント名、説明、タグで検索できます"
        )
        
        # 検索モード選択と検索ボタン
        col1, col2 = st.columns(2)
        with col1:
            search_mode = st.selectbox(
                "検索モード",
                ["部分一致", "完全一致"],
                index=0,
                help="検索の一致方法を選択"
            )
        with col2:
            if st.button("🔍 検索", use_container_width=True):
                state_manager.set('search_query', search_query)
                state_manager.set('search_mode', search_mode)
                state_manager.set('show_search_results', True)
                st.rerun()
        
        # 検索候補表示
        if search_query and len(search_query) >= 2:
            suggestions = search_engine.get_suggestions(search_query, limit=3)
            if suggestions:
                st.caption("💡 候補:")
                for suggestion in suggestions:
                    if st.button(f"→ {suggestion}", key=f"sugg_{suggestion}"):
                        state_manager.set('search_query', suggestion)
                        state_manager.set('search_mode', search_mode)
                        state_manager.set('show_search_results', True)
                        st.rerun()
        
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
                state_manager.set('show_search_results', False)
                st.rerun()
        
        if favorites:
            for fav in favorites[:5]:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    # クリック可能なリンクとして表示
                    if st.button(f"📍 {fav}", key=f"goto_{fav}", use_container_width=True):
                        state_manager.set('current_component', fav)
                        state_manager.set('view_mode', 'component')
                        state_manager.set('show_search_results', False)
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

def render_search_results():
    """検索結果を表示"""
    search_query = state_manager.get('search_query', '')
    search_mode_str = state_manager.get('search_mode', '部分一致')
    
    if not search_query:
        st.info("検索キーワードを入力してください")
        return
    
    # 検索モードの変換
    mode = SearchMode.PARTIAL if search_mode_str == "部分一致" else SearchMode.EXACT
    
    # 検索実行
    results = search_engine.search(
        query=search_query,
        mode=mode,
        limit=20
    )
    
    # ヘッダー
    col1, col2 = st.columns([10, 1])
    with col1:
        st.title(f"🔍 検索結果: '{search_query}'")
        st.caption(f"検索モード: {search_mode_str} | {len(results)}件の結果")
    with col2:
        if st.button("✖️", help="検索を終了"):
            state_manager.set('show_search_results', False)
            state_manager.set('search_query', '')
            st.rerun()
    
    if not results:
        st.warning("検索結果が見つかりませんでした")
        st.info("別のキーワードで検索してみてください")
        return
    
    # 検索結果の表示
    for i, result in enumerate(results):
        with st.container():
            col1, col2, col3 = st.columns([6, 2, 2])
            
            with col1:
                # コンポーネント名（ハイライト付き）
                if 'name' in result.highlights:
                    st.markdown(f"### {result.highlights['name']}")
                else:
                    st.markdown(f"### {result.name}")
                
                # 説明（ハイライト付き）
                if 'description' in result.highlights:
                    st.markdown(result.highlights['description'])
                else:
                    st.write(result.description)
                
                # マッチしたフィールド
                st.caption(f"💡 マッチ: {', '.join(result.matched_fields)} | スコア: {result.score:.1f}")
            
            with col2:
                # カテゴリバッジ
                category_info = COMPONENT_CATEGORIES.get(result.category, {})
                st.info(f"{category_info.get('icon', '')} {category_info.get('name', result.category)}")
            
            with col3:
                # アクションボタン
                if st.button("詳細を見る", key=f"view_{result.component_id}"):
                    state_manager.set('current_component', result.component_id)
                    state_manager.set('current_category', result.category)
                    state_manager.set('view_mode', 'component')
                    state_manager.set('show_search_results', False)
                    st.rerun()
                
                # お気に入りボタン
                is_favorite = state_manager.is_favorite(result.component_id)
                fav_label = "★" if is_favorite else "☆"
                if st.button(fav_label, key=f"fav_search_{result.component_id}"):
                    state_manager.toggle_favorite(result.component_id)
                    st.rerun()
            
            st.divider()
    
    # 関連コンポーネントの表示
    if results:
        st.subheader("🔗 関連するコンポーネント")
        first_result = results[0]
        related = search_engine.get_related_components(first_result.component_id, limit=5)
        
        if related:
            cols = st.columns(min(len(related), 5))
            for i, comp_id in enumerate(related):
                with cols[i]:
                    if st.button(comp_id, key=f"related_{comp_id}", use_container_width=True):
                        state_manager.set('current_component', comp_id)
                        state_manager.set('view_mode', 'component')
                        state_manager.set('show_search_results', False)
                        st.rerun()

def render_main_content():
    """メインコンテンツのレンダリング"""
    # 検索結果表示モードのチェック
    if state_manager.get('show_search_results', False):
        render_search_results()
        return
    
    selected_category = state_manager.get('current_category', 'input_widgets')
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
                    st.text_input("プレビュー", "サンプル", key=f"preview_{fav}")
                elif fav == "number_input":
                    st.number_input("プレビュー", value=100, key=f"preview_{fav}")
                elif fav == "text_area":
                    st.text_area("プレビュー", "複数行のテキスト", key=f"preview_{fav}", height=100)
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
    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
        st.title(f"📍 st.{component_name}")
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
        render_component_demo(component_name)
    
    with tabs[1]:
        render_component_code(component_name)
    
    with tabs[2]:
        render_component_docs(component_name)
    
    with tabs[3]:
        render_component_examples(component_name)

def render_component_demo(component_name: str):
    """コンポーネントのデモを表示"""
    st.subheader("🎮 インタラクティブデモ")
    
    if component_name == "text_input":
        with st.expander("⚙️ パラメータ設定", expanded=True):
            label = st.text_input("ラベル", "テキストを入力", key="param_label")
            value = st.text_input("デフォルト値", "", key="param_value")
            max_chars = st.number_input("最大文字数", min_value=1, value=100, key="param_max")
            placeholder = st.text_input("プレースホルダー", "ここに入力...", key="param_ph")
            help_text = st.text_input("ヘルプテキスト", "説明文", key="param_help")
        
        st.subheader("実行結果")
        result = st.text_input(
            label,
            value=value,
            max_chars=max_chars,
            placeholder=placeholder,
            help=help_text,
            key="demo_text_input"
        )
        st.success(f"入力値: {result}")
    
    elif component_name == "number_input":
        with st.expander("⚙️ パラメータ設定", expanded=True):
            label = st.text_input("ラベル", "数値を入力", key="param_label")
            min_value = st.number_input("最小値", value=0, key="param_min")
            max_value = st.number_input("最大値", value=100, key="param_max")
            value = st.number_input("デフォルト値", min_value=min_value, max_value=max_value, value=50, key="param_value")
            step = st.number_input("ステップ", value=1, key="param_step")
        
        st.subheader("実行結果")
        result = st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            value=value,
            step=step,
            key="demo_number_input"
        )
        st.success(f"入力値: {result}")
    
    elif component_name == "text_area":
        with st.expander("⚙️ パラメータ設定", expanded=True):
            label = st.text_input("ラベル", "テキストエリア", key="param_label")
            value = st.text_area("デフォルト値", "初期テキスト", key="param_value", height=50)
            height = st.number_input("高さ（ピクセル）", min_value=50, value=200, key="param_height")
            max_chars = st.number_input("最大文字数", min_value=0, value=0, key="param_max", help="0は無制限")
        
        st.subheader("実行結果")
        result = st.text_area(
            label,
            value=value,
            height=height,
            max_chars=max_chars if max_chars > 0 else None,
            key="demo_text_area"
        )
        st.success(f"入力文字数: {len(result)}")
    
    else:
        st.info(f"🚧 {component_name} のデモは準備中です")

def render_component_code(component_name: str):
    """コンポーネントのコードを表示"""
    st.subheader("💻 コード生成")
    
    code_templates = {
        "text_input": """import streamlit as st

result = st.text_input(
    label="テキストを入力",
    value="",
    max_chars=100,
    placeholder="ここに入力...",
    help="説明文"
)

st.write(f"入力値: {result}")""",
        
        "number_input": """import streamlit as st

result = st.number_input(
    label="数値を入力",
    min_value=0,
    max_value=100,
    value=50,
    step=1
)

st.write(f"入力値: {result}")""",
        
        "text_area": """import streamlit as st

result = st.text_area(
    label="複数行テキスト",
    value="",
    height=200,
    max_chars=500,
    placeholder="ここに複数行のテキストを入力..."
)

st.write(f"入力文字数: {len(result)}")"""
    }
    
    code = code_templates.get(component_name, f"st.{component_name}()")
    st.code(code, language="python")
    
    if st.button("📋 コードをコピー", key="copy_code"):
        st.success("コピーしました！")

def render_component_docs(component_name: str):
    """コンポーネントのドキュメントを表示"""
    st.subheader("📚 ドキュメント")
    
    # メタデータから情報を取得
    component_meta = search_engine.index.get(component_name, {})
    
    st.markdown(f"### st.{component_name}")
    st.write(component_meta.get('description', 'コンポーネントの説明'))
    
    # パラメータ
    if 'parameters' in component_meta:
        st.markdown("#### パラメータ")
        for param in component_meta['parameters']:
            param_name = param['name']
            param_type = param['type']
            param_desc = param.get('description', '')
            required = "必須" if param.get('required', False) else "オプション"
            
            st.markdown(f"- **`{param_name}`** ({param_type}, {required}): {param_desc}")
    
    # Tips
    if 'tips' in component_meta:
        st.markdown("#### 💡 Tips")
        for tip in component_meta['tips']:
            st.markdown(f"- {tip}")
    
    # 関連コンポーネント
    if 'related' in component_meta:
        st.markdown("#### 🔗 関連コンポーネント")
        related_str = ", ".join([f"`st.{comp}`" for comp in component_meta['related']])
        st.markdown(related_str)

def render_component_examples(component_name: str):
    """コンポーネントの使用例を表示"""
    st.subheader("💡 使用例")
    
    # メタデータから例を取得
    component_meta = search_engine.index.get(component_name, {})
    
    if 'examples' in component_meta:
        for example in component_meta['examples']:
            st.markdown(f"#### {example['title']}")
            st.code(example['code'], language="python")
    else:
        # デフォルトの例
        st.code(f"""
# 基本的な使い方
result = st.{component_name}("ラベル")

# オプション付き
result = st.{component_name}(
    "ラベル",
    value="デフォルト",
    help="ヘルプテキスト"
)
        """, language="python")

def render_demo_tab(category: str):
    """デモタブのレンダリング"""
    st.subheader("コンポーネントデモ")
    
    if category == "input_widgets":
        render_input_widgets_demo()
    elif category == "display_widgets":
        render_display_widgets_demo()
    elif category == "data_widgets":
        render_data_widgets_demo()
    elif category == "chart_widgets":
        render_chart_widgets_demo()
    else:
        st.info(f"🚧 {category} のデモは準備中です")

def render_input_widgets_demo():
    """入力ウィジェットのデモ"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Text Input")
        text_value = st.text_input("名前を入力", "太郎")
        st.write(f"入力値: {text_value}")
        
        if st.button("⭐ お気に入り", key="fav_text_input"):
            state_manager.toggle_favorite("text_input")
            st.rerun()
        
        view_count = state_manager.increment_view_count("text_input")
        st.caption(f"閲覧回数: {view_count}")
    
    with col2:
        st.markdown("### Number Input")
        number_value = st.number_input("年齢を入力", min_value=0, max_value=120, value=30)
        st.write(f"入力値: {number_value}")
        
        if st.button("⭐ お気に入り", key="fav_number_input"):
            state_manager.toggle_favorite("number_input")
            st.rerun()
        
        view_count = state_manager.increment_view_count("number_input")
        st.caption(f"閲覧回数: {view_count}")

def render_display_widgets_demo():
    """表示ウィジェットのデモ"""
    tabs = st.tabs(["テキスト", "見出し", "メッセージ", "コード"])
    
    with tabs[0]:
        st.write("これは **st.write** で表示されたテキストです。")
        st.text("これは st.text で表示された固定幅フォントのテキストです")
        st.markdown("**太字** と *イタリック*")
    
    with tabs[1]:
        st.title("st.title - タイトル")
        st.header("st.header - ヘッダー")
        st.subheader("st.subheader - サブヘッダー")
        st.caption("st.caption - キャプション")
    
    with tabs[2]:
        st.success("✅ 成功メッセージ")
        st.info("ℹ️ 情報メッセージ")
        st.warning("⚠️ 警告メッセージ")
        st.error("❌ エラーメッセージ")
    
    with tabs[3]:
        code_example = '''def hello():
    print("Hello, World!")
    return True'''
        st.code(code_example, language='python')

def render_data_widgets_demo():
    """データ表示ウィジェットのデモ"""
    tabs = st.tabs(["DataFrame", "Table", "Metric", "JSON"])
    
    with tabs[0]:
        st.markdown("### st.dataframe")
        df = sample_data.generate_dataframe(rows=10)
        st.dataframe(df, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### st.table")
        table_data = pd.DataFrame({
            '項目': ['A', 'B', 'C'],
            '値': [100, 200, 150]
        })
        st.table(table_data)
    
    with tabs[2]:
        st.markdown("### st.metric")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("売上", "¥1.2M", "+15%")
        with col2:
            st.metric("ユーザー", "1,234", "+89")
        with col3:
            st.metric("評価", "4.8/5.0", "+0.2")
    
    with tabs[3]:
        st.markdown("### st.json")
        json_data = {
            "name": "Streamlit",
            "version": "1.33.0",
            "features": ["Fast", "Easy", "Interactive"]
        }
        st.json(json_data)

def render_chart_widgets_demo():
    """チャートウィジェットのデモ"""
    from components.chart_widgets.basic_charts import ChartDataGenerator
    
    generator = ChartDataGenerator()
    tabs = st.tabs(["Line Chart", "Bar Chart", "Area Chart"])
    
    with tabs[0]:
        st.markdown("### Line Chart")
        data = generator.generate_time_series(days=30, columns=["売上", "利益"])
        st.line_chart(data)
    
    with tabs[1]:
        st.markdown("### Bar Chart")
        data = generator.generate_categorical_data(
            categories=["Q1", "Q2", "Q3", "Q4"],
            metrics=["売上", "利益"]
        )
        chart_data = data.set_index('Category')
        st.bar_chart(chart_data)
    
    with tabs[2]:
        st.markdown("### Area Chart")
        data = generator.generate_time_series(
            days=30,
            columns=["デスクトップ", "モバイル", "タブレット"]
        )
        st.area_chart(data)

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
        else:
            st.info(f"🚧 {category} のドキュメントは準備中です")
    
    with st.expander("💡 Tips & Tricks"):
        st.markdown("""
        - パラメータ `key` を使用して、ウィジェットを一意に識別
        - `help` パラメータでツールチップを追加
        - `on_change` コールバックで変更を検知
        """)

@error_handler.error_boundary(message="アプリケーションエラーが発生しました")
def main():
    """メインアプリケーション"""
    initialize_session_state()
    render_sidebar()
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