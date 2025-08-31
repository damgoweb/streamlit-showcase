"""
Streamlit UIコンポーネントショーケース
メインアプリケーション - ユーティリティ統合版!
"""

import streamlit as st
import sys
from pathlib import Path

# プロジェクトルートをパスに追加（必要に応じて）
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
        favorites = state_manager.get_favorites()
        if favorites:
            for fav in favorites[:5]:
                st.caption(f"• {fav}")
            if len(favorites) > 5:
                st.caption(f"他 {len(favorites) - 5} 件...")
        else:
            st.caption("お気に入りはまだありません")
        
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

def render_main_content():
    """メインコンテンツのレンダリング"""
    selected_category = state_manager.get('current_category', 'input_widgets')
    search_query = state_manager.get('search_query', '')
    
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

def render_demo_tab(category: str):
    """デモタブのレンダリング"""
    st.subheader("コンポーネントデモ")
    
    # カテゴリごとのデモ（仮実装）
    if category == "input_widgets":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Text Input")
            text_value = st.text_input("名前を入力", "太郎")
            st.write(f"入力値: {text_value}")
            
            # 閲覧回数をカウント
            state_manager.increment_view_count("text_input")
            
            # お気に入りボタン
            if st.button("⭐ お気に入りに追加", key="fav_text_input"):
                if state_manager.toggle_favorite("text_input"):
                    st.success("お気に入りに追加しました")
                else:
                    st.info("お気に入りから削除しました")
        
        with col2:
            st.markdown("### Number Input")
            number_value = st.number_input("年齢を入力", min_value=0, max_value=120, value=30)
            st.write(f"入力値: {number_value}")
            
            state_manager.increment_view_count("number_input")
    
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

def render_code_examples_tab(category: str):
    """コード例タブのレンダリング"""
    st.subheader("コード例")
    
    # コードレベル選択
    code_level = st.radio(
        "コードレベル",
        ["basic", "advanced", "full"],
        horizontal=True
    )
    
    # サンプルコード生成
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
        
        # コード表示
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
    
    with st.expander("⚠️ よくある問題"):
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