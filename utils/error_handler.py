"""
エラーハンドリングモジュール
統一的なエラー処理を提供するユーティリティ
"""

import streamlit as st
from enum import Enum
from typing import Optional, Callable, Any
import logging
import traceback
from functools import wraps
from datetime import datetime

class ErrorLevel(Enum):
    """エラーレベル定義"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorHandler:
    """統一的なエラーハンドリングクラス"""
    
    def __init__(self, logger_name: str = __name__):
        """
        初期化
        
        Args:
            logger_name: ロガー名
        """
        self.logger = self._setup_logger(logger_name)
        self.error_count = 0
        self.error_history = []
    
    def _setup_logger(self, name: str) -> logging.Logger:
        """ロガーのセットアップ"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # ハンドラーが既に設定されていない場合のみ追加
        if not logger.handlers:
            # コンソールハンドラー
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # フォーマット設定
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
        
        return logger
    
    def handle_error(self,
                    error: Exception,
                    level: ErrorLevel = ErrorLevel.ERROR,
                    user_message: Optional[str] = None,
                    show_traceback: bool = False) -> None:
        """
        エラーを処理
        
        Args:
            error: 発生したエラー
            level: エラーレベル
            user_message: ユーザーに表示するメッセージ
            show_traceback: トレースバックを表示するか
        """
        self.error_count += 1
        
        # エラー情報を記録
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'level': level.value,
            'traceback': traceback.format_exc() if show_traceback else None
        }
        self.error_history.append(error_info)
        
        # ログ記録
        log_method = getattr(self.logger, level.value)
        log_method(f"Error occurred: {str(error)}", exc_info=show_traceback)
        
        # ユーザーへの通知
        if user_message:
            self._notify_user(user_message, level)
        else:
            self._notify_user(self._get_default_message(error), level)
        
        # デバッグ情報の表示（開発モードの場合）
        if show_traceback and level in [ErrorLevel.ERROR, ErrorLevel.CRITICAL]:
            with st.expander("🔍 詳細なエラー情報"):
                st.code(traceback.format_exc())
    
    def _notify_user(self, message: str, level: ErrorLevel) -> None:
        """ユーザーに通知"""
        if level == ErrorLevel.DEBUG:
            # デバッグレベルは通常表示しない
            pass
        elif level == ErrorLevel.INFO:
            st.info(f"ℹ️ {message}")
        elif level == ErrorLevel.WARNING:
            st.warning(f"⚠️ {message}")
        elif level == ErrorLevel.ERROR:
            st.error(f"❌ {message}")
        elif level == ErrorLevel.CRITICAL:
            st.error(f"🚨 重大なエラー: {message}")
            st.stop()  # 処理を停止
    
    def _get_default_message(self, error: Exception) -> str:
        """デフォルトのエラーメッセージを取得"""
        error_messages = {
            FileNotFoundError: "ファイルが見つかりません。ファイルパスを確認してください。",
            ValueError: "入力値が正しくありません。入力内容を確認してください。",
            KeyError: "必要な設定またはデータが見つかりません。",
            ImportError: "必要なモジュールが読み込めません。インストール状況を確認してください。",
            TypeError: "データ型が正しくありません。入力形式を確認してください。",
            IndexError: "インデックスが範囲外です。データの範囲を確認してください。",
            AttributeError: "属性またはメソッドが存在しません。",
            ZeroDivisionError: "ゼロによる除算が発生しました。計算式を確認してください。",
            ConnectionError: "接続エラーが発生しました。ネットワーク接続を確認してください。",
            TimeoutError: "タイムアウトが発生しました。しばらく待ってから再試行してください。"
        }
        
        return error_messages.get(
            type(error),
            f"予期しないエラーが発生しました: {type(error).__name__}"
        )
    
    def safe_execute(self,
                    func: Callable,
                    *args,
                    default_return: Any = None,
                    error_message: Optional[str] = None,
                    **kwargs) -> Any:
        """
        安全に関数を実行
        
        Args:
            func: 実行する関数
            *args: 関数の引数
            default_return: エラー時のデフォルト戻り値
            error_message: エラー時のメッセージ
            **kwargs: 関数のキーワード引数
        
        Returns:
            関数の戻り値またはデフォルト値
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(
                e,
                level=ErrorLevel.ERROR,
                user_message=error_message
            )
            return default_return
    
    def error_boundary(self,
                      level: ErrorLevel = ErrorLevel.ERROR,
                      message: Optional[str] = None,
                      default_return: Any = None):
        """
        デコレーターとしてのエラーバウンダリ
        
        Args:
            level: エラーレベル
            message: エラーメッセージ
            default_return: エラー時のデフォルト戻り値
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.handle_error(
                        e,
                        level=level,
                        user_message=message
                    )
                    return default_return
            return wrapper
        return decorator
    
    def validate_input(self,
                      value: Any,
                      validator: Callable[[Any], bool],
                      error_message: str = "入力値が無効です") -> bool:
        """
        入力値を検証
        
        Args:
            value: 検証する値
            validator: 検証関数
            error_message: エラーメッセージ
        
        Returns:
            検証結果
        """
        try:
            if not validator(value):
                raise ValueError(error_message)
            return True
        except Exception as e:
            self.handle_error(
                e,
                level=ErrorLevel.WARNING,
                user_message=error_message
            )
            return False
    
    def get_error_stats(self) -> Dict[str, Any]:
        """
        エラー統計を取得
        
        Returns:
            エラー統計情報
        """
        if not self.error_history:
            return {
                'total_errors': 0,
                'error_types': {},
                'recent_errors': []
            }
        
        error_types = {}
        for error in self.error_history:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_errors': self.error_count,
            'error_types': error_types,
            'recent_errors': self.error_history[-5:]  # 最新5件
        }
    
    def clear_error_history(self) -> None:
        """エラー履歴をクリア"""
        self.error_history = []
        self.error_count = 0
    
    def display_error_report(self) -> None:
        """エラーレポートを表示"""
        stats = self.get_error_stats()
        
        if stats['total_errors'] == 0:
            st.success("✅ エラーは発生していません")
            return
        
        with st.expander(f"📊 エラーレポート (合計: {stats['total_errors']}件)"):
            # エラータイプ別の集計
            if stats['error_types']:
                st.subheader("エラータイプ別集計")
                for error_type, count in stats['error_types'].items():
                    st.write(f"- {error_type}: {count}件")
            
            # 最近のエラー
            if stats['recent_errors']:
                st.subheader("最近のエラー")
                for error in stats['recent_errors']:
                    st.write(f"- [{error['timestamp']}] {error['type']}: {error['message']}")


# グローバルインスタンス
error_handler = ErrorHandler()

# 便利な関数のエイリアス
handle_error = error_handler.handle_error
safe_execute = error_handler.safe_execute
error_boundary = error_handler.error_boundary