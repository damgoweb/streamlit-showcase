"""
テキスト入力コンポーネント
text_input と text_area の実装
"""

import streamlit as st
from typing import Any, Dict, Optional
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.base_component import BaseComponent
from utils.code_display import code_display
from utils.sample_data import sample_data

class TextInputComponent(BaseComponent):
    """st.text_input コンポーネント"""
    
    def __init__(self):
        super().__init__("text_input", "input_widgets")
        self.metadata = {
            'id': 'text_input',
            'name': 'st.text_input',
            'category': 'input_widgets',
            'description': '単一行のテキスト入力フィールド。ユーザーから短いテキスト入力を受け取るための基本的なコンポーネント。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Enter text',
                    'description': '入力フィールドの上に表示されるラベル'
                },
                {
                    'name': 'value',
                    'type': 'str',
                    'required': False,
                    'default': '',
                    'description': 'デフォルト値'
                },
                {
                    'name': 'max_chars',
                    'type': 'int',
                    'required': False,
                    'default': None,
                    'description': '最大文字数制限'
                },
                {
                    'name': 'key',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ウィジェットの一意識別子'
                },
                {
                    'name': 'type',
                    'type': 'str',
                    'required': False,
                    'default': 'default',
                    'description': '入力タイプ (default/password)'
                },
                {
                    'name': 'help',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'ヘルプテキスト（ツールチップ）'
                },
                {
                    'name': 'autocomplete',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'HTMLのautocomplete属性'
                },
                {
                    'name': 'placeholder',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'プレースホルダーテキスト'
                },
                {
                    'name': 'disabled',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': '入力を無効化'
                },
                {
                    'name': 'label_visibility',
                    'type': 'str',
                    'required': False,
                    'default': 'visible',
                    'description': 'ラベルの表示設定 (visible/hidden/collapsed)'
                }
            ],
            'tips': [
                'type="password" でパスワード入力フィールドとして使用可能',
                'placeholder でユーザーに入力例を提示',
                'max_chars で入力文字数を制限してバリデーション',
                'on_change コールバックで変更を検知（session_stateと組み合わせ）',
                'key パラメータで session_state から値にアクセス可能'
            ],
            'related': ['text_area', 'chat_input', 'number_input'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        # パラメータ設定セクション
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                label = st.text_input(
                    "ラベル",
                    value="お名前を入力してください",
                    key=f"{self.id}_param_label"
                )
                
                value = st.text_input(
                    "デフォルト値",
                    value="",
                    key=f"{self.id}_param_value"
                )
                
                max_chars = st.number_input(
                    "最大文字数 (0=無制限)",
                    min_value=0,
                    value=0,
                    key=f"{self.id}_param_max_chars"
                )
                
                input_type = st.selectbox(
                    "入力タイプ",
                    ["default", "password"],
                    key=f"{self.id}_param_type"
                )
                
                placeholder = st.text_input(
                    "プレースホルダー",
                    value="例: 山田太郎",
                    key=f"{self.id}_param_placeholder"
                )
            
            with col2:
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="全角・半角文字を入力できます",
                    key=f"{self.id}_param_help"
                )
                
                autocomplete = st.selectbox(
                    "オートコンプリート",
                    [None, "off", "on", "name", "email", "username", "current-password", "new-password"],
                    key=f"{self.id}_param_autocomplete"
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
        
        # パラメータを構築
        params = {
            'label': label,
            'key': f"{self.id}_demo_widget"
        }
        
        if value:
            params['value'] = value
        if max_chars > 0:
            params['max_chars'] = max_chars
        if input_type != "default":
            params['type'] = input_type
        if help_text:
            params['help'] = help_text
        if autocomplete:
            params['autocomplete'] = autocomplete
        if placeholder:
            params['placeholder'] = placeholder
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # コンポーネントを実行
        result = st.text_input(**params)
        
        # 結果表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("入力値", f'"{result}"' if result else "(空)")
        with col2:
            st.metric("文字数", len(result))
        with col3:
            st.metric("タイプ", type(result).__name__)
        
        # 入力値の詳細
        if result:
            with st.expander("🔍 入力値の詳細"):
                st.write("**文字列表現:**", repr(result))
                st.write("**長さ:**", len(result))
                st.write("**空白除去:**", result.strip())
                st.write("**大文字変換:**", result.upper())
                st.write("**小文字変換:**", result.lower())
        
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
                'label': 'Enter text',
                'value': '',
                'placeholder': 'Type here...',
                'help': 'Enter some text'
            }
        
        # Noneや空の値を除外
        clean_params = {k: v for k, v in params.items() if v is not None and v != '' and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.text_input", clean_params, level="basic")
        
        elif level == "advanced":
            advanced_code = f"""
import streamlit as st

# セッション状態で値を管理
if 'text_value' not in st.session_state:
    st.session_state.text_value = ''

# text_input with callback
def on_text_change():
    st.success(f"Text changed to: {{st.session_state.text_value}}")

text = st.text_input(
    {self._format_params_for_code(clean_params)},
    key='text_value',
    on_change=on_text_change
)

# 値の検証
if text:
    if len(text) < 3:
        st.warning("Text is too short (minimum 3 characters)")
    else:
        st.success(f"Valid input: {{text}}")
"""
            return advanced_code.strip()
        
        else:  # full
            full_code = f"""
import streamlit as st
import re

def validate_input(text: str) -> tuple[bool, str]:
    \"\"\"入力値を検証\"\"\"
    if not text:
        return False, "入力は必須です"
    if len(text) < 3:
        return False, "3文字以上入力してください"
    if len(text) > 100:
        return False, "100文字以内で入力してください"
    if not re.match(r'^[a-zA-Z0-9\\s]+$', text):
        return False, "英数字とスペースのみ使用可能です"
    return True, "OK"

def main():
    st.title("Text Input Example")
    
    # カスタムCSS
    st.markdown(\"\"\"
    <style>
    .stTextInput > label {{
        color: #FF6B6B;
        font-weight: bold;
    }}
    </style>
    \"\"\", unsafe_allow_html=True)
    
    # フォーム作成
    with st.form("text_form"):
        text_input = st.text_input(
            {self._format_params_for_code(clean_params)}
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("送信", type="primary")
        with col2:
            clear = st.form_submit_button("クリア")
    
    # 処理
    if submit:
        is_valid, message = validate_input(text_input)
        if is_valid:
            st.success(f"✅ {{message}}: '{{text_input}}'")
            # ここでデータ処理や保存を実行
        else:
            st.error(f"❌ {{message}}")
    
    if clear:
        st.rerun()

if __name__ == "__main__":
    main()
"""
            return full_code.strip()
    
    def _format_params_for_code(self, params: Dict) -> str:
        """コード用にパラメータをフォーマット"""
        lines = []
        for key, value in params.items():
            if isinstance(value, str):
                lines.append(f'    {key}="{value}"')
            else:
                lines.append(f'    {key}={value}')
        return ',\n'.join(lines)


class TextAreaComponent(BaseComponent):
    """st.text_area コンポーネント"""
    
    def __init__(self):
        super().__init__("text_area", "input_widgets")
        self.metadata = {
            'id': 'text_area',
            'name': 'st.text_area',
            'category': 'input_widgets',
            'description': '複数行のテキスト入力フィールド。長文やコメント、説明文などの入力に適している。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Enter text',
                    'description': 'テキストエリアのラベル'
                },
                {
                    'name': 'value',
                    'type': 'str',
                    'required': False,
                    'default': '',
                    'description': 'デフォルト値'
                },
                {
                    'name': 'height',
                    'type': 'int',
                    'required': False,
                    'default': None,
                    'description': 'テキストエリアの高さ（ピクセル）'
                },
                {
                    'name': 'max_chars',
                    'type': 'int',
                    'required': False,
                    'default': None,
                    'description': '最大文字数制限'
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
                    'default': None,
                    'description': 'プレースホルダーテキスト'
                },
                {
                    'name': 'disabled',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': '入力を無効化'
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
                'height パラメータでテキストエリアのサイズを調整',
                '改行を含むテキストの入力が可能',
                'Markdownやコード、JSONなどの構造化テキストの入力に便利',
                'value.splitlines() で行ごとに処理可能',
                'len(value.split()) で単語数をカウント'
            ],
            'related': ['text_input', 'code', 'markdown'],
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
                    value="コメントを入力してください",
                    key=f"{self.id}_param_label"
                )
                
                value = st.text_area(
                    "デフォルト値",
                    value="複数行の\nテキストを\n入力できます",
                    height=100,
                    key=f"{self.id}_param_value"
                )
                
                height = st.slider(
                    "高さ (ピクセル)",
                    min_value=50,
                    max_value=500,
                    value=200,
                    step=50,
                    key=f"{self.id}_param_height"
                )
                
                max_chars = st.number_input(
                    "最大文字数 (0=無制限)",
                    min_value=0,
                    value=500,
                    key=f"{self.id}_param_max_chars"
                )
            
            with col2:
                placeholder = st.text_area(
                    "プレースホルダー",
                    value="ここにテキストを入力...\n複数行対応",
                    height=100,
                    key=f"{self.id}_param_placeholder"
                )
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="Ctrl+Enterで送信、Shift+Enterで改行",
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
            'key': f"{self.id}_demo_widget"
        }
        
        if value:
            params['value'] = value
        if height:
            params['height'] = height
        if max_chars > 0:
            params['max_chars'] = max_chars
        if help_text:
            params['help'] = help_text
        if placeholder:
            params['placeholder'] = placeholder
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # コンポーネント実行
        result = st.text_area(**params)
        
        # 結果表示
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("文字数", len(result))
        with col2:
            st.metric("行数", len(result.splitlines()))
        with col3:
            st.metric("単語数", len(result.split()))
        with col4:
            st.metric("空白除く", len(result.replace(" ", "").replace("\n", "")))
        
        # テキスト分析
        if result:
            with st.expander("🔍 テキスト分析"):
                st.write("**プレビュー:**")
                st.text(result[:200] + "..." if len(result) > 200 else result)
                
                st.write("**行ごとの内容:**")
                for i, line in enumerate(result.splitlines()[:10], 1):
                    st.write(f"{i}. {line}")
                
                if len(result.splitlines()) > 10:
                    st.write(f"... 他 {len(result.splitlines()) - 10} 行")
        
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
                'label': 'Enter text',
                'value': '',
                'height': 200,
                'placeholder': 'Type here...'
            }
        
        # Noneや空の値を除外
        clean_params = {k: v for k, v in params.items() if v is not None and v != '' and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.text_area", clean_params, level="basic")
        
        elif level == "advanced":
            advanced_code = f"""
import streamlit as st

# テキストエリアで複数行入力
text = st.text_area(
    {self._format_params_for_code(clean_params)}
)

# テキスト処理
if text:
    # 統計情報
    st.write(f"📊 文字数: {{len(text)}}, 行数: {{len(text.splitlines())}}")
    
    # 行ごとに処理
    lines = text.splitlines()
    st.write("**各行の処理:**")
    for i, line in enumerate(lines, 1):
        if line.strip():  # 空行をスキップ
            st.write(f"{{i}}. {{line}}")
    
    # キーワード検索
    keyword = st.text_input("検索キーワード")
    if keyword and keyword in text:
        st.success(f"'{{keyword}}' が見つかりました！")
"""
            return advanced_code.strip()
        
        else:  # full
            full_code = f"""
import streamlit as st
import re
from collections import Counter

def analyze_text(text: str) -> dict:
    \"\"\"テキストを分析\"\"\"
    words = re.findall(r'\\w+', text.lower())
    return {{
        'char_count': len(text),
        'word_count': len(words),
        'line_count': len(text.splitlines()),
        'unique_words': len(set(words)),
        'most_common': Counter(words).most_common(5)
    }}

def main():
    st.title("Text Area Analysis Tool")
    
    # メインのテキストエリア
    text = st.text_area(
        {self._format_params_for_code(clean_params)}
    )
    
    if text:
        # テキスト分析
        stats = analyze_text(text)
        
        # 統計表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("文字数", stats['char_count'])
            st.metric("単語数", stats['word_count'])
        with col2:
            st.metric("行数", stats['line_count'])
            st.metric("ユニーク単語", stats['unique_words'])
        with col3:
            st.write("**頻出単語 TOP5:**")
            for word, count in stats['most_common']:
                st.write(f"- {{word}}: {{count}}回")
        
        # 変換オプション
        st.subheader("テキスト変換")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("大文字に変換"):
                st.code(text.upper())
            if st.button("小文字に変換"):
                st.code(text.lower())
            if st.button("タイトルケース"):
                st.code(text.title())
        
        with col2:
            if st.button("空白を削除"):
                st.code(text.replace(" ", ""))
            if st.button("改行を削除"):
                st.code(text.replace("\\n", " "))
            if st.button("逆順"):
                st.code(text[::-1])
        
        # エクスポート
        st.download_button(
            label="📥 テキストをダウンロード",
            data=text,
            file_name="text_output.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
"""
            return full_code.strip()
    
    def _format_params_for_code(self, params: Dict) -> str:
        """コード用にパラメータをフォーマット"""
        lines = []
        for key, value in params.items():
            if isinstance(value, str):
                # 改行を含む場合の処理
                if '\n' in value:
                    value = value.replace('\n', '\\n')
                lines.append(f'    {key}="{value}"')
            else:
                lines.append(f'    {key}={value}')
        return ',\n'.join(lines)


# コンポーネントのエクスポート
__all__ = ['TextInputComponent', 'TextAreaComponent']