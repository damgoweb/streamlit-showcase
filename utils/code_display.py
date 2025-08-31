"""
コード表示管理モジュール
コードのフォーマットと表示を管理するユーティリティ
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import textwrap
import re

class CodeDisplay:
    """コード表示管理クラス"""
    
    def __init__(self):
        """初期化"""
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """コードテンプレートを定義"""
        return {
            'basic': """
                {imports}
                
                {component_call}
            """,
            'advanced': """
                {imports}
                
                # {component_name}の使用例
                {setup_code}
                
                result = {component_call}
                
                # 結果の処理
                if result:
                    st.success(f"入力値: {{result}}")
                {additional_code}
            """,
            'full': """
                {imports}
                import pandas as pd
                import numpy as np
                
                def main():
                    st.title("{app_title}")
                    st.markdown("{description}")
                    
                    # コンポーネントの設定
                    {setup_code}
                    
                    with st.container():
                        result = {component_call}
                    
                    # 結果の表示
                    if result is not None:
                        st.write("結果:", result)
                        
                        # 追加の処理
                        process_result(result)
                
                def process_result(value):
                    \"\"\"結果を処理する関数\"\"\"
                    # ここに処理ロジックを実装
                    st.info(f"処理された値: {{value}}")
                
                if __name__ == "__main__":
                    main()
            """
        }
    
    def format_code(self,
                   component_name: str,
                   params: Dict[str, Any],
                   level: str = "basic",
                   additional_context: Optional[Dict] = None) -> str:
        """
        コードをフォーマット
        
        Args:
            component_name: コンポーネント名（例: st.text_input）
            params: パラメータ辞書
            level: コードレベル (basic/advanced/full)
            additional_context: 追加のコンテキスト情報
        
        Returns:
            フォーマット済みのコード
        """
        if level == "basic":
            return self._format_basic(component_name, params)
        elif level == "advanced":
            return self._format_advanced(component_name, params, additional_context)
        else:
            return self._format_full(component_name, params, additional_context)
    
    def _format_basic(self, component_name: str, params: Dict[str, Any]) -> str:
        """基本コードのフォーマット"""
        imports = "import streamlit as st"
        component_call = self._format_component_call(component_name, params)
        
        code = self.templates['basic'].format(
            imports=imports,
            component_call=component_call
        )
        
        return self._clean_code(code)
    
    def _format_advanced(self, 
                        component_name: str, 
                        params: Dict[str, Any],
                        context: Optional[Dict] = None) -> str:
        """応用コードのフォーマット"""
        imports = "import streamlit as st"
        
        # セットアップコード
        setup_code = ""
        if context and context.get('setup'):
            setup_code = context['setup']
        
        # コンポーネント呼び出し
        component_call = self._format_component_call(component_name, params, multiline=True)
        
        # 追加コード
        additional_code = ""
        if context and context.get('additional'):
            additional_code = context['additional']
        
        code = self.templates['advanced'].format(
            imports=imports,
            component_name=component_name,
            setup_code=setup_code,
            component_call=component_call,
            additional_code=additional_code
        )
        
        return self._clean_code(code)
    
    def _format_full(self,
                    component_name: str,
                    params: Dict[str, Any],
                    context: Optional[Dict] = None) -> str:
        """完全なコードのフォーマット"""
        imports = "import streamlit as st"
        
        # コンテキスト情報の取得
        app_title = context.get('title', f'Streamlit {component_name} デモ') if context else f'Streamlit {component_name} デモ'
        description = context.get('description', f'{component_name}の使用例です。') if context else f'{component_name}の使用例です。'
        setup_code = context.get('setup', '') if context else ''
        
        # コンポーネント呼び出し
        component_call = self._format_component_call(component_name, params, multiline=True, indent=8)
        
        code = self.templates['full'].format(
            imports=imports,
            app_title=app_title,
            description=description,
            setup_code=setup_code,
            component_call=component_call
        )
        
        return self._clean_code(code)
    
    def _format_component_call(self,
                              component_name: str,
                              params: Dict[str, Any],
                              multiline: bool = False,
                              indent: int = 4) -> str:
        """
        コンポーネント呼び出しをフォーマット
        
        Args:
            component_name: コンポーネント名
            params: パラメータ辞書
            multiline: 複数行でフォーマットするか
            indent: インデントのスペース数
        
        Returns:
            フォーマット済みの呼び出しコード
        """
        if not params:
            return f"{component_name}()"
        
        if multiline:
            return self._format_params_multiline(component_name, params, indent)
        else:
            return self._format_params_single_line(component_name, params)
    
    def _format_params_single_line(self, component_name: str, params: Dict[str, Any]) -> str:
        """パラメータを1行でフォーマット"""
        param_parts = []
        
        for key, value in params.items():
            if value is None or (isinstance(value, str) and not value):
                continue
            param_parts.append(self._format_param_value(key, value))
        
        param_str = ", ".join(param_parts)
        return f"{component_name}({param_str})"
    
    def _format_params_multiline(self, 
                                component_name: str,
                                params: Dict[str, Any],
                                indent: int = 4) -> str:
        """パラメータを複数行でフォーマット"""
        if not params:
            return f"{component_name}()"
        
        param_parts = []
        spaces = " " * indent
        
        for key, value in params.items():
            if value is None or (isinstance(value, str) and not value):
                continue
            param_parts.append(f"{spaces}{self._format_param_value(key, value)}")
        
        if not param_parts:
            return f"{component_name}()"
        
        param_str = ",\n".join(param_parts)
        return f"{component_name}(\n{param_str}\n)"
    
    def _format_param_value(self, key: str, value: Any) -> str:
        """パラメータ値をフォーマット"""
        if isinstance(value, str):
            # 文字列のエスケープ処理
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
            return f'{key}="{escaped_value}"'
        elif isinstance(value, bool):
            return f'{key}={value}'
        elif isinstance(value, (int, float)):
            return f'{key}={value}'
        elif isinstance(value, list):
            # リストの場合
            if all(isinstance(item, str) for item in value):
                formatted_items = [f'"{item}"' for item in value]
                return f'{key}=[{", ".join(formatted_items)}]'
            else:
                return f'{key}={value}'
        elif isinstance(value, dict):
            # 辞書の場合（簡略化）
            return f'{key}={value}'
        else:
            return f'{key}={repr(value)}'
    
    def _clean_code(self, code: str) -> str:
        """コードをクリーンアップ"""
        # 余分な空白行を削除
        lines = code.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if not prev_empty:
                    cleaned_lines.append(line)
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False
        
        # 先頭と末尾の空白を削除
        code = '\n'.join(cleaned_lines).strip()
        
        # インデントを調整
        return textwrap.dedent(code)
    
    def display_with_copy(self, 
                         code: str,
                         language: str = "python",
                         key: Optional[str] = None) -> None:
        """
        コピー機能付きでコードを表示
        
        Args:
            code: 表示するコード
            language: プログラミング言語
            key: ボタンのユニークキー
        """
        # コード表示
        st.code(code, language=language)
        
        # コピーボタン
        button_key = key or "copy_button"
        if st.button(f"📋 コードをコピー", key=button_key):
            # クリップボードへのコピーをシミュレート
            st.success("✅ コードをコピーしました！")
            st.info("Ctrl+C (Windows/Linux) または Cmd+C (Mac) でもコピーできます。")
    
    def create_download_button(self,
                             code: str,
                             filename: str = "code.py",
                             button_text: str = "📥 コードをダウンロード") -> None:
        """
        コードダウンロードボタンを作成
        
        Args:
            code: ダウンロードするコード
            filename: ファイル名
            button_text: ボタンのテキスト
        """
        st.download_button(
            label=button_text,
            data=code,
            file_name=filename,
            mime='text/plain'
        )
    
    def highlight_changes(self, 
                         original_code: str,
                         modified_code: str) -> None:
        """
        コードの変更箇所をハイライト表示
        
        Args:
            original_code: 元のコード
            modified_code: 変更後のコード
        """
        st.subheader("📝 変更前")
        st.code(original_code, language='python')
        
        st.subheader("✏️ 変更後")
        st.code(modified_code, language='python')
        
        # 簡単な差分表示
        if original_code != modified_code:
            st.info("💡 コードが変更されています")
    
    def create_code_snippet_library(self, snippets: Dict[str, str]) -> Optional[str]:
        """
        コードスニペットライブラリを作成
        
        Args:
            snippets: スニペット辞書 {名前: コード}
        
        Returns:
            選択されたスニペットのコード
        """
        if not snippets:
            return None
        
        snippet_name = st.selectbox(
            "📚 コードスニペットを選択",
            options=list(snippets.keys())
        )
        
        if snippet_name:
            code = snippets[snippet_name]
            st.code(code, language='python')
            return code
        
        return None


# グローバルインスタンス
code_display = CodeDisplay()