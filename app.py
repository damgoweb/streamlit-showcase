"""
Streamlit UIコンポーネントショーケース
メインアプリケーション - お気に入り機能修正版
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
        st.title(f"📍 {component_name}")
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
    
    # カテゴリごとのデモ（仮実装）
    if category == "input_widgets":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Text Input")
            
            # お気に入り状態を確認
            is_favorite_text = state_manager.is_favorite("text_input")
            
            # お気に入りボタン（状態に応じてアイコンを変更）
            fav_button_label = "⭐ お気に入りから削除" if is_favorite_text else "⭐ お気に入りに追加"
            
            if st.button(fav_button_label, key="fav_text_input"):
                if state_manager.toggle_favorite("text_input"):
                    st.success("✅ お気に入りに追加しました")
                else:
                    st.info("ℹ️ お気に入りから削除しました")
                st.rerun()  # 画面を更新してサイドバーに反映
            
            # コンポーネントのデモ
            text_value = st.text_input("名前を入力", "太郎")
            st.write(f"入力値: {text_value}")
            
            # 閲覧回数をカウント
            view_count = state_manager.increment_view_count("text_input")
            st.caption(f"閲覧回数: {view_count}")
        
        with col2:
            st.markdown("### Number Input")
            
            # お気に入り状態を確認
            is_favorite_number = state_manager.is_favorite("number_input")
            
            # お気に入りボタン
            fav_button_label = "⭐ お気に入りから削除" if is_favorite_number else "⭐ お気に入りに追加"
            
            if st.button(fav_button_label, key="fav_number_input"):
                if state_manager.toggle_favorite("number_input"):
                    st.success("✅ お気に入りに追加しました")
                else:
                    st.info("ℹ️ お気に入りから削除しました")
                st.rerun()  # 画面を更新
            
            # コンポーネントのデモ
            number_value = st.number_input("年齢を入力", min_value=0, max_value=120, value=30)
            st.write(f"入力値: {number_value}")
            
            # 閲覧回数をカウント
            view_count = state_manager.increment_view_count("number_input")
            st.caption(f"閲覧回数: {view_count}")
    
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