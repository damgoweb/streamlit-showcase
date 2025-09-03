"""
表示系コンポーネントのテスト
"""
import streamlit as st

st.set_page_config(
    page_title="Display Components Test",
    page_icon="📝",
    layout="wide"
)

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from components.display_widgets.text_display import (
        WriteComponent,
        MarkdownComponent,
        HeadingComponents,
        CodeComponent,
        MessageComponents
    )
    
    st.title("📝 表示系コンポーネントテスト")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "write", "markdown", "headings", "code", "messages"
    ])
    
    with tab1:
        st.header("st.write")
        WriteComponent().render_demo()
    
    with tab2:
        st.header("st.markdown")
        MarkdownComponent().render_demo()
    
    with tab3:
        st.header("見出し系")
        HeadingComponents().render_demo()
    
    with tab4:
        st.header("st.code")
        CodeComponent().render_demo()
        
    with tab5:
        st.header("メッセージ系")
        MessageComponents().render_demo()
        
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())