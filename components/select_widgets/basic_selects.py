"""
選択系基本コンポーネント
checkbox, radio, selectbox, multiselect の実装
"""

import streamlit as st
from typing import Any, Dict, Optional, List, Union
import sys
from pathlib import Path
import random

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.base_component import BaseComponent
from utils.code_display import code_display
from utils.sample_data import sample_data


class CheckboxComponent(BaseComponent):
    """st.checkbox コンポーネント"""
    
    def __init__(self):
        super().__init__("checkbox", "select_widgets")
        self.metadata = {
            'id': 'checkbox',
            'name': 'st.checkbox',
            'category': 'select_widgets',
            'description': 'チェックボックス。True/Falseの二値選択を提供する基本的なウィジェット。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Check me',
                    'description': 'チェックボックスのラベル'
                },
                {
                    'name': 'value',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'デフォルトのチェック状態'
                },
                {
                    'name': 'key',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ウィジェットの一意識別子'
                },
                {
                    'name': 'help',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ヘルプテキスト'
                },
                {
                    'name': 'on_change',
                    'type': 'callable',
                    'required': False,
                    'default': None,
                    'description': '値変更時のコールバック関数'
                },
                {
                    'name': 'disabled',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'チェックボックスを無効化'
                },
                {
                    'name': 'label_visibility',
                    'type': 'str',
                    'required': False,
                    'default': 'visible',
                    'description': 'ラベルの表示設定'
                }
            ],
            'tips': [
                '条件付き表示の制御に便利',
                'value=Trueでデフォルトでチェック済みに',
                'on_changeコールバックで変更を検知',
                '複数のチェックボックスで複数選択UIを構築可能',
                'session_stateと組み合わせて状態を永続化'
            ],
            'related': ['radio', 'toggle', 'multiselect'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        # パラメータ設定
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                label = st.text_input(
                    "ラベル",
                    value="同意する",
                    key=f"{self.id}_param_label"
                )
                
                value = st.checkbox(
                    "デフォルトでチェック",
                    value=False,
                    key=f"{self.id}_param_value"
                )
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="利用規約に同意する場合はチェック",
                    key=f"{self.id}_param_help"
                )
            
            with col2:
                disabled = st.checkbox(
                    "無効化",
                    value=False,
                    key=f"{self.id}_param_disabled"
                )
                
                label_visibility = st.selectbox(
                    "ラベル表示",
                    ["visible", "hidden", "collapsed"],
                    key=f"{self.id}_param_label_visibility"
                )
        
        # パラメータ構築
        params = {
            'label': label,
            'value': value,
            'key': f"{self.id}_demo_widget"
        }
        
        if help_text:
            params['help'] = help_text
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # 単一チェックボックス
        result = st.checkbox(**params)
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("状態", "✅ チェック済み" if result else "⬜ 未チェック")
        with col2:
            st.metric("値", str(result))
        with col3:
            st.metric("タイプ", type(result).__name__)
        
        # 応用例：複数チェックボックス
        st.divider()
        st.subheader("🎯 応用例：複数選択")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**興味のある分野を選択:**")
            interests = {}
            options = ["プログラミング", "データ分析", "機械学習", "Web開発", "モバイル開発"]
            for option in options:
                interests[option] = st.checkbox(option, key=f"interest_{option}")
            
            selected = [k for k, v in interests.items() if v]
            st.write(f"選択された項目: {', '.join(selected) if selected else 'なし'}")
        
        with col2:
            st.write("**設定オプション:**")
            notifications = st.checkbox("通知を有効化", value=True)
            dark_mode = st.checkbox("ダークモード")
            auto_save = st.checkbox("自動保存", value=True)
            
            if notifications:
                st.info("🔔 通知が有効です")
            if dark_mode:
                st.info("🌙 ダークモードが有効です")
            if auto_save:
                st.info("💾 自動保存が有効です")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic", params)
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return result
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if params is None:
            params = {'label': 'Check me', 'value': False}
        
        clean_params = {k: v for k, v in params.items() if v is not None and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.checkbox", clean_params, level="basic")
        
        elif level == "advanced":
            return """import streamlit as st

# 複数チェックボックスで選択
options = ["オプション1", "オプション2", "オプション3"]
selected = {}

for option in options:
    selected[option] = st.checkbox(option)

# 選択された項目を表示
selected_items = [k for k, v in selected.items() if v]
if selected_items:
    st.success(f"選択: {', '.join(selected_items)}")
else:
    st.warning("何も選択されていません")

# 条件付き表示
if st.checkbox("詳細設定を表示"):
    st.write("詳細設定パネル")
    detail1 = st.checkbox("詳細オプション1")
    detail2 = st.checkbox("詳細オプション2")"""
        
        else:  # full
            return """import streamlit as st

def main():
    st.title("チェックボックス設定画面")
    
    # 設定セクション
    st.subheader("⚙️ アプリケーション設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**表示設定**")
        show_header = st.checkbox("ヘッダーを表示", value=True)
        show_sidebar = st.checkbox("サイドバーを表示", value=True)
        show_footer = st.checkbox("フッターを表示", value=False)
        
    with col2:
        st.write("**機能設定**")
        enable_cache = st.checkbox("キャッシュを有効化", value=True)
        enable_debug = st.checkbox("デバッグモード", value=False)
        enable_analytics = st.checkbox("分析を有効化", value=True)
    
    # 設定の保存
    if st.button("設定を保存"):
        settings = {
            'show_header': show_header,
            'show_sidebar': show_sidebar,
            'show_footer': show_footer,
            'enable_cache': enable_cache,
            'enable_debug': enable_debug,
            'enable_analytics': enable_analytics
        }
        st.session_state['settings'] = settings
        st.success("✅ 設定を保存しました")
        
        # 設定内容を表示
        st.json(settings)

if __name__ == "__main__":
    main()"""


class RadioComponent(BaseComponent):
    """st.radio コンポーネント"""
    
    def __init__(self):
        super().__init__("radio", "select_widgets")
        self.metadata = {
            'id': 'radio',
            'name': 'st.radio',
            'category': 'select_widgets',
            'description': 'ラジオボタン。複数の選択肢から1つを選択するウィジェット。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Choose one',
                    'description': 'ラジオボタングループのラベル'
                },
                {
                    'name': 'options',
                    'type': 'list',
                    'required': True,
                    'default': [],
                    'description': '選択肢のリスト'
                },
                {
                    'name': 'index',
                    'type': 'int',
                    'required': False,
                    'default': 0,
                    'description': 'デフォルト選択のインデックス'
                },
                {
                    'name': 'format_func',
                    'type': 'callable',
                    'required': False,
                    'default': None,
                    'description': '表示形式を変換する関数'
                },
                {
                    'name': 'key',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ウィジェットの一意識別子'
                },
                {
                    'name': 'help',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ヘルプテキスト'
                },
                {
                    'name': 'horizontal',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': '水平配置'
                },
                {
                    'name': 'captions',
                    'type': 'list',
                    'required': False,
                    'default': None,
                    'description': '各選択肢の説明文'
                },
                {
                    'name': 'disabled',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'ラジオボタンを無効化'
                },
                {
                    'name': 'label_visibility',
                    'type': 'str',
                    'required': False,
                    'default': 'visible',
                    'description': 'ラベルの表示設定'
                }
            ],
            'tips': [
                'horizontal=Trueで水平配置に',
                'captionsで各選択肢に説明を追加',
                'format_funcで表示形式をカスタマイズ',
                'index=Noneで未選択状態から開始',
                '選択肢が少ない場合（2-5個）に最適'
            ],
            'related': ['selectbox', 'checkbox', 'toggle'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        # パラメータ設定
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                label = st.text_input(
                    "ラベル",
                    value="サイズを選択",
                    key=f"{self.id}_param_label"
                )
                
                options_input = st.text_area(
                    "選択肢（改行区切り）",
                    value="Small\nMedium\nLarge\nExtra Large",
                    key=f"{self.id}_param_options"
                )
                options = [opt.strip() for opt in options_input.split('\n') if opt.strip()]
                
                index = st.number_input(
                    "デフォルト選択インデックス",
                    min_value=0,
                    max_value=max(0, len(options)-1),
                    value=0,
                    key=f"{self.id}_param_index"
                )
                
                horizontal = st.checkbox(
                    "水平配置",
                    value=False,
                    key=f"{self.id}_param_horizontal"
                )
            
            with col2:
                use_captions = st.checkbox(
                    "説明文を追加",
                    value=False,
                    key=f"{self.id}_use_captions"
                )
                
                if use_captions:
                    captions_input = st.text_area(
                        "説明文（改行区切り）",
                        value="コンパクトサイズ\n標準サイズ\n大きめサイズ\n特大サイズ",
                        key=f"{self.id}_param_captions"
                    )
                    captions = [cap.strip() for cap in captions_input.split('\n') if cap.strip()]
                else:
                    captions = None
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="1つ選択してください",
                    key=f"{self.id}_param_help"
                )
                
                disabled = st.checkbox(
                    "無効化",
                    value=False,
                    key=f"{self.id}_param_disabled"
                )
                
                label_visibility = st.selectbox(
                    "ラベル表示",
                    ["visible", "hidden", "collapsed"],
                    key=f"{self.id}_param_label_visibility"
                )
        
        # パラメータ構築
        params = {
            'label': label,
            'options': options,
            'index': index,
            'horizontal': horizontal,
            'key': f"{self.id}_demo_widget"
        }
        
        if captions:
            params['captions'] = captions[:len(options)]
        if help_text:
            params['help'] = help_text
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # ラジオボタン
        result = st.radio(**params)
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("選択値", result)
        with col2:
            st.metric("インデックス", options.index(result) if result in options else -1)
        with col3:
            st.metric("タイプ", type(result).__name__)
        
        # 応用例
        st.divider()
        st.subheader("🎯 応用例：条件分岐")
        
        mode = st.radio(
            "表示モード",
            ["テーブル", "グラフ", "統計"],
            horizontal=True
        )
        
        if mode == "テーブル":
            df = sample_data.generate_dataframe(rows=5)
            st.dataframe(df)
        elif mode == "グラフ":
            chart_data = sample_data.generate_chart_data("line", 20)
            st.line_chart(chart_data.set_index('x'))
        else:  # 統計
            st.write("**統計情報**")
            col1, col2, col3 = st.columns(3)
            col1.metric("平均", "75.3")
            col2.metric("中央値", "72.5")
            col3.metric("標準偏差", "12.4")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic", params)
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return result
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if params is None:
            params = {
                'label': 'Choose one',
                'options': ['Option 1', 'Option 2', 'Option 3'],
                'index': 0
            }
        
        clean_params = {k: v for k, v in params.items() if v is not None and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.radio", clean_params, level="basic")
        
        elif level == "advanced":
            return """import streamlit as st

# ラジオボタンで選択
genre = st.radio(
    "好きな音楽ジャンルは？",
    ["ロック", "ポップ", "ジャズ", "クラシック", "その他"],
    index=0,
    horizontal=True,
    help="1つ選択してください"
)

# 選択に応じた処理
if genre == "ロック":
    st.write("🎸 ロックンロール！")
    bands = ["Queen", "Led Zeppelin", "The Beatles"]
    selected_band = st.radio("好きなバンドは？", bands)
elif genre == "ジャズ":
    st.write("🎺 ジャズはいいですね！")
    artists = ["Miles Davis", "John Coltrane", "Bill Evans"]
    selected_artist = st.radio("好きなアーティストは？", artists)
else:
    st.write(f"🎵 {genre}が好きなんですね！")"""
        
        else:  # full
            return """import streamlit as st
import pandas as pd

def main():
    st.title("ラジオボタンによる設定画面")
    
    # 表示設定
    st.subheader("📊 データ表示設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 表示形式
        display_format = st.radio(
            "表示形式",
            ["テーブル", "グラフ", "カード", "リスト"],
            index=0,
            captions=[
                "データを表形式で表示",
                "視覚的なグラフ表示",
                "カード形式で表示",
                "シンプルなリスト表示"
            ]
        )
        
    with col2:
        # ソート順
        sort_order = st.radio(
            "ソート順",
            ["昇順", "降順", "カスタム"],
            index=0,
            horizontal=True
        )
        
        # フィルタ
        filter_type = st.radio(
            "フィルタ設定",
            ["すべて", "アクティブのみ", "非アクティブのみ"],
            index=0
        )
    
    # サンプルデータ生成
    df = pd.DataFrame({
        'ID': range(1, 6),
        'Name': ['Item A', 'Item B', 'Item C', 'Item D', 'Item E'],
        'Status': ['Active', 'Inactive', 'Active', 'Active', 'Inactive'],
        'Value': [100, 200, 150, 300, 250]
    })
    
    # フィルタ適用
    if filter_type == "アクティブのみ":
        df = df[df['Status'] == 'Active']
    elif filter_type == "非アクティブのみ":
        df = df[df['Status'] == 'Inactive']
    
    # ソート適用
    if sort_order == "昇順":
        df = df.sort_values('Value')
    elif sort_order == "降順":
        df = df.sort_values('Value', ascending=False)
    
    # 表示
    st.divider()
    st.subheader("結果表示")
    
    if display_format == "テーブル":
        st.dataframe(df, use_container_width=True)
    elif display_format == "グラフ":
        st.bar_chart(df.set_index('Name')['Value'])
    elif display_format == "カード":
        cols = st.columns(3)
        for idx, row in df.iterrows():
            with cols[idx % 3]:
                st.metric(row['Name'], row['Value'], row['Status'])
    else:  # リスト
        for _, row in df.iterrows():
            st.write(f"- {row['Name']}: {row['Value']} ({row['Status']})")

if __name__ == "__main__":
    main()"""


class SelectboxComponent(BaseComponent):
    """st.selectbox コンポーネント"""
    
    def __init__(self):
        super().__init__("selectbox", "select_widgets")
        self.metadata = {
            'id': 'selectbox',
            'name': 'st.selectbox',
            'category': 'select_widgets',
            'description': 'ドロップダウン選択ボックス。多数の選択肢から1つを選択する場合に最適。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Select',
                    'description': 'セレクトボックスのラベル'
                },
                {
                    'name': 'options',
                    'type': 'list',
                    'required': True,
                    'default': [],
                    'description': '選択肢のリスト'
                },
                {
                    'name': 'index',
                    'type': 'int',
                    'required': False,
                    'default': 0,
                    'description': 'デフォルト選択のインデックス'
                },
                {
                    'name': 'format_func',
                    'type': 'callable',
                    'required': False,
                    'default': None,
                    'description': '表示形式を変換する関数'
                },
                {
                    'name': 'key',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ウィジェットの一意識別子'
                },
                {
                    'name': 'help',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ヘルプテキスト'
                },
                {
                    'name': 'placeholder',
                    'type': 'str',
                    'required': False,
                    'default': 'Choose an option',
                    'description': 'プレースホルダーテキスト'
                },
                {
                    'name': 'disabled',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'セレクトボックスを無効化'
                },
                {
                    'name': 'label_visibility',
                    'type': 'str',
                    'required': False,
                    'default': 'visible',
                    'description': 'ラベルの表示設定'
                }
            ],
            'tips': [
                '選択肢が多い場合（6個以上）に適している',
                'placeholder でプレースホルダーテキストを設定',
                'format_func で表示と実際の値を分離',
                'index=None で未選択状態から開始',
                '検索機能付きで大量の選択肢も扱いやすい'
            ],
            'related': ['multiselect', 'radio', 'select_slider'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        # パラメータ設定
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                label = st.text_input(
                    "ラベル",
                    value="都道府県を選択",
                    key=f"{self.id}_param_label"
                )
                
                # サンプル選択肢
                options_type = st.radio(
                    "選択肢タイプ",
                    ["都道府県", "プログラミング言語", "カスタム"],
                    key=f"{self.id}_options_type"
                )
                
                if options_type == "都道府県":
                    options = ["東京都", "大阪府", "愛知県", "福岡県", "北海道", 
                              "宮城県", "広島県", "京都府", "神奈川県", "埼玉県"]
                elif options_type == "プログラミング言語":
                    options = ["Python", "JavaScript", "Java", "C++", "Go", 
                              "Rust", "TypeScript", "Ruby", "PHP", "Swift"]
                else:
                    options_input = st.text_area(
                        "選択肢（改行区切り）",
                        value="Option 1\nOption 2\nOption 3",
                        key=f"{self.id}_custom_options"
                    )
                    options = [opt.strip() for opt in options_input.split('\n') if opt.strip()]
                
                index = st.number_input(
                    "デフォルト選択インデックス",
                    min_value=0,
                    max_value=max(0, len(options)-1),
                    value=0,
                    key=f"{self.id}_param_index"
                )
            
            with col2:
                placeholder = st.text_input(
                    "プレースホルダー",
                    value="選択してください",
                    key=f"{self.id}_param_placeholder"
                )
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="ドロップダウンから選択",
                    key=f"{self.id}_param_help"
                )
                
                disabled = st.checkbox(
                    "無効化",
                    value=False,
                    key=f"{self.id}_param_disabled"
                )
                
                label_visibility = st.selectbox(
                    "ラベル表示",
                    ["visible", "hidden", "collapsed"],
                    key=f"{self.id}_param_label_visibility"
                )
        
        # パラメータ構築
        params = {
            'label': label,
            'options': options,
            'index': index,
            'placeholder': placeholder,
            'key': f"{self.id}_demo_widget"
        }
        
        if help_text:
            params['help'] = help_text
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # セレクトボックス
        result = st.selectbox(**params)
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("選択値", result)
        with col2:
            st.metric("インデックス", options.index(result) if result in options else -1)
        with col3:
            st.metric("選択肢数", len(options))
        
        # 応用例：連動セレクトボックス
        st.divider()
        st.subheader("🎯 応用例：連動セレクトボックス")
        
        # カテゴリ選択
        categories = {
            "フルーツ": ["りんご", "みかん", "ぶどう", "いちご", "メロン"],
            "野菜": ["トマト", "きゅうり", "レタス", "にんじん", "たまねぎ"],
            "肉類": ["牛肉", "豚肉", "鶏肉", "羊肉", "鴨肉"]
        }
        
        category = st.selectbox(
            "カテゴリを選択",
            list(categories.keys())
        )
        
        item = st.selectbox(
            f"{category}を選択",
            categories[category]
        )
        
        st.info(f"選択: {category} → {item}")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic", params)
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return result
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if params is None:
            params = {
                'label': 'Select',
                'options': ['Option 1', 'Option 2', 'Option 3'],
                'index': 0
            }
        
        clean_params = {k: v for k, v in params.items() if v is not None and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.selectbox", clean_params, level="basic")
        
        elif level == "advanced":
            return """import streamlit as st

# 連動するセレクトボックス
country = st.selectbox(
    "国を選択",
    ["日本", "アメリカ", "イギリス", "フランス"]
)

# 国に応じて都市を変更
cities = {
    "日本": ["東京", "大阪", "京都", "福岡"],
    "アメリカ": ["ニューヨーク", "ロサンゼルス", "シカゴ", "ヒューストン"],
    "イギリス": ["ロンドン", "マンチェスター", "リバプール", "エディンバラ"],
    "フランス": ["パリ", "マルセイユ", "リヨン", "トゥールーズ"]
}

city = st.selectbox(
    "都市を選択",
    cities[country]
)

st.success(f"選択: {country} - {city}")

# format_funcの使用例
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [
    Person("太郎", 25),
    Person("花子", 30),
    Person("次郎", 35)
]

selected_person = st.selectbox(
    "人を選択",
    people,
    format_func=lambda p: f"{p.name} ({p.age}歳)"
)

if selected_person:
    st.write(f"選択された人: {selected_person.name}, 年齢: {selected_person.age}")"""
        
        else:  # full
            return """import streamlit as st
import pandas as pd

def main():
    st.title("セレクトボックスによるフィルタリング")
    
    # サンプルデータ
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Department': ['Sales', 'Engineering', 'Sales', 'HR', 'Engineering'],
        'Location': ['Tokyo', 'Osaka', 'Tokyo', 'Kyoto', 'Osaka'],
        'Salary': [50000, 60000, 55000, 45000, 65000]
    })
    
    st.subheader("🔍 フィルタ設定")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 部署フィルタ
        departments = ['All'] + list(df['Department'].unique())
        selected_dept = st.selectbox(
            "部署",
            departments,
            index=0
        )
    
    with col2:
        # 場所フィルタ
        locations = ['All'] + list(df['Location'].unique())
        selected_loc = st.selectbox(
            "勤務地",
            locations,
            index=0
        )
    
    with col3:
        # ソート条件
        sort_by = st.selectbox(
            "ソート基準",
            ['Name', 'Department', 'Location', 'Salary'],
            index=0
        )
    
    # フィルタリング
    filtered_df = df.copy()
    
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    
    if selected_loc != 'All':
        filtered_df = filtered_df[filtered_df['Location'] == selected_loc]
    
    # ソート
    filtered_df = filtered_df.sort_values(by=sort_by)
    
    # 結果表示
    st.divider()
    st.subheader("📊 結果")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.dataframe(filtered_df, use_container_width=True)
    
    with col2:
        st.metric("件数", len(filtered_df))
        if len(filtered_df) > 0:
            st.metric("平均給与", f"${filtered_df['Salary'].mean():,.0f}")

if __name__ == "__main__":
    main()"""


class MultiselectComponent(BaseComponent):
    """st.multiselect コンポーネント"""
    
    def __init__(self):
        super().__init__("multiselect", "select_widgets")
        self.metadata = {
            'id': 'multiselect',
            'name': 'st.multiselect',
            'category': 'select_widgets',
            'description': '複数選択ドロップダウン。複数の選択肢から任意の数を選択できる。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Select multiple',
                    'description': 'マルチセレクトのラベル'
                },
                {
                    'name': 'options',
                    'type': 'list',
                    'required': True,
                    'default': [],
                    'description': '選択肢のリスト'
                },
                {
                    'name': 'default',
                    'type': 'list',
                    'required': False,
                    'default': None,
                    'description': 'デフォルト選択項目'
                },
                {
                    'name': 'format_func',
                    'type': 'callable',
                    'required': False,
                    'default': None,
                    'description': '表示形式を変換する関数'
                },
                {
                    'name': 'key',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ウィジェットの一意識別子'
                },
                {
                    'name': 'help',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ヘルプテキスト'
                },
                {
                    'name': 'max_selections',
                    'type': 'int',
                    'required': False,
                    'default': None,
                    'description': '最大選択数'
                },
                {
                    'name': 'placeholder',
                    'type': 'str',
                    'required': False,
                    'default': 'Choose options',
                    'description': 'プレースホルダーテキスト'
                },
                {
                    'name': 'disabled',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'マルチセレクトを無効化'
                },
                {
                    'name': 'label_visibility',
                    'type': 'str',
                    'required': False,
                    'default': 'visible',
                    'description': 'ラベルの表示設定'
                }
            ],
            'tips': [
                'タグ選択やカテゴリ選択に最適',
                'max_selections で選択数を制限',
                '選択された項目はタグとして表示',
                'リストが返されるので len() で選択数を確認',
                '検索機能付きで大量の選択肢も扱いやすい'
            ],
            'related': ['selectbox', 'checkbox', 'tags'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        # パラメータ設定
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                label = st.text_input(
                    "ラベル",
                    value="スキルを選択",
                    key=f"{self.id}_param_label"
                )
                
                # サンプル選択肢
                options_type = st.radio(
                    "選択肢タイプ",
                    ["プログラミングスキル", "言語", "カスタム"],
                    key=f"{self.id}_options_type"
                )
                
                if options_type == "プログラミングスキル":
                    options = ["Python", "JavaScript", "SQL", "Git", "Docker", 
                              "AWS", "React", "Django", "FastAPI", "MongoDB"]
                elif options_type == "言語":
                    options = ["日本語", "英語", "中国語", "韓国語", "スペイン語",
                              "フランス語", "ドイツ語", "イタリア語", "ロシア語", "アラビア語"]
                else:
                    options_input = st.text_area(
                        "選択肢（改行区切り）",
                        value="Item 1\nItem 2\nItem 3\nItem 4\nItem 5",
                        key=f"{self.id}_custom_options"
                    )
                    options = [opt.strip() for opt in options_input.split('\n') if opt.strip()]
                
                # デフォルト選択
                default_count = st.number_input(
                    "デフォルト選択数",
                    min_value=0,
                    max_value=len(options),
                    value=min(2, len(options)),
                    key=f"{self.id}_default_count"
                )
                default = options[:default_count] if default_count > 0 else None
            
            with col2:
                max_selections = st.number_input(
                    "最大選択数（0=無制限）",
                    min_value=0,
                    value=0,
                    key=f"{self.id}_param_max"
                )
                
                placeholder = st.text_input(
                    "プレースホルダー",
                    value="選択してください",
                    key=f"{self.id}_param_placeholder"
                )
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="複数選択可能です",
                    key=f"{self.id}_param_help"
                )
                
                disabled = st.checkbox(
                    "無効化",
                    value=False,
                    key=f"{self.id}_param_disabled"
                )
                
                label_visibility = st.selectbox(
                    "ラベル表示",
                    ["visible", "hidden", "collapsed"],
                    key=f"{self.id}_param_label_visibility"
                )
        
        # パラメータ構築
        params = {
            'label': label,
            'options': options,
            'placeholder': placeholder,
            'key': f"{self.id}_demo_widget"
        }
        
        if default:
            params['default'] = default
        if max_selections > 0:
            params['max_selections'] = max_selections
        if help_text:
            params['help'] = help_text
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # マルチセレクト
        result = st.multiselect(**params)
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("選択数", len(result))
        with col2:
            st.metric("選択肢総数", len(options))
        with col3:
            st.metric("未選択数", len(options) - len(result))
        
        # 選択項目の表示
        if result:
            st.success(f"選択された項目: {', '.join(result)}")
        else:
            st.info("項目が選択されていません")
        
        # 応用例：タグフィルタ
        st.divider()
        st.subheader("🎯 応用例：タグによるフィルタリング")
        
        # サンプルデータ
        articles = [
            {"title": "Python入門", "tags": ["Python", "プログラミング", "初心者"]},
            {"title": "機械学習の基礎", "tags": ["Python", "機械学習", "AI"]},
            {"title": "Webアプリ開発", "tags": ["JavaScript", "React", "Web"]},
            {"title": "データ分析入門", "tags": ["Python", "データ分析", "pandas"]},
            {"title": "クラウド入門", "tags": ["AWS", "クラウド", "インフラ"]}
        ]
        
        # 全タグを抽出
        all_tags = list(set(tag for article in articles for tag in article["tags"]))
        
        # タグ選択
        selected_tags = st.multiselect(
            "タグでフィルタ",
            all_tags,
            default=None,
            placeholder="タグを選択"
        )
        
        # フィルタリング
        if selected_tags:
            filtered = [a for a in articles if any(tag in selected_tags for tag in a["tags"])]
            st.write(f"**検索結果: {len(filtered)}件**")
            for article in filtered:
                st.write(f"- {article['title']} (タグ: {', '.join(article['tags'])})")
        else:
            st.write("**全記事**")
            for article in articles:
                st.write(f"- {article['title']} (タグ: {', '.join(article['tags'])})")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic", params)
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return result
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if params is None:
            params = {
                'label': 'Select multiple',
                'options': ['Option 1', 'Option 2', 'Option 3'],
                'default': []
            }
        
        clean_params = {k: v for k, v in params.items() if v is not None and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.multiselect", clean_params, level="basic")
        
        elif level == "advanced":
            return """import streamlit as st

# スキル選択
skills = st.multiselect(
    "保有スキルを選択してください",
    ["Python", "JavaScript", "SQL", "Git", "Docker", 
     "AWS", "React", "Django", "FastAPI", "MongoDB"],
    default=["Python", "Git"],
    max_selections=5,
    help="最大5つまで選択可能"
)

if skills:
    st.success(f"選択されたスキル ({len(skills)}個): {', '.join(skills)}")
    
    # スキルレベルの評価
    skill_levels = {}
    for skill in skills:
        skill_levels[skill] = st.slider(
            f"{skill}のレベル",
            1, 5, 3,
            help="1:初心者 - 5:エキスパート"
        )
    
    # 結果表示
    st.write("**スキル評価:**")
    for skill, level in skill_levels.items():
        st.write(f"- {skill}: {'⭐' * level}")
else:
    st.warning("スキルを選択してください")"""
        
        else:  # full
            return """import streamlit as st
import pandas as pd

def main():
    st.title("マルチセレクトによるデータフィルタリング")
    
    # サンプルデータ
    data = {
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                   'Webcam', 'Microphone', 'Speaker', 'USB Hub', 'Cable'],
        'Category': ['Computer', 'Accessory', 'Accessory', 'Computer', 'Audio',
                    'Video', 'Audio', 'Audio', 'Accessory', 'Accessory'],
        'Brand': ['Dell', 'Logitech', 'Logitech', 'LG', 'Sony',
                 'Logitech', 'Blue', 'JBL', 'Anker', 'Belkin'],
        'Price': [1200, 25, 50, 300, 150, 80, 120, 200, 30, 15],
        'Stock': [10, 50, 30, 15, 20, 25, 12, 18, 40, 100]
    }
    df = pd.DataFrame(data)
    
    st.subheader("🔍 フィルタ設定")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # カテゴリフィルタ
        categories = st.multiselect(
            "カテゴリ",
            df['Category'].unique(),
            default=df['Category'].unique(),
            placeholder="カテゴリを選択"
        )
    
    with col2:
        # ブランドフィルタ
        brands = st.multiselect(
            "ブランド",
            df['Brand'].unique(),
            default=None,
            placeholder="ブランドを選択"
        )
    
    with col3:
        # 価格範囲
        price_range = st.slider(
            "価格範囲",
            int(df['Price'].min()),
            int(df['Price'].max()),
            (int(df['Price'].min()), int(df['Price'].max()))
        )
    
    # フィルタリング
    filtered_df = df[
        (df['Category'].isin(categories) if categories else True) &
        (df['Brand'].isin(brands) if brands else df['Brand'].notna()) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1])
    ]
    
    # 結果表示
    st.divider()
    st.subheader("📊 フィルタ結果")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("商品数", len(filtered_df))
    col2.metric("平均価格", f"${filtered_df['Price'].mean():.0f}" if len(filtered_df) > 0 else "N/A")
    col3.metric("在庫合計", filtered_df['Stock'].sum() if len(filtered_df) > 0 else 0)
    
    # データ表示
    st.dataframe(filtered_df, use_container_width=True)
    
    # 選択された商品の詳細
    if len(filtered_df) > 0:
        selected_products = st.multiselect(
            "商品を選択して詳細を表示",
            filtered_df['Product'].tolist(),
            max_selections=3
        )
        
        if selected_products:
            st.subheader("📦 選択された商品の詳細")
            for product in selected_products:
                product_data = filtered_df[filtered_df['Product'] == product].iloc[0]
                with st.expander(f"{product}"):
                    st.write(f"**カテゴリ**: {product_data['Category']}")
                    st.write(f"**ブランド**: {product_data['Brand']}")
                    st.write(f"**価格**: ${product_data['Price']}")
                    st.write(f"**在庫**: {product_data['Stock']}個")

if __name__ == "__main__":
    main()"""


# コンポーネントのエクスポート
__all__ = ['CheckboxComponent', 'RadioComponent', 'SelectboxComponent', 'MultiselectComponent']