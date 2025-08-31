# test_utils.py として保存して実行
import streamlit as st
from utils.state_manager import state_manager
from utils.code_display import code_display
from utils.sample_data import sample_data
from utils.error_handler import error_handler

st.title("ユーティリティ動作確認")

# StateManager テスト
st.header("1. StateManager")
state_manager.set("test_key", "test_value")
st.write(f"取得した値: {state_manager.get('test_key')}")

# CodeDisplay テスト
st.header("2. CodeDisplay")
code = code_display.format_code("st.text_input", {"label": "名前", "value": "太郎"})
code_display.display_with_copy(code)

# SampleData テスト
st.header("3. SampleData")
df = sample_data.generate_dataframe(rows=5)
st.dataframe(df)

# ErrorHandler テスト
st.header("4. ErrorHandler")
@error_handler.error_boundary(message="テストエラー")
def test_function():
    return 1 / 1  # エラーを起こしたい場合は 1 / 0 に変更

result = test_function()
st.write(f"結果: {result}")