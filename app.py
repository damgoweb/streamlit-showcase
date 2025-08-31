"""
Streamlit UIコンポーネントショーケース
メインアプリケーション
"""

import streamlit as st
from config import (
    APP_NAME, 
    APP_VERSION, 
    APP_DESCRIPTION,
    COMPONENT_CATEGORIES
)

# ページ設定
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """メインアプリケーション"""
    
    # サイドバー
    with st.sidebar:
        st.title(f"{APP_NAME}")
        st.caption(f"Version {APP_VERSION}")
        st.divider()
        
        # カテゴリ選択
        st.subheader("📚 カテゴリ")
        selected_category = st.selectbox(
            "カテゴリを選択",
            options=list(COMPONENT_CATEGORIES.keys()),
            format_func=lambda x: f"{COMPONENT_CATEGORIES[x]['icon']} {COMPONENT_CATEGORIES[x]['name']}"
        )
        
        st.divider()
        st.caption(APP_DESCRIPTION)
    
    # メインコンテンツ
    st.title(f"{COMPONENT_CATEGORIES[selected_category]['icon']} {COMPONENT_CATEGORIES[selected_category]['name']}")
    st.markdown(COMPONENT_CATEGORIES[selected_category]['description'])
    
    # プレースホルダー
    st.info("🚧 コンポーネントの実装準備中...")

if __name__ == "__main__":
    main()