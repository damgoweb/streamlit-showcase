"""
サンプルデータ生成モジュール
デモ用のサンプルデータを生成するユーティリティ
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import random
import string

class SampleDataGenerator:
    """サンプルデータ生成クラス"""
    
    def __init__(self, seed: int = 42):
        """
        初期化
        
        Args:
            seed: 乱数シード
        """
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
    
    def generate_dataframe(self, 
                          rows: int = 100,
                          columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        サンプルDataFrameを生成
        
        Args:
            rows: 行数
            columns: カラム名リスト
        
        Returns:
            生成されたDataFrame
        """
        if columns is None:
            columns = ['ID', 'Name', 'Age', 'Score', 'Date', 'Category']
        
        data = {}
        
        for col in columns:
            if col == 'ID':
                data[col] = range(1, rows + 1)
            elif col == 'Name':
                data[col] = [self._generate_name() for _ in range(rows)]
            elif col == 'Age':
                data[col] = np.random.randint(18, 80, rows)
            elif col == 'Score':
                data[col] = np.round(np.random.uniform(0, 100, rows), 2)
            elif col == 'Date':
                data[col] = [self._generate_date() for _ in range(rows)]
            elif col == 'Category':
                categories = ['A', 'B', 'C', 'D']
                data[col] = np.random.choice(categories, rows)
            else:
                # デフォルトは数値データ
                data[col] = np.random.randn(rows)
        
        return pd.DataFrame(data)
    
    def generate_time_series(self, 
                           days: int = 30,
                           freq: str = 'D') -> pd.DataFrame:
        """
        時系列データを生成
        
        Args:
            days: 日数
            freq: 頻度 ('D'=日次, 'H'=時間, 'M'=分)
        
        Returns:
            時系列DataFrame
        """
        dates = pd.date_range(start=datetime.now() - timedelta(days=days),
                             end=datetime.now(),
                             freq=freq)
        
        df = pd.DataFrame({
            'Date': dates,
            'Value': np.cumsum(np.random.randn(len(dates))) + 100,
            'Volume': np.random.randint(1000, 10000, len(dates)),
            'Category': np.random.choice(['Type1', 'Type2', 'Type3'], len(dates))
        })
        
        return df
    
    def generate_chart_data(self, 
                          chart_type: str = 'line',
                          points: int = 50) -> pd.DataFrame:
        """
        チャート用データを生成
        
        Args:
            chart_type: チャートタイプ (line/bar/scatter/area)
            points: データポイント数
        
        Returns:
            チャート用DataFrame
        """
        x = np.linspace(0, 10, points)
        
        if chart_type == 'line':
            df = pd.DataFrame({
                'x': x,
                'y1': np.sin(x) + np.random.normal(0, 0.1, points),
                'y2': np.cos(x) + np.random.normal(0, 0.1, points),
                'y3': np.sin(x/2) + np.random.normal(0, 0.1, points)
            })
        elif chart_type == 'bar':
            categories = [f'Category {i}' for i in range(points)]
            df = pd.DataFrame({
                'Category': categories[:20],  # バーチャートは20項目まで
                'Value1': np.random.randint(10, 100, min(20, points)),
                'Value2': np.random.randint(20, 80, min(20, points))
            })
        elif chart_type == 'scatter':
            df = pd.DataFrame({
                'x': np.random.randn(points),
                'y': np.random.randn(points),
                'size': np.random.randint(10, 100, points),
                'color': np.random.choice(['red', 'blue', 'green'], points)
            })
        elif chart_type == 'area':
            df = pd.DataFrame({
                'x': x,
                'Area1': np.abs(np.sin(x)) * 10,
                'Area2': np.abs(np.cos(x)) * 8,
                'Area3': np.abs(np.sin(x/2)) * 6
            })
        else:
            # デフォルト
            df = pd.DataFrame({
                'x': x,
                'y': np.sin(x) + np.random.normal(0, 0.1, points)
            })
        
        return df
    
    def generate_json_data(self) -> Dict[str, Any]:
        """
        サンプルJSON データを生成
        
        Returns:
            JSON形式のデータ
        """
        return {
            "id": random.randint(1000, 9999),
            "name": self._generate_name(),
            "email": self._generate_email(),
            "age": random.randint(20, 60),
            "address": {
                "street": f"{random.randint(1, 999)} Main St",
                "city": random.choice(["Tokyo", "Osaka", "Kyoto", "Yokohama"]),
                "country": "Japan",
                "postal_code": f"{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            },
            "hobbies": random.sample(["Reading", "Gaming", "Cooking", "Travel", "Music", "Sports"], 3),
            "registered": datetime.now().isoformat(),
            "active": random.choice([True, False]),
            "scores": {
                "math": random.randint(60, 100),
                "science": random.randint(60, 100),
                "english": random.randint(60, 100)
            }
        }
    
    def generate_text_data(self, words: int = 100) -> str:
        """
        サンプルテキストデータを生成
        
        Args:
            words: 単語数
        
        Returns:
            生成されたテキスト
        """
        lorem_words = [
            "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
            "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
            "incididunt", "ut", "labore", "et", "dolore", "magna",
            "aliqua", "enim", "ad", "minim", "veniam", "quis",
            "nostrud", "exercitation", "ullamco", "laboris", "nisi"
        ]
        
        text = []
        for _ in range(words):
            text.append(random.choice(lorem_words))
        
        # 文章っぽく整形
        result = ' '.join(text)
        sentences = []
        words_list = result.split()
        
        i = 0
        while i < len(words_list):
            sentence_length = random.randint(5, 15)
            sentence = ' '.join(words_list[i:i+sentence_length])
            if sentence:
                sentence = sentence[0].upper() + sentence[1:] + '.'
                sentences.append(sentence)
            i += sentence_length
        
        return ' '.join(sentences)
    
    def generate_metrics_data(self) -> Dict[str, Any]:
        """
        メトリクス表示用データを生成
        
        Returns:
            メトリクスデータ
        """
        return {
            "revenue": {
                "value": f"¥{random.randint(1000000, 9999999):,}",
                "delta": f"{random.uniform(-10, 20):.1f}%",
                "delta_color": "normal"
            },
            "users": {
                "value": f"{random.randint(1000, 50000):,}",
                "delta": f"+{random.randint(10, 500)}",
                "delta_color": "normal"
            },
            "conversion": {
                "value": f"{random.uniform(1, 5):.2f}%",
                "delta": f"{random.uniform(-0.5, 0.5):.2f}%",
                "delta_color": "normal"
            },
            "satisfaction": {
                "value": f"{random.uniform(4.0, 5.0):.1f}/5.0",
                "delta": f"+{random.uniform(0, 0.3):.1f}",
                "delta_color": "normal"
            }
        }
    
    def _generate_name(self) -> str:
        """ランダムな名前を生成"""
        first_names = ["田中", "佐藤", "鈴木", "高橋", "渡辺", "伊藤", "山本", "中村"]
        last_names = ["太郎", "花子", "一郎", "美香", "健一", "由美", "隆", "恵子"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_email(self) -> str:
        """ランダムなメールアドレスを生成"""
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(['example.com', 'test.jp', 'sample.org'])
        return f"{username}@{domain}"
    
    def _generate_date(self) -> datetime:
        """ランダムな日付を生成"""
        start = datetime.now() - timedelta(days=365)
        end = datetime.now()
        random_date = start + timedelta(
            seconds=random.randint(0, int((end - start).total_seconds()))
        )
        return random_date
    
    def get_sample_csv_content(self) -> str:
        """
        サンプルCSVコンテンツを生成
        
        Returns:
            CSV形式の文字列
        """
        df = self.generate_dataframe(rows=10)
        return df.to_csv(index=False)
    
    def get_sample_options(self, count: int = 5) -> List[str]:
        """
        サンプル選択肢を生成
        
        Args:
            count: 選択肢の数
        
        Returns:
            選択肢リスト
        """
        options = [
            "Option A - 最初の選択肢",
            "Option B - 2番目の選択肢",
            "Option C - 3番目の選択肢",
            "Option D - 4番目の選択肢",
            "Option E - 5番目の選択肢",
            "Option F - 6番目の選択肢",
            "Option G - 7番目の選択肢",
            "Option H - 8番目の選択肢"
        ]
        return options[:count]


# グローバルインスタンス
sample_data = SampleDataGenerator()