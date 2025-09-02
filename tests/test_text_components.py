"""
テキストコンポーネントのテスト
"""
import streamlit as st
import sys
from pathlib import Path

# ページ設定を最初に実行
st.set_page_config(
    page_title="Text Components Test",
    page_icon="📝",
    layout="wide"
)

# プロジェクトルートをパスに追加
if Path.cwd().name == 'tests':
    sys.path.insert(0, str(Path.cwd().parent))
else:
    sys.path.insert(0, str(Path.cwd()))

# インポート試行
try:
    from components.input_widgets.text_inputs import TextInputComponent, TextAreaComponent
    import_success = True
except ImportError as e:
    import_success = False
    st.error(f"❌ インポートエラー: {e}")
    st.info("components/input_widgets/text_inputs.py を作成してください")

# デバッグ情報（サイドバー）
with st.sidebar:
    st.caption("デバッグ情報")
    st.caption(f"Path: {Path.cwd()}")
    if import_success:
        st.success("✅ モジュール読込成功")
    else:
        st.error("❌ モジュール読込失敗")

# メインコンテンツ
st.title("📝 テキスト入力コンポーネントテスト")

if import_success:
    tab1, tab2 = st.tabs(["text_input", "text_area"])

    with tab1:
        st.header("st.text_input")
        try:
            text_input_component = TextInputComponent()
            text_input_component.render_demo()
        except Exception as e:
            st.error(f"コンポーネントエラー: {e}")
            st.exception(e)

    with tab2:
        st.header("st.text_area")
        try:
            text_area_component = TextAreaComponent()
            text_area_component.render_demo()
        except Exception as e:
            st.error(f"コンポーネントエラー: {e}")
            st.exception(e)
else:
    st.warning("コンポーネントをインポートできませんでした。")
    st.info("ファイルの配置を確認してください：")
    st.code("""
    streamlit-showcase/
    ├── components/
    │   ├── __init__.py
    │   ├── base_component.py
    │   └── input_widgets/
    │       ├── __init__.py
    │       └── text_inputs.py
    """)
