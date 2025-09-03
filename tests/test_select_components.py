"""
選択系基本コンポーネントのテスト
"""
import streamlit as st

st.set_page_config(
    page_title="Select Components Test",
    page_icon="☑️",
    layout="wide"
)

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from components.select_widgets.basic_selects import (
        CheckboxComponent,
        RadioComponent,
        SelectboxComponent,
        MultiselectComponent
    )
    
    st.title("☑️ 選択系基本コンポーネントテスト")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "checkbox", "radio", "selectbox", "multiselect"
    ])
    
    with tab1:
        st.header("st.checkbox")
        CheckboxComponent().render_demo()
    
    with tab2:
        st.header("st.radio")
        RadioComponent().render_demo()
    
    with tab3:
        st.header("st.selectbox")
        SelectboxComponent().render_demo()
    
    with tab4:
        st.header("st.multiselect")
        MultiselectComponent().render_demo()
        
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())
