"""
アプリケーション設定ファイル
"""

# アプリケーション基本設定
APP_NAME = "Streamlit UIコンポーネントショーケース"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Streamlitコンポーネントの包括的なリファレンス"

# UI設定
SIDEBAR_WIDTH = 300
MAX_WIDTH = 1200
SHOW_GITHUB_LINK = True
GITHUB_URL = "https://github.com/yourusername/streamlit-showcase"

# デフォルト設定
DEFAULT_THEME = "light"
DEFAULT_LANGUAGE = "ja"
ENABLE_CACHE = True
CACHE_TTL = 3600  # 秒
DEFAULT_CATEGORY = "input_widgets"
MAX_FAVORITES = 20
RECENT_COMPONENTS_COUNT = 5

# コンポーネントカテゴリ
COMPONENT_CATEGORIES = {
    "input_widgets": {
        "name": "入力ウィジェット",
        "icon": "📝",
        "description": "ユーザー入力を受け付けるコンポーネント"
    },
    "select_widgets": {
        "name": "選択ウィジェット", 
        "icon": "☑️",
        "description": "選択肢から選ぶコンポーネント"
    },
    "display_widgets": {
        "name": "表示ウィジェット",
        "icon": "📊",
        "description": "データや情報を表示するコンポーネント"
    },
    "data_widgets": {
        "name": "データ表示",
        "icon": "📋",
        "description": "データフレームやテーブルを表示するコンポーネント"
    },
    "chart_widgets": {
        "name": "チャート",
        "icon": "📈",
        "description": "グラフやチャートを描画するコンポーネント"
    },
    "layout_widgets": {
        "name": "レイアウト",
        "icon": "🎨",
        "description": "画面構成を制御するコンポーネント"
    },
    "media_widgets": {
        "name": "メディア",
        "icon": "🎬",
        "description": "画像・音声・動画を扱うコンポーネント"
    },
    "status_widgets": {
        "name": "ステータス",
        "icon": "⏳",
        "description": "進捗やステータスを表示するコンポーネント"
    },
    "control_widgets": {
        "name": "制御フロー",
        "icon": "🔄",
        "description": "アプリケーションの制御フローに関するコンポーネント"
    }
}

# サンプルデータ設定
SAMPLE_DATA_ROWS = 100
RANDOM_SEED = 42
SAMPLE_DATA_CONFIG = {
    "max_rows": 1000,
    "default_rows": 100,
    "chart_types": ["line", "bar", "area", "scatter"],
    "time_series_days": 30
}

# ページ設定
PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🎨",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# エラーハンドリング設定
ERROR_CONFIG = {
    "show_error_details": True,
    "log_errors": True,
    "max_error_history": 50
}

# キャッシュ設定
CACHE_CONFIG = {
    "ttl": CACHE_TTL,
    "max_entries": 100
}