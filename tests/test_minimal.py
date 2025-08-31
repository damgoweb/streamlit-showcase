import streamlit as st
import sys
import os

st.title("環境確認")

# 現在のディレクトリ
st.write("Current directory:", os.getcwd())

# utilsディレクトリの確認
utils_exists = os.path.exists("utils")
st.write(f"utils directory exists: {utils_exists}")

if utils_exists:
    files = os.listdir("utils")
    st.write("Files in utils:", files)

# Pythonパスに追加してインポート試行
try:
    sys.path.insert(0, os.getcwd())
    from utils.state_manager import state_manager
    st.success("✅ インポート成功！")
    
    # 簡単なテスト
    state_manager.set("test", "OK")
    value = state_manager.get("test")
    st.write(f"テスト値: {value}")
    
except ImportError as e:
    st.error(f"❌ インポートエラー: {e}")
    st.write("sys.path:", sys.path[:3])
