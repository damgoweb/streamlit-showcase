"""
日付・時刻入力コンポーネント
date_input, time_input の実装
"""

import streamlit as st
from typing import Any, Dict, Optional, Union
from datetime import datetime, date, time, timedelta
import calendar
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.base_component import BaseComponent
from utils.code_display import code_display
from utils.sample_data import sample_data


class DateInputComponent(BaseComponent):
    """st.date_input コンポーネント"""
    
    def __init__(self):
        super().__init__("date_input", "input_widgets")
        self.metadata = {
            'id': 'date_input',
            'name': 'st.date_input',
            'category': 'input_widgets',
            'description': '日付選択ウィジェット。カレンダーUIで日付を選択できる。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Select a date',
                    'description': 'ウィジェットのラベル'
                },
                {
                    'name': 'value',
                    'type': 'date/datetime/tuple',
                    'required': False,
                    'default': 'today',
                    'description': 'デフォルト日付または日付範囲'
                },
                {
                    'name': 'min_value',
                    'type': 'date/datetime',
                    'required': False,
                    'default': None,
                    'description': '選択可能な最小日付'
                },
                {
                    'name': 'max_value',
                    'type': 'date/datetime',
                    'required': False,
                    'default': None,
                    'description': '選択可能な最大日付'
                },
                {
                    'name': 'format',
                    'type': 'str',
                    'required': False,
                    'default': 'YYYY/MM/DD',
                    'description': '日付表示フォーマット'
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
                'valueにタプルを渡すと日付範囲選択モードになる',
                'datetime.date.today()で今日の日付を取得',
                'min_value/max_valueで選択可能範囲を制限',
                'formatで表示形式をカスタマイズ（YYYY/MM/DD, MM/DD/YYYY等）',
                '日付範囲選択時は2つの日付のタプルが返される'
            ],
            'related': ['time_input', 'slider', 'calendar'],
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
                    value="日付を選択してください",
                    key=f"{self.id}_param_label"
                )
                
                # 選択モード
                mode = st.radio(
                    "選択モード",
                    ["単一日付", "日付範囲"],
                    key=f"{self.id}_param_mode"
                )
                
                # デフォルト値設定
                if mode == "単一日付":
                    default_option = st.selectbox(
                        "デフォルト値",
                        ["今日", "昨日", "明日", "カスタム"],
                        key=f"{self.id}_param_default_option"
                    )
                    
                    if default_option == "今日":
                        value = date.today()
                    elif default_option == "昨日":
                        value = date.today() - timedelta(days=1)
                    elif default_option == "明日":
                        value = date.today() + timedelta(days=1)
                    else:
                        value = st.date_input(
                            "カスタム日付",
                            value=date.today(),
                            key=f"{self.id}_param_custom_date"
                        )
                else:
                    # 範囲選択
                    start_date = st.date_input(
                        "開始日",
                        value=date.today() - timedelta(days=7),
                        key=f"{self.id}_param_start"
                    )
                    end_date = st.date_input(
                        "終了日",
                        value=date.today(),
                        key=f"{self.id}_param_end"
                    )
                    value = (start_date, end_date)
                
                # 最小・最大日付
                use_min = st.checkbox("最小日付を設定", key=f"{self.id}_use_min")
                if use_min:
                    min_value = st.date_input(
                        "最小日付",
                        value=date.today() - timedelta(days=365),
                        key=f"{self.id}_param_min"
                    )
                else:
                    min_value = None
            
            with col2:
                use_max = st.checkbox("最大日付を設定", key=f"{self.id}_use_max")
                if use_max:
                    max_value = st.date_input(
                        "最大日付",
                        value=date.today() + timedelta(days=365),
                        key=f"{self.id}_param_max"
                    )
                else:
                    max_value = None
                
                format_str = st.selectbox(
                    "日付フォーマット",
                    ["YYYY/MM/DD", "MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
                    key=f"{self.id}_param_format"
                )
                
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="カレンダーアイコンをクリックして選択",
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
            'value': value,
            'format': format_str,
            'key': f"{self.id}_demo_widget"
        }
        
        if min_value:
            params['min_value'] = min_value
        if max_value:
            params['max_value'] = max_value
        if help_text:
            params['help'] = help_text
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # コンポーネント実行
        result = st.date_input(**params)
        
        # 結果表示
        if isinstance(result, tuple):
            # 範囲選択の場合
            if len(result) == 2:
                start, end = result
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("開始日", start.strftime('%Y/%m/%d'))
                with col2:
                    st.metric("終了日", end.strftime('%Y/%m/%d'))
                with col3:
                    days_diff = (end - start).days + 1
                    st.metric("期間", f"{days_diff}日間")
                
                # 詳細情報
                with st.expander("🔍 期間の詳細"):
                    st.write(f"**週数**: {days_diff // 7}週と{days_diff % 7}日")
                    st.write(f"**月数**: 約{days_diff / 30:.1f}ヶ月")
                    
                    # カレンダー表示（簡易版）
                    st.write("**期間内の日付:**")
                    current = start
                    dates = []
                    while current <= end and len(dates) < 100:  # 最大100日
                        dates.append(current.strftime('%m/%d'))
                        current += timedelta(days=1)
                    st.write(", ".join(dates[:20]) + ("..." if len(dates) > 20 else ""))
        else:
            # 単一日付の場合
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("選択日", result.strftime('%Y/%m/%d'))
            with col2:
                st.metric("曜日", ['月', '火', '水', '木', '金', '土', '日'][result.weekday()])
            with col3:
                days_from_today = (result - date.today()).days
                st.metric("今日から", f"{days_from_today:+d}日")
            with col4:
                st.metric("年の第", f"{result.isocalendar()[1]}週")
            
            # 詳細情報
            with st.expander("🔍 日付の詳細"):
                st.write(f"**年**: {result.year}")
                st.write(f"**月**: {result.month}")
                st.write(f"**日**: {result.day}")
                st.write(f"**曜日**: {['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'][result.weekday()]}")
                st.write(f"**年の第{result.timetuple().tm_yday}日目**")
                st.write(f"**ISO形式**: {result.isoformat()}")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic", params, mode)
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return result
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None, mode: str = "単一日付") -> str:
        """コードを取得"""
        if params is None:
            params = {
                'label': 'Select a date',
                'value': date.today(),
                'format': 'YYYY/MM/DD'
            }
        
        if level == "basic":
            if mode == "日付範囲":
                return """import streamlit as st
from datetime import date, timedelta

# 日付範囲選択
date_range = st.date_input(
    "期間を選択",
    value=(date.today() - timedelta(days=7), date.today()),
    format="YYYY/MM/DD"
)

if len(date_range) == 2:
    start, end = date_range
    st.write(f"選択期間: {start} から {end}")"""
            else:
                return """import streamlit as st
from datetime import date

# 日付選択
selected_date = st.date_input(
    "日付を選択",
    value=date.today(),
    format="YYYY/MM/DD"
)

st.write(f"選択した日付: {selected_date}")"""
        
        elif level == "advanced":
            return """import streamlit as st
from datetime import date, timedelta
import calendar

# 日付入力
selected_date = st.date_input(
    "日付を選択",
    value=date.today(),
    min_value=date.today() - timedelta(days=365),
    max_value=date.today() + timedelta(days=365),
    format="YYYY/MM/DD"
)

# 日付情報の表示
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("年月日", selected_date.strftime('%Y年%m月%d日'))
    
with col2:
    weekday = ['月', '火', '水', '木', '金', '土', '日'][selected_date.weekday()]
    st.metric("曜日", f"{weekday}曜日")
    
with col3:
    days_from_today = (selected_date - date.today()).days
    if days_from_today > 0:
        st.metric("今日から", f"{days_from_today}日後")
    elif days_from_today < 0:
        st.metric("今日から", f"{abs(days_from_today)}日前")
    else:
        st.metric("今日から", "今日")"""
        
        else:  # full
            return """import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import calendar

def main():
    st.title("📅 日付選択ツール")
    
    # 日付選択
    selected_date = st.date_input(
        "日付を選択",
        value=date.today(),
        format="YYYY/MM/DD"
    )
    
    # 日付分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**基本情報**")
        st.write(f"- 年: {selected_date.year}")
        st.write(f"- 月: {selected_date.month}")
        st.write(f"- 日: {selected_date.day}")
        st.write(f"- 曜日: {calendar.day_name[selected_date.weekday()]}")
        
    with col2:
        st.write("**相対情報**")
        days_from_today = (selected_date - date.today()).days
        st.write(f"- 今日から: {days_from_today:+d}日")
        st.write(f"- 年の第{selected_date.timetuple().tm_yday}日目")

if __name__ == "__main__":
    main()"""


