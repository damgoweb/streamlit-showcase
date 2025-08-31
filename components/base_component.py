"""
基底コンポーネントクラス
全てのStreamlitコンポーネントの基底となるクラス
"""

from abc import ABC, abstractmethod
import streamlit as st
from typing import Dict, Any, List, Optional
import json
import textwrap
from pathlib import Path

class BaseComponent(ABC):
    """全コンポーネントの基底クラス"""
    
    def __init__(self, component_id: str, category: str = ""):
        """
        初期化
        
        Args:
            component_id: コンポーネントの一意識別子
            category: コンポーネントのカテゴリ
        """
        self.id = component_id
        self.category = category
        self.metadata = self._load_metadata()
        self.params = {}
        
    def _load_metadata(self) -> Dict[str, Any]:
        """コンポーネントのメタデータを読み込み"""
        # メタデータファイルが存在する場合は読み込み
        meta_file = Path("data/components_meta.json")
        if meta_file.exists():
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                components = data.get('components', [])
                for comp in components:
                    if comp.get('id') == self.id:
                        return comp
        
        # デフォルトのメタデータを返す
        return {
            'id': self.id,
            'name': f'st.{self.id}',
            'category': self.category,
            'description': f'{self.id}コンポーネント',
            'parameters': []
        }
    
    @abstractmethod
    def render_demo(self) -> Any:
        """
        デモをレンダリング
        サブクラスで必ず実装する
        """
        pass
    
    @abstractmethod
    def get_code(self, level: str = "basic") -> str:
        """
        コードを取得
        
        Args:
            level: コードレベル (basic/advanced/full)
        
        Returns:
            フォーマット済みのコード文字列
        """
        pass
    
    def render_parameter_controls(self) -> Dict[str, Any]:
        """パラメータ調整UIをレンダリング"""
        params = {}
        
        if not self.metadata.get('parameters'):
            return params
            
        st.subheader("⚙️ パラメータ設定")
        
        for param in self.metadata['parameters']:
            param_name = param['name']
            param_type = param['type']
            param_desc = param.get('description', '')
            param_default = param.get('default', None)
            
            # パラメータの型に応じてUIを生成
            params[param_name] = self._render_param_control(
                param_name, param_type, param_desc, param_default
            )
        
        self.params = params
        return params
    
    def _render_param_control(self, name: str, param_type: str, 
                             description: str, default: Any) -> Any:
        """個別パラメータコントロールをレンダリング"""
        
        # パラメータ名を人間が読みやすい形式に変換
        display_name = name.replace('_', ' ').title()
        
        if param_type == 'str':
            return st.text_input(
                f"{display_name}",
                value=default or '',
                help=description,
                key=f"{self.id}_{name}"
            )
        elif param_type == 'int':
            return st.number_input(
                f"{display_name}",
                value=default or 0,
                help=description,
                key=f"{self.id}_{name}",
                step=1
            )
        elif param_type == 'float':
            return st.number_input(
                f"{display_name}",
                value=float(default or 0.0),
                help=description,
                key=f"{self.id}_{name}",
                step=0.1
            )
        elif param_type == 'bool':
            return st.checkbox(
                f"{display_name}",
                value=default or False,
                help=description,
                key=f"{self.id}_{name}"
            )
        elif param_type == 'list':
            # リストの場合はテキストエリアで入力（カンマ区切り）
            text_value = st.text_area(
                f"{display_name}",
                value=', '.join(default) if default else '',
                help=f"{description} (カンマ区切りで入力)",
                key=f"{self.id}_{name}"
            )
            return [item.strip() for item in text_value.split(',') if item.strip()]
        else:
            # その他の型はテキスト入力
            return st.text_input(
                f"{display_name}",
                value=str(default) if default else '',
                help=description,
                key=f"{self.id}_{name}"
            )
    
    def display_code(self, syntax_highlight: bool = True) -> None:
        """コードを表示"""
        code = self.get_code()
        if syntax_highlight:
            st.code(code, language='python')
        else:
            st.text(code)
    
    def render_tabs(self) -> None:
        """タブ形式でコードとデモを表示"""
        tab1, tab2, tab3, tab4 = st.tabs([
            "📺 デモ", "💻 基本コード", "🚀 応用コード", "📝 フルコード"
        ])
        
        with tab1:
            st.subheader("実際の動作")
            demo_result = self.render_demo()
            if demo_result is not None:
                st.success(f"結果: {demo_result}")
        
        with tab2:
            st.subheader("基本的な使い方")
            basic_code = self.get_code("basic")
            st.code(basic_code, language='python')
            if st.button("📋 コピー", key=f"copy_basic_{self.id}"):
                st.success("コピーしました！")
        
        with tab3:
            st.subheader("応用的な使い方")
            advanced_code = self.get_code("advanced")
            st.code(advanced_code, language='python')
            if st.button("📋 コピー", key=f"copy_advanced_{self.id}"):
                st.success("コピーしました！")
        
        with tab4:
            st.subheader("完全なサンプルコード")
            full_code = self.get_code("full")
            st.code(full_code, language='python')
            if st.button("📋 コピー", key=f"copy_full_{self.id}"):
                st.success("コピーしました！")
    
    def render_info(self) -> None:
        """コンポーネントの情報を表示"""
        with st.expander("📚 詳細情報", expanded=False):
            st.markdown(f"**カテゴリ**: {self.category}")
            st.markdown(f"**コンポーネント名**: `{self.metadata.get('name', 'N/A')}`")
            st.markdown(f"**説明**: {self.metadata.get('description', 'N/A')}")
            
            if self.metadata.get('tips'):
                st.markdown("**💡 Tips**:")
                for tip in self.metadata['tips']:
                    st.markdown(f"- {tip}")
            
            if self.metadata.get('related'):
                st.markdown("**🔗 関連コンポーネント**:")
                related = ', '.join([f"`st.{comp}`" for comp in self.metadata['related']])
                st.markdown(related)
    
    def format_code_with_params(self, template: str, **kwargs) -> str:
        """
        コードテンプレートにパラメータを埋め込む
        
        Args:
            template: コードテンプレート
            **kwargs: 埋め込むパラメータ
        
        Returns:
            フォーマット済みのコード
        """
        return textwrap.dedent(template).strip().format(**kwargs)
    
    def get_import_statements(self) -> str:
        """必要なimport文を取得"""
        return "import streamlit as st"