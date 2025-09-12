"""
レイアウトコンポーネント
- columns: カラムレイアウト
- container: コンテナ
- expander: 展開可能セクション
- tabs: タブコンポーネント
"""

import streamlit as st
from typing import List, Optional, Union, Any, Dict, Tuple
import pandas as pd
import numpy as np
from datetime import datetime


class LayoutComponents:
    """レイアウトコンポーネント集"""
    
    @staticmethod
    def columns_demo(
        num_columns: int = 2,
        gap: str = "medium",
        example_type: str = "basic"
    ) -> None:
        """
        カラムレイアウトのデモ
        
        Args:
            num_columns: カラム数
            gap: カラム間のギャップ（small, medium, large）
            example_type: 例のタイプ
        """
        st.subheader(f"📏 {num_columns} Columns Layout")
        
        if example_type == "basic":
            # 基本的な均等割り
            cols = st.columns(num_columns, gap=gap)
            for idx, col in enumerate(cols):
                with col:
                    st.metric(f"Column {idx+1}", f"Value {idx+1}", f"+{(idx+1)*10}%")
                    st.write(f"This is column {idx+1}")
                    
        elif example_type == "weighted":
            # 重み付きカラム
            if num_columns == 2:
                col1, col2 = st.columns([2, 1], gap=gap)
                with col1:
                    st.info("📏 This column is 2x wider")
                    st.bar_chart(pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C']))
                with col2:
                    st.warning("📐 This column is narrower")
                    st.metric("Metric", "123", "+45%")
                    
            elif num_columns == 3:
                col1, col2, col3 = st.columns([1, 2, 1], gap=gap)
                with col1:
                    st.info("Side")
                    st.button("Action 1")
                with col2:
                    st.success("Main Content (2x)")
                    st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=['X', 'Y']))
                with col3:
                    st.info("Side")
                    st.button("Action 2")
                    
        elif example_type == "nested":
            # ネストされたカラム
            col1, col2 = st.columns(2)
            with col1:
                st.header("Parent Column 1")
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.write("Sub 1-1")
                    st.number_input("Input 1", key="nested_1")
                with subcol2:
                    st.write("Sub 1-2")
                    st.number_input("Input 2", key="nested_2")
            with col2:
                st.header("Parent Column 2")
                subcol3, subcol4 = st.columns(2)
                with subcol3:
                    st.write("Sub 2-1")
                    st.selectbox("Select", ["A", "B"], key="nested_3")
                with subcol4:
                    st.write("Sub 2-2")
                    st.checkbox("Check", key="nested_4")
    
    @staticmethod
    def container_demo(
        example_type: str = "basic",
        show_border: bool = True
    ) -> None:
        """
        コンテナのデモ
        
        Args:
            example_type: 例のタイプ
            show_border: 境界線を表示するか
        """
        st.subheader("📦 Container Layout")
        
        if example_type == "basic":
            # 基本的なコンテナ
            with st.container(border=show_border):
                st.write("This is inside a container")
                st.bar_chart(pd.DataFrame(np.random.randn(10, 3), columns=['A', 'B', 'C']))
                
        elif example_type == "dynamic":
            # 動的コンテンツ
            container = st.container(border=show_border)
            
            # コンテナの後に追加されるコンテンツ
            st.write("This is written after the container")
            
            # コンテナに後から追加
            with container:
                st.write("But this is added to the container!")
                st.success("Dynamic content insertion")
                
        elif example_type == "placeholder":
            # プレースホルダーとして使用
            placeholder = st.empty()
            
            # 選択に応じて内容を変更
            content_type = st.radio("Select content:", ["Text", "Chart", "Metric"])
            
            with placeholder.container():
                if content_type == "Text":
                    st.write("### Text Content")
                    st.write("This is a text paragraph in the placeholder.")
                elif content_type == "Chart":
                    st.write("### Chart Content")
                    st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C']))
                else:
                    st.write("### Metric Content")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sales", "1.2M", "+15%")
                    with col2:
                        st.metric("Users", "8.5K", "+5%")
                    with col3:
                        st.metric("Revenue", "3.2M", "+20%")
    
    @staticmethod
    def expander_demo(
        example_type: str = "basic",
        expanded_by_default: bool = False
    ) -> None:
        """
        エクスパンダーのデモ
        
        Args:
            example_type: 例のタイプ
            expanded_by_default: デフォルトで展開するか
        """
        st.subheader("📂 Expander Layout")
        
        if example_type == "basic":
            # 基本的なエクスパンダー
            with st.expander("Click to expand", expanded=expanded_by_default):
                st.write("### Hidden Content")
                st.write("This content is hidden by default and can be expanded.")
                st.image("https://via.placeholder.com/400x200.png?text=Sample+Image")
                
        elif example_type == "multiple":
            # 複数のエクスパンダー（アコーディオン風）
            with st.expander("📊 Section 1: Data", expanded=expanded_by_default):
                df = pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])
                st.dataframe(df)
                
            with st.expander("📈 Section 2: Charts"):
                st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=['X', 'Y', 'Z']))
                
            with st.expander("⚙️ Section 3: Settings"):
                st.slider("Parameter 1", 0, 100, 50)
                st.selectbox("Option", ["Option A", "Option B", "Option C"])
                st.checkbox("Enable feature")
                
        elif example_type == "nested":
            # ネストされたエクスパンダー
            with st.expander("🗂️ Main Category", expanded=True):
                st.write("Main content here")
                
                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("📁 Sub-category 1"):
                        st.write("Nested content 1")
                        st.button("Action 1")
                with col2:
                    with st.expander("📁 Sub-category 2"):
                        st.write("Nested content 2")
                        st.button("Action 2")
    
    @staticmethod
    def tabs_demo(
        example_type: str = "basic",
        num_tabs: int = 3
    ) -> None:
        """
        タブのデモ
        
        Args:
            example_type: 例のタイプ
            num_tabs: タブ数
        """
        st.subheader("📑 Tabs Layout")
        
        if example_type == "basic":
            # 基本的なタブ
            tab_names = [f"Tab {i+1}" for i in range(num_tabs)]
            tabs = st.tabs(tab_names)
            
            for idx, tab in enumerate(tabs):
                with tab:
                    st.header(f"Content of Tab {idx+1}")
                    st.write(f"This is the content of tab {idx+1}")
                    if idx == 0:
                        st.bar_chart(pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C']))
                    elif idx == 1:
                        st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=['X', 'Y']))
                    else:
                        st.metric("Metric", f"{np.random.randint(100, 1000)}", f"+{np.random.randint(1, 20)}%")
                        
        elif example_type == "icons":
            # アイコン付きタブ
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Data", "📈 Charts", "🎯 Metrics", "⚙️ Settings"])
            
            with tab1:
                st.header("Data View")
                df = pd.DataFrame(np.random.randn(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
                st.dataframe(df, use_container_width=True)
                
            with tab2:
                st.header("Charts View")
                chart_type = st.radio("Chart Type", ["Line", "Bar", "Area"], horizontal=True)
                data = pd.DataFrame(np.random.randn(20, 3), columns=['Series 1', 'Series 2', 'Series 3'])
                
                if chart_type == "Line":
                    st.line_chart(data)
                elif chart_type == "Bar":
                    st.bar_chart(data)
                else:
                    st.area_chart(data)
                    
            with tab3:
                st.header("Metrics Dashboard")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Revenue", "$1.25M", "+12%")
                with col2:
                    st.metric("Users", "8,543", "+234")
                with col3:
                    st.metric("Performance", "98.5%", "+2.3%")
                    
            with tab4:
                st.header("Settings")
                st.checkbox("Enable notifications")
                st.slider("Refresh interval (seconds)", 1, 60, 10)
                st.selectbox("Theme", ["Light", "Dark", "Auto"])
                
        elif example_type == "nested":
            # ネストされたタブ
            main_tabs = st.tabs(["🏠 Dashboard", "📊 Analytics", "📝 Reports"])
            
            with main_tabs[0]:
                st.header("Dashboard")
                sub_tabs = st.tabs(["Overview", "Details", "Summary"])
                
                with sub_tabs[0]:
                    st.write("Dashboard Overview")
                    st.info("Key metrics and KPIs")
                    
                with sub_tabs[1]:
                    st.write("Dashboard Details")
                    st.dataframe(pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C']))
                    
                with sub_tabs[2]:
                    st.write("Dashboard Summary")
                    st.success("All systems operational")
                    
            with main_tabs[1]:
                st.header("Analytics")
                st.line_chart(pd.DataFrame(np.random.randn(30, 4), columns=['A', 'B', 'C', 'D']))
                
            with main_tabs[2]:
                st.header("Reports")
                st.selectbox("Select Report", ["Daily", "Weekly", "Monthly"])
                st.button("Generate Report")


class LayoutPatterns:
    """よく使われるレイアウトパターン"""
    
    @staticmethod
    def dashboard_layout():
        """ダッシュボードレイアウトパターン"""
        st.header("📊 Dashboard Layout Pattern")
        
        # ヘッダーメトリクス
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", "$45.2K", "+12%")
        with col2:
            st.metric("New Users", "1,234", "+89")
        with col3:
            st.metric("Conversion", "3.4%", "+0.2%")
        with col4:
            st.metric("Avg. Order", "$123", "-5%", delta_color="inverse")
        
        st.divider()
        
        # メインコンテンツとサイドバー
        main_col, side_col = st.columns([3, 1])
        
        with main_col:
            # タブでコンテンツを整理
            tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Distribution", "📋 Table"])
            
            with tab1:
                st.line_chart(pd.DataFrame(np.random.randn(30, 3), columns=['Product A', 'Product B', 'Product C']))
                
            with tab2:
                st.bar_chart(pd.DataFrame(np.random.randn(10, 4), columns=['Q1', 'Q2', 'Q3', 'Q4']))
                
            with tab3:
                df = pd.DataFrame({
                    'Product': ['A', 'B', 'C', 'D'],
                    'Sales': [1234, 5678, 3456, 7890],
                    'Growth': ['+12%', '+5%', '-3%', '+20%']
                })
                st.dataframe(df, use_container_width=True)
        
        with side_col:
            with st.container(border=True):
                st.subheader("Filters")
                st.date_input("Date Range", key="dash_date")
                st.selectbox("Product", ["All", "A", "B", "C"], key="dash_product")
                st.selectbox("Region", ["All", "North", "South", "East", "West"], key="dash_region")
                st.button("Apply Filters", type="primary", use_container_width=True)
    
    @staticmethod
    def form_layout():
        """フォームレイアウトパターン"""
        st.header("📝 Form Layout Pattern")
        
        with st.container(border=True):
            st.subheader("User Registration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("First Name", key="form_fname")
                st.text_input("Email", key="form_email")
                st.date_input("Date of Birth", key="form_dob")
                
            with col2:
                st.text_input("Last Name", key="form_lname")
                st.text_input("Phone", key="form_phone")
                st.selectbox("Country", ["USA", "Japan", "UK", "Other"], key="form_country")
            
            with st.expander("Additional Information"):
                st.text_area("Bio", height=100, key="form_bio")
                st.multiselect("Interests", ["Technology", "Sports", "Music", "Travel", "Reading"], key="form_interests")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.checkbox("I agree to the terms and conditions", key="form_agree")
            with col2:
                st.button("Cancel", use_container_width=True)
            with col3:
                st.button("Submit", type="primary", use_container_width=True)
    
    @staticmethod
    def card_layout():
        """カードレイアウトパターン"""
        st.header("🃏 Card Layout Pattern")
        
        # 3カラムのカードレイアウト
        cols = st.columns(3, gap="medium")
        
        for idx, col in enumerate(cols):
            with col:
                with st.container(border=True):
                    st.subheader(f"Card {idx + 1}")
                    st.image(f"https://via.placeholder.com/300x150.png?text=Image+{idx+1}")
                    st.write("**Description**")
                    st.write("This is a sample card with some content. Cards are great for organizing related information.")
                    
                    with st.expander("Details"):
                        st.write("Additional details about this card...")
                        st.metric("Value", np.random.randint(100, 1000))
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.button("Action", key=f"card_action_{idx}", use_container_width=True)
                    with col_b:
                        st.button("More", key=f"card_more_{idx}", use_container_width=True)


def render_layout_demo():
    """レイアウトコンポーネントのデモ"""
    st.header("📐 Layout Components Demo")
    
    # メインタブ
    main_tab1, main_tab2, main_tab3 = st.tabs(["🧩 Components", "🎨 Patterns", "📖 Documentation"])
    
    with main_tab1:
        # コンポーネントデモ
        st.markdown("### Layout Components")
        
        # コンポーネント選択
        component = st.selectbox(
            "Select Component",
            ["Columns", "Container", "Expander", "Tabs"]
        )
        
        layout = LayoutComponents()
        
        if component == "Columns":
            st.markdown("#### Columns Layout")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                num_cols = st.slider("Number of columns", 2, 4, 2)
            with col2:
                gap = st.selectbox("Gap size", ["small", "medium", "large"])
            with col3:
                example = st.selectbox("Example type", ["basic", "weighted", "nested"])
            
            st.divider()
            layout.columns_demo(num_cols, gap, example)
            
        elif component == "Container":
            st.markdown("#### Container Layout")
            
            col1, col2 = st.columns(2)
            with col1:
                example = st.selectbox("Example type", ["basic", "dynamic", "placeholder"])
            with col2:
                border = st.checkbox("Show border", value=True)
            
            st.divider()
            layout.container_demo(example, border)
            
        elif component == "Expander":
            st.markdown("#### Expander Layout")
            
            col1, col2 = st.columns(2)
            with col1:
                example = st.selectbox("Example type", ["basic", "multiple", "nested"])
            with col2:
                expanded = st.checkbox("Expanded by default", value=False)
            
            st.divider()
            layout.expander_demo(example, expanded)
            
        else:  # Tabs
            st.markdown("#### Tabs Layout")
            
            col1, col2 = st.columns(2)
            with col1:
                example = st.selectbox("Example type", ["basic", "icons", "nested"])
            with col2:
                if example == "basic":
                    num_tabs = st.slider("Number of tabs", 2, 5, 3)
                else:
                    num_tabs = 3
            
            st.divider()
            layout.tabs_demo(example, num_tabs)
    
    with main_tab2:
        # パターンデモ
        st.markdown("### Common Layout Patterns")
        
        pattern = st.selectbox(
            "Select Pattern",
            ["Dashboard", "Form", "Card Grid"]
        )
        
        st.divider()
        
        patterns = LayoutPatterns()
        
        if pattern == "Dashboard":
            patterns.dashboard_layout()
        elif pattern == "Form":
            patterns.form_layout()
        else:
            patterns.card_layout()
    
    with main_tab3:
        # ドキュメント
        st.markdown("""
        ### 📚 Layout Components Documentation
        
        Layout components help organize and structure your Streamlit applications.
        
        #### Available Components:
        
        1. **Columns** (`st.columns`)
           - Create horizontal layouts
           - Support weighted columns
           - Can be nested
           
        2. **Container** (`st.container`)
           - Group related elements
           - Support dynamic content insertion
           - Optional borders
           
        3. **Expander** (`st.expander`)
           - Hide/show content
           - Great for optional information
           - Can be nested
           
        4. **Tabs** (`st.tabs`)
           - Organize content in tabs
           - Support icons in labels
           - Can be nested
           
        #### Best Practices:
        
        - Use columns for side-by-side layouts
        - Use containers to group related elements
        - Use expanders to reduce visual clutter
        - Use tabs to organize different views
        - Combine components for complex layouts
        - Consider mobile responsiveness
        
        #### Code Examples:
        
        ```python
        # Columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Column 1")
        
        # Weighted columns
        col1, col2 = st.columns([2, 1])
        
        # Container
        with st.container(border=True):
            st.write("Grouped content")
        
        # Expander
        with st.expander("Click to expand"):
            st.write("Hidden content")
        
        # Tabs
        tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
        with tab1:
            st.write("Tab 1 content")
        ```
        """)


if __name__ == "__main__":
    # スタンドアロンテスト
    st.set_page_config(page_title="Layout Components Demo", layout="wide")
    render_layout_demo()