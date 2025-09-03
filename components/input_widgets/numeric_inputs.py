"""
数値入力コンポーネント
number_input の実装
"""

import streamlit as st
from typing import Any, Dict, Optional, Union
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.base_component import BaseComponent
from utils.code_display import code_display
from utils.sample_data import sample_data


class NumberInputComponent(BaseComponent):
    """st.number_input コンポーネント"""
    
    def __init__(self):
        super().__init__("number_input", "input_widgets")
        self.metadata = {
            'id': 'number_input',
            'name': 'st.number_input',
            'category': 'input_widgets',
            'description': '数値入力フィールド。整数または浮動小数点数の入力を受け付ける。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Enter a number',
                    'description': '入力フィールドのラベル'
                },
                {
                    'name': 'min_value',
                    'type': 'float/int',
                    'required': False,
                    'default': None,
                    'description': '最小値'
                },
                {
                    'name': 'max_value',
                    'type': 'float/int',
                    'required': False,
                    'default': None,
                    'description': '最大値'
                },
                {
                    'name': 'value',
                    'type': 'float/int',
                    'required': False,
                    'default': 'min_value or 0',
                    'description': 'デフォルト値'
                },
                {
                    'name': 'step',
                    'type': 'float/int',
                    'required': False,
                    'default': 1,
                    'description': '増減ステップ'
                },
                {
                    'name': 'format',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': '表示フォーマット（printf形式）'
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
                'stepパラメータで増減の単位を設定可能',
                'format="%d"で整数表示、format="%.2f"で小数点2桁表示',
                'min_value/max_valueで入力範囲を制限',
                '矢印キーまたは+/-ボタンで値を調整',
                'value引数にintを渡すと整数モード、floatを渡すと小数モード'
            ],
            'related': ['slider', 'text_input', 'metric'],
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
                    value="数値を入力してください",
                    key=f"{self.id}_param_label"
                )
                
                # 数値タイプ選択
                number_type = st.radio(
                    "数値タイプ",
                    ["整数 (int)", "小数 (float)"],
                    key=f"{self.id}_param_type"
                )
                
                is_float = number_type == "小数 (float)"
                
                # 最小値・最大値
                min_value = st.number_input(
                    "最小値",
                    value=0.0 if is_float else 0,
                    key=f"{self.id}_param_min"
                )
                
                max_value = st.number_input(
                    "最大値",
                    value=100.0 if is_float else 100,
                    key=f"{self.id}_param_max"
                )
                
                # デフォルト値
                if is_float:
                    value = st.number_input(
                        "デフォルト値",
                        min_value=float(min_value),
                        max_value=float(max_value),
                        value=50.0,
                        key=f"{self.id}_param_value"
                    )
                    step = st.number_input(
                        "ステップ",
                        value=0.1,
                        key=f"{self.id}_param_step"
                    )
                else:
                    value = st.number_input(
                        "デフォルト値",
                        min_value=int(min_value),
                        max_value=int(max_value),
                        value=50,
                        key=f"{self.id}_param_value"
                    )
                    step = st.number_input(
                        "ステップ",
                        value=1,
                        key=f"{self.id}_param_step"
                    )
            
            with col2:
                format_str = st.text_input(
                    "フォーマット文字列",
                    value="%.2f" if is_float else "%d",
                    help="printf形式: %d(整数), %.2f(小数点2桁)",
                    key=f"{self.id}_param_format"
                )
                
                placeholder = st.text_input(
                    "プレースホルダー",
                    value="",
                    key=f"{self.id}_param_placeholder"
                )
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="矢印キーまたは+/-ボタンで調整",
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
        
        # パラメータを構築
        params = {
            'label': label,
            'min_value': min_value if is_float else int(min_value),
            'max_value': max_value if is_float else int(max_value),
            'value': value,
            'step': step,
            'key': f"{self.id}_demo_widget"
        }
        
        if format_str:
            params['format'] = format_str
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
        
        # コンポーネントを実行
        result = st.number_input(**params)
        
        # 結果表示
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("入力値", result)
        with col2:
            st.metric("タイプ", type(result).__name__)
        with col3:
            st.metric("2倍", result * 2)
        with col4:
            st.metric("平方", result ** 2)
        
        # 詳細分析
        with st.expander("🔍 数値の詳細"):
            st.write("**値の情報:**")
            st.write(f"- 絶対値: {abs(result)}")
            st.write(f"- 符号: {'正' if result > 0 else '負' if result < 0 else 'ゼロ'}")
            if isinstance(result, float):
                st.write(f"- 整数部: {int(result)}")
                st.write(f"- 小数部: {result - int(result):.4f}")
            st.write(f"- 16進数: {hex(int(result))}")
            st.write(f"- 2進数: {bin(int(result))}")
            
            # 範囲チェック
            st.write("**範囲チェック:**")
            progress = (result - min_value) / (max_value - min_value) if max_value > min_value else 0
            st.progress(progress)
            st.write(f"範囲内の位置: {progress:.1%}")
        
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
                'label': 'Enter a number',
                'min_value': 0,
                'max_value': 100,
                'value': 50,
                'step': 1
            }
        
        # keyパラメータを除外
        clean_params = {k: v for k, v in params.items() if v is not None and k != 'key'}
        
        if level == "basic":
            return code_display.format_code("st.number_input", clean_params, level="basic")
        
        elif level == "advanced":
            advanced_code = f"""
import streamlit as st

# 数値入力と計算
number = st.number_input(
    {self._format_params_for_code(clean_params)}
)

# 計算結果
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("2倍", number * 2)
with col2:
    st.metric("平方", number ** 2)
with col3:
    st.metric("平方根", number ** 0.5 if number >= 0 else "N/A")

# 範囲チェック
if number < {clean_params.get('min_value', 0)}:
    st.error("値が小さすぎます")
elif number > {clean_params.get('max_value', 100)}:
    st.error("値が大きすぎます")
else:
    st.success(f"有効な値: {{number}}")
"""
            return advanced_code.strip()
        
        else:  # full
            full_code = f"""
import streamlit as st
import pandas as pd
import numpy as np

def calculate_statistics(value: float) -> dict:
    \"\"\"統計情報を計算\"\"\"
    return {{
        'mean': value,
        'double': value * 2,
        'square': value ** 2,
        'sqrt': np.sqrt(abs(value)),
        'log': np.log(value) if value > 0 else None,
        'sin': np.sin(value),
        'cos': np.cos(value)
    }}

def main():
    st.title("Number Input Calculator")
    
    # メイン入力
    col1, col2 = st.columns([2, 1])
    
    with col1:
        number = st.number_input(
            {self._format_params_for_code(clean_params)}
        )
    
    with col2:
        operation = st.selectbox(
            "演算",
            ["加算", "減算", "乗算", "除算", "べき乗"]
        )
        
        operand = st.number_input(
            "演算子",
            value=2.0
        )
    
    # 計算実行
    if operation == "加算":
        result = number + operand
    elif operation == "減算":
        result = number - operand
    elif operation == "乗算":
        result = number * operand
    elif operation == "除算":
        result = number / operand if operand != 0 else "エラー: ゼロ除算"
    else:  # べき乗
        result = number ** operand
    
    # 結果表示
    st.subheader("計算結果")
    if isinstance(result, (int, float)):
        st.success(f"{{number}} {{operation}} {{operand}} = {{result}}")
        
        # 統計情報
        stats = calculate_statistics(result)
        
        cols = st.columns(4)
        for i, (key, value) in enumerate(stats.items()):
            if value is not None:
                cols[i % 4].metric(key.title(), f"{{value:.4f}}")
    else:
        st.error(result)
    
    # データ履歴
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if st.button("履歴に追加"):
        st.session_state.history.append({{
            'number': number,
            'operation': operation,
            'operand': operand,
            'result': result if isinstance(result, (int, float)) else None
        }})
    
    if st.session_state.history:
        st.subheader("計算履歴")
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
        
        if st.button("履歴をクリア"):
            st.session_state.history = []
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


# コンポーネントのエクスポート
__all__ = ['NumberInputComponent']