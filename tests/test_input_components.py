"""
入力ウィジェット全体のテスト
"""
import streamlit as st

st.set_page_config(
    page_title="Input Components Test",
    page_icon="📝",
    layout="wide"
)

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

st.title("📝 入力ウィジェット コンポーネントテスト")

# 各モジュールからインポート
try:
    from components.input_widgets.text_inputs import TextInputComponent, TextAreaComponent
    from components.input_widgets.numeric_inputs import NumberInputComponent
    from components.input_widgets.date_time_inputs import DateInputComponent, TimeInputComponent
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "text_input", "text_area", "number_input", "date_input", "time_input"
    ])
    
    with tab1:
        TextInputComponent().render_demo()
    
    with tab2:
        TextAreaComponent().render_demo()
    
    with tab3:
        NumberInputComponent().render_demo()
    
    with tab4:
        DateInputComponent().render_demo()
    
    with tab5:
        TimeInputComponent().render_demo()
        
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())
