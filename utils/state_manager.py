"""
アプリケーション状態管理モジュールz
StreamlitのSessionStateを管理するユーティリティ
"""

import streamlit as st
from typing import Any, Dict, List, Optional
from datetime import datetime
import json

class StateManager:
    """アプリケーション状態管理クラス"""
    
    def __init__(self):
        """初期化"""
        self._initialize_state()
    
    def _initialize_state(self):
        """初期状態を設定"""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.current_category = "input_widgets"
            st.session_state.current_component = None
            st.session_state.search_query = ""
            st.session_state.favorites = []
            st.session_state.theme = "light"
            st.session_state.show_code = True
            st.session_state.demo_params = {}
            st.session_state.history = []
            st.session_state.view_count = {}
            st.session_state.last_visited = None
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        状態値を取得
        
        Args:
            key: 取得するキー
            default: デフォルト値
        
        Returns:
            状態値
        """
        return st.session_state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        状態値を設定
        
        Args:
            key: 設定するキー
            value: 設定する値
        """
        st.session_state[key] = value
        self._add_to_history(key, value)
    
    def update_demo_params(self, component_id: str, params: Dict) -> None:
        """
        デモパラメータを更新
        
        Args:
            component_id: コンポーネントID
            params: パラメータ辞書
        """
        if 'demo_params' not in st.session_state:
            st.session_state.demo_params = {}
        st.session_state.demo_params[component_id] = params
    
    def get_demo_params(self, component_id: str) -> Dict:
        """
        デモパラメータを取得
        
        Args:
            component_id: コンポーネントID
        
        Returns:
            パラメータ辞書
        """
        if 'demo_params' not in st.session_state:
            return {}
        return st.session_state.demo_params.get(component_id, {})
    
    def toggle_favorite(self, component_id: str) -> bool:
        """
        お気に入りの切り替え
        
        Args:
            component_id: コンポーネントID
        
        Returns:
            お気に入りに追加された場合True
        """
        if 'favorites' not in st.session_state:
            st.session_state.favorites = []
        
        if component_id in st.session_state.favorites:
            st.session_state.favorites.remove(component_id)
            return False
        else:
            st.session_state.favorites.append(component_id)
            return True
    
    def is_favorite(self, component_id: str) -> bool:
        """
        お気に入りかどうかを確認
        
        Args:
            component_id: コンポーネントID
        
        Returns:
            お気に入りの場合True
        """
        if 'favorites' not in st.session_state:
            return False
        return component_id in st.session_state.favorites
    
    def get_favorites(self) -> List[str]:
        """
        お気に入りリストを取得
        
        Returns:
            お気に入りのコンポーネントIDリスト
        """
        return st.session_state.get('favorites', [])
    
    def increment_view_count(self, component_id: str) -> int:
        """
        コンポーネントの閲覧回数を増やす
        
        Args:
            component_id: コンポーネントID
        
        Returns:
            更新後の閲覧回数
        """
        if 'view_count' not in st.session_state:
            st.session_state.view_count = {}
        
        current_count = st.session_state.view_count.get(component_id, 0)
        st.session_state.view_count[component_id] = current_count + 1
        return current_count + 1
    
    def get_view_count(self, component_id: str) -> int:
        """
        コンポーネントの閲覧回数を取得
        
        Args:
            component_id: コンポーネントID
        
        Returns:
            閲覧回数
        """
        if 'view_count' not in st.session_state:
            return 0
        return st.session_state.view_count.get(component_id, 0)
    
    def get_popular_components(self, limit: int = 5) -> List[tuple]:
        """
        人気のコンポーネントを取得
        
        Args:
            limit: 取得する数
        
        Returns:
            (component_id, view_count)のタプルリスト
        """
        if 'view_count' not in st.session_state:
            return []
        
        sorted_components = sorted(
            st.session_state.view_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_components[:limit]
    
    def _add_to_history(self, key: str, value: Any) -> None:
        """
        履歴に追加
        
        Args:
            key: 操作キー
            value: 操作値
        """
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        st.session_state.history.append({
            'timestamp': datetime.now().isoformat(),
            'key': key,
            'value': value
        })
        
        # 履歴の上限管理（最新100件のみ保持）
        if len(st.session_state.history) > 100:
            st.session_state.history = st.session_state.history[-100:]
    
    def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """
        最近の履歴を取得
        
        Args:
            limit: 取得する数
        
        Returns:
            履歴リスト
        """
        if 'history' not in st.session_state:
            return []
        return st.session_state.history[-limit:]
    
    def clear_history(self) -> None:
        """履歴をクリア"""
        st.session_state.history = []
    
    def export_state(self) -> str:
        """
        現在の状態をJSON形式でエクスポート
        
        Returns:
            JSON文字列
        """
        state_dict = {
            'current_category': self.get('current_category'),
            'current_component': self.get('current_component'),
            'favorites': self.get('favorites', []),
            'theme': self.get('theme', 'light'),
            'view_count': self.get('view_count', {}),
            'timestamp': datetime.now().isoformat()
        }
        return json.dumps(state_dict, indent=2, ensure_ascii=False)
    
    def import_state(self, json_str: str) -> bool:
        """
        JSON形式の状態をインポート
        
        Args:
            json_str: JSON文字列
        
        Returns:
            成功した場合True
        """
        try:
            state_dict = json.loads(json_str)
            for key, value in state_dict.items():
                if key != 'timestamp':
                    self.set(key, value)
            return True
        except Exception:
            return False
    
    def reset_state(self) -> None:
        """状態を初期化"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self._initialize_state()


# グローバルインスタンス
state_manager = StateManager()