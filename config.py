### **config.py**

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
    "chart_widgets": {
        "name": "チャート",
        "icon": "📈",
        "description": "グラフやチャートを描画するコンポーネント"
    },
    "layout_widgets": {
        "name": "レイアウト",
        "icon": "🎨",
        "description": "画面構成を制御するコンポーネント"
    }
}

# サンプルデータ設定
SAMPLE_DATA_ROWS = 100
RANDOM_SEED = 42