class TimeInputComponent(BaseComponent):
    """st.time_input コンポーネント"""
    
    def __init__(self):
        super().__init__("time_input", "input_widgets")
        self.metadata = {
            'id': 'time_input',
            'name': 'st.time_input',
            'category': 'input_widgets',
            'description': '時刻選択ウィジェット。時間と分を選択できる。',
            'parameters': [
                {
                    'name': 'label',
                    'type': 'str',
                    'required': True,
                    'default': 'Select a time',
                    'description': 'ウィジェットのラベル'
                },
                {
                    'name': 'value',
                    'type': 'time/datetime',
                    'required': False,
                    'default': 'None',
                    'description': 'デフォルト時刻'
                },
                {
                    'name': 'step',
                    'type': 'int/timedelta',
                    'required': False,
                    'default': 900,
                    'description': '選択ステップ（秒単位）'
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
                'stepパラメータで選択間隔を設定（デフォルト15分）',
                'datetime.time()で時刻オブジェクトを作成',
                '24時間形式で表示',
                'value=Noneで空の状態から開始',
                'timedelta(minutes=30)でステップを30分に設定可能'
            ],
            'related': ['date_input', 'slider'],
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
                    value="時刻を選択してください",
                    key=f"{self.id}_param_label"
                )
                
                # デフォルト時刻設定
                default_option = st.selectbox(
                    "デフォルト値",
                    ["現在時刻", "正午", "なし", "カスタム"],
                    key=f"{self.id}_param_default"
                )
                
                if default_option == "現在時刻":
                    value = datetime.now().time()
                elif default_option == "正午":
                    value = time(12, 0)
                elif default_option == "なし":
                    value = None
                else:
                    hour = st.number_input("時", 0, 23, 9, key=f"{self.id}_hour")
                    minute = st.number_input("分", 0, 59, 0, key=f"{self.id}_minute")
                    value = time(hour, minute)
                
                # ステップ設定
                step_option = st.selectbox(
                    "ステップ間隔",
                    ["1分", "5分", "15分", "30分", "1時間"],
                    index=2,
                    key=f"{self.id}_param_step_option"
                )
                
                step_map = {
                    "1分": 60,
                    "5分": 300,
                    "15分": 900,
                    "30分": 1800,
                    "1時間": 3600
                }
                step = step_map[step_option]
            
            with col2:
                help_text = st.text_input(
                    "ヘルプテキスト",
                    value="時刻を選択してください",
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
            'step': step,
            'key': f"{self.id}_demo_widget"
        }
        
        if value is not None:
            params['value'] = value
        if help_text:
            params['help'] = help_text
        if disabled:
            params['disabled'] = disabled
        if label_visibility != "visible":
            params['label_visibility'] = label_visibility
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # コンポーネント実行
        result = st.time_input(**params)
        
        # 結果表示
        if result:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("選択時刻", result.strftime('%H:%M'))
            with col2:
                st.metric("12時間形式", result.strftime('%I:%M %p'))
            with col3:
                total_minutes = result.hour * 60 + result.minute
                st.metric("0時からの分数", f"{total_minutes}分")
            with col4:
                st.metric("秒数", f"{total_minutes * 60}秒")
            
            # 詳細情報
            with st.expander("🔍 時刻の詳細"):
                st.write(f"**時**: {result.hour}")
                st.write(f"**分**: {result.minute}")
                st.write(f"**秒**: {result.second}")
                st.write(f"**ISO形式**: {result.isoformat()}")
                
                # 時間帯判定
                if 5 <= result.hour < 12:
                    period = "午前"
                elif 12 <= result.hour < 17:
                    period = "午後"
                elif 17 <= result.hour < 21:
                    period = "夕方"
                else:
                    period = "夜"
                st.write(f"**時間帯**: {period}")
                
                # 現在時刻との差
                now = datetime.now().time()
                now_minutes = now.hour * 60 + now.minute
                diff_minutes = total_minutes - now_minutes
                
                if diff_minutes > 0:
                    st.write(f"**現在時刻から**: {diff_minutes}分後")
                elif diff_minutes < 0:
                    st.write(f"**現在時刻から**: {abs(diff_minutes)}分前")
                else:
                    st.write("**現在時刻から**: 同じ時刻")
        
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
                'label': 'Select a time',
                'value': time(9, 0),
                'step': 900
            }
        
        if level == "basic":
            return """import streamlit as st
from datetime import time

# 時刻選択
selected_time = st.time_input(
    "時刻を選択",
    value=time(9, 0),
    step=900  # 15分間隔
)

st.write(f"選択した時刻: {selected_time.strftime('%H:%M')}")"""
        
        elif level == "advanced":
            return """import streamlit as st
from datetime import time, datetime, timedelta

# 時刻入力
selected_time = st.time_input(
    "開始時刻",
    value=time(9, 0),
    step=900  # 15分間隔
)

# 終了時刻の計算
duration = st.slider("所要時間（分）", 15, 180, 60)
end_time = (datetime.combine(datetime.today(), selected_time) + 
            timedelta(minutes=duration)).time()

# 結果表示
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("開始", selected_time.strftime('%H:%M'))
with col2:
    st.metric("終了", end_time.strftime('%H:%M'))
with col3:
    st.metric("所要時間", f"{duration}分")"""
        
        else:  # full
            return """import streamlit as st
from datetime import time, datetime, timedelta
import pandas as pd

def main():
    st.title("⏰ タイムスケジューラー")
    
    # 時間設定
    start_time = st.time_input(
        "開始時刻",
        value=time(9, 0),
        step=900
    )
    
    end_time = st.time_input(
        "終了時刻",
        value=time(18, 0),
        step=900
    )
    
    # 営業時間計算
    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute
    total_minutes = end_minutes - start_minutes
    
    # 結果表示
    st.metric("営業時間", f"{total_minutes // 60}時間{total_minutes % 60}分")

if __name__ == "__main__":
    main()"""


# コンポーネントのエクスポート
__all__ = ['DateInputComponent', 'TimeInputComponent']