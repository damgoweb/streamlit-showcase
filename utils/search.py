"""
検索エンジンモジュール
コンポーネントの検索機能を提供
"""

import re
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
import json
from dataclasses import dataclass
from enum import Enum

@dataclass
class SearchResult:
    """検索結果を表すデータクラス"""
    component_id: str
    name: str
    category: str
    description: str
    score: float
    matched_fields: List[str]
    highlights: Dict[str, str]

class SearchMode(Enum):
    """検索モード"""
    EXACT = "exact"          # 完全一致
    PARTIAL = "partial"      # 部分一致
    FUZZY = "fuzzy"         # あいまい検索
    REGEX = "regex"         # 正規表現

class SearchEngine:
    """コンポーネント検索エンジン"""
    
    def __init__(self, components_data: Optional[List[Dict]] = None):
        """
        初期化
        
        Args:
            components_data: コンポーネントデータのリスト
        """
        self.components = components_data or []
        self.index = {}
        self.inverted_index = {}
        self.tag_index = {}
        
        if self.components:
            self._build_index()
        else:
            self._load_components_data()
            self._build_index()
    
    def _load_components_data(self) -> None:
        """コンポーネントメタデータを読み込み"""
        meta_file = Path("data/components_meta.json")
        
        if meta_file.exists():
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.components = data.get('components', [])
        
        # メタデータがない場合は、デフォルトのコンポーネントデータを追加
        if not self.components:
            self.components = self._create_default_components()
    
    def _create_default_components(self) -> List[Dict]:
        """デフォルトのコンポーネントデータを作成"""
        return [
            {
                "id": "text_input",
                "name": "st.text_input",
                "category": "input_widgets",
                "description": "単一行のテキスト入力フィールド",
                "tags": ["input", "text", "form", "basic"],
                "keywords": ["テキスト", "入力", "文字列", "フォーム"]
            },
            {
                "id": "number_input",
                "name": "st.number_input",
                "category": "input_widgets",
                "description": "数値入力フィールド",
                "tags": ["input", "number", "form", "basic"],
                "keywords": ["数値", "入力", "数字", "フォーム"]
            },
            {
                "id": "text_area",
                "name": "st.text_area",
                "category": "input_widgets",
                "description": "複数行のテキスト入力エリア",
                "tags": ["input", "text", "multiline", "form"],
                "keywords": ["テキストエリア", "複数行", "入力", "長文"]
            },
            {
                "id": "date_input",
                "name": "st.date_input",
                "category": "input_widgets",
                "description": "日付選択ウィジェット",
                "tags": ["input", "date", "calendar", "時間"],
                "keywords": ["日付", "カレンダー", "日時", "選択"]
            },
            {
                "id": "checkbox",
                "name": "st.checkbox",
                "category": "select_widgets",
                "description": "チェックボックス",
                "tags": ["select", "boolean", "toggle", "basic"],
                "keywords": ["チェック", "選択", "オンオフ", "ブール"]
            },
            {
                "id": "radio",
                "name": "st.radio",
                "category": "select_widgets",
                "description": "ラジオボタン",
                "tags": ["select", "choice", "single", "basic"],
                "keywords": ["ラジオ", "選択", "単一選択", "オプション"]
            },
            {
                "id": "selectbox",
                "name": "st.selectbox",
                "category": "select_widgets",
                "description": "ドロップダウン選択ボックス",
                "tags": ["select", "dropdown", "choice", "basic"],
                "keywords": ["セレクト", "ドロップダウン", "選択", "リスト"]
            },
            {
                "id": "multiselect",
                "name": "st.multiselect",
                "category": "select_widgets",
                "description": "複数選択ボックス",
                "tags": ["select", "multiple", "choice", "list"],
                "keywords": ["複数選択", "マルチ", "選択", "複数"]
            },
            {
                "id": "slider",
                "name": "st.slider",
                "category": "select_widgets",
                "description": "スライダー",
                "tags": ["select", "range", "slider", "basic"],
                "keywords": ["スライダー", "範囲", "調整", "スライド"]
            },
            {
                "id": "button",
                "name": "st.button",
                "category": "input_widgets",
                "description": "ボタン",
                "tags": ["action", "button", "click", "basic"],
                "keywords": ["ボタン", "クリック", "アクション", "実行"]
            },
            {
                "id": "dataframe",
                "name": "st.dataframe",
                "category": "data_widgets",
                "description": "インタラクティブなデータフレーム表示",
                "tags": ["data", "table", "dataframe", "basic"],
                "keywords": ["データフレーム", "テーブル", "表", "データ"]
            },
            {
                "id": "table",
                "name": "st.table",
                "category": "data_widgets",
                "description": "静的なテーブル表示",
                "tags": ["data", "table", "static"],
                "keywords": ["テーブル", "表", "静的", "固定"]
            },
            {
                "id": "metric",
                "name": "st.metric",
                "category": "data_widgets",
                "description": "メトリクス表示",
                "tags": ["data", "metric", "kpi", "dashboard"],
                "keywords": ["メトリクス", "KPI", "指標", "ダッシュボード"]
            },
            {
                "id": "line_chart",
                "name": "st.line_chart",
                "category": "chart_widgets",
                "description": "折れ線グラフ",
                "tags": ["chart", "line", "graph", "basic"],
                "keywords": ["折れ線", "グラフ", "チャート", "推移"]
            },
            {
                "id": "bar_chart",
                "name": "st.bar_chart",
                "category": "chart_widgets",
                "description": "棒グラフ",
                "tags": ["chart", "bar", "graph", "basic"],
                "keywords": ["棒グラフ", "バー", "チャート", "比較"]
            },
            {
                "id": "area_chart",
                "name": "st.area_chart",
                "category": "chart_widgets",
                "description": "エリアチャート",
                "tags": ["chart", "area", "graph"],
                "keywords": ["エリア", "面", "チャート", "累積"]
            },
            {
                "id": "columns",
                "name": "st.columns",
                "category": "layout_widgets",
                "description": "カラムレイアウト",
                "tags": ["layout", "columns", "grid", "basic"],
                "keywords": ["カラム", "列", "レイアウト", "配置"]
            },
            {
                "id": "container",
                "name": "st.container",
                "category": "layout_widgets",
                "description": "コンテナ",
                "tags": ["layout", "container", "group"],
                "keywords": ["コンテナ", "グループ", "まとめ", "整理"]
            },
            {
                "id": "expander",
                "name": "st.expander",
                "category": "layout_widgets",
                "description": "展開可能セクション",
                "tags": ["layout", "expander", "collapsible"],
                "keywords": ["展開", "折りたたみ", "エクスパンダー", "詳細"]
            },
            {
                "id": "tabs",
                "name": "st.tabs",
                "category": "layout_widgets",
                "description": "タブレイアウト",
                "tags": ["layout", "tabs", "navigation"],
                "keywords": ["タブ", "切り替え", "ナビゲーション", "整理"]
            }
        ]
    
    def _build_index(self) -> None:
        """検索インデックスを構築"""
        for comp in self.components:
            comp_id = comp['id']
            
            # 基本インデックス
            self.index[comp_id] = comp
            
            # 転置インデックス（単語 -> コンポーネントID）
            self._add_to_inverted_index(comp)
            
            # タグインデックス
            for tag in comp.get('tags', []):
                if tag not in self.tag_index:
                    self.tag_index[tag] = []
                self.tag_index[tag].append(comp_id)
    
    def _add_to_inverted_index(self, component: Dict) -> None:
        """転置インデックスにコンポーネントを追加"""
        comp_id = component['id']
        
        # インデックス対象のフィールドからトークンを抽出
        searchable_fields = ['id', 'name', 'description', 'category']
        for field in searchable_fields:
            if field in component:
                tokens = self._tokenize(str(component[field]))
                for token in tokens:
                    if token not in self.inverted_index:
                        self.inverted_index[token] = {}
                    if comp_id not in self.inverted_index[token]:
                        self.inverted_index[token][comp_id] = []
                    self.inverted_index[token][comp_id].append(field)
        
        # キーワードも追加
        for keyword in component.get('keywords', []):
            tokens = self._tokenize(keyword)
            for token in tokens:
                if token not in self.inverted_index:
                    self.inverted_index[token] = {}
                if comp_id not in self.inverted_index[token]:
                    self.inverted_index[token][comp_id] = []
                self.inverted_index[token][comp_id].append('keywords')
    
    def _tokenize(self, text: str) -> List[str]:
        """テキストをトークン化"""
        if not text:
            return []
        
        # 小文字化
        text = text.lower()
        
        # 日本語と英語の両方に対応
        # 英数字の単語を抽出
        tokens = re.findall(r'\w+', text)
        
        # 日本語の場合は文字単位でも分割（簡易的な処理）
        japanese_chars = re.findall(r'[ぁ-んァ-ン一-龥]+', text)
        for word in japanese_chars:
            # 2文字以上の連続する文字を追加
            for i in range(len(word) - 1):
                tokens.append(word[i:i+2])
        
        return list(set(tokens))  # 重複を除去
    
    def search(self,
              query: str,
              mode: SearchMode = SearchMode.PARTIAL,
              limit: int = 10,
              category_filter: Optional[str] = None,
              tag_filter: Optional[List[str]] = None) -> List[SearchResult]:
        """
        検索を実行
        
        Args:
            query: 検索クエリ
            mode: 検索モード
            limit: 最大結果数
            category_filter: カテゴリフィルタ
            tag_filter: タグフィルタ
        
        Returns:
            検索結果のリスト
        """
        if not query:
            return []
        
        # クエリをトークン化
        query_tokens = self._tokenize(query.lower())
        
        # スコアリング
        scores = {}
        matched_fields = {}
        
        for token in query_tokens:
            # 完全一致
            if token in self.inverted_index:
                for comp_id, fields in self.inverted_index[token].items():
                    if comp_id not in scores:
                        scores[comp_id] = 0
                        matched_fields[comp_id] = set()
                    scores[comp_id] += len(fields) * 2  # 完全一致は高スコア
                    matched_fields[comp_id].update(fields)
            
            # 部分一致（PARTIAL モードの場合）
            if mode == SearchMode.PARTIAL:
                for index_token in self.inverted_index:
                    if token in index_token or index_token in token:
                        for comp_id, fields in self.inverted_index[index_token].items():
                            if comp_id not in scores:
                                scores[comp_id] = 0
                                matched_fields[comp_id] = set()
                            scores[comp_id] += len(fields)  # 部分一致は通常スコア
                            matched_fields[comp_id].update(fields)
        
        # フィルタリング
        filtered_scores = {}
        for comp_id, score in scores.items():
            comp = self.index[comp_id]
            
            # カテゴリフィルタ
            if category_filter and comp.get('category') != category_filter:
                continue
            
            # タグフィルタ
            if tag_filter:
                comp_tags = set(comp.get('tags', []))
                if not any(tag in comp_tags for tag in tag_filter):
                    continue
            
            filtered_scores[comp_id] = score
        
        # ソートして結果を作成
        sorted_results = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for comp_id, score in sorted_results[:limit]:
            comp = self.index[comp_id]
            
            # ハイライトを生成
            highlights = self._generate_highlights(comp, query_tokens)
            
            result = SearchResult(
                component_id=comp_id,
                name=comp['name'],
                category=comp['category'],
                description=comp['description'],
                score=score,
                matched_fields=list(matched_fields[comp_id]),
                highlights=highlights
            )
            results.append(result)
        
        return results
    
    def _generate_highlights(self, component: Dict, query_tokens: List[str]) -> Dict[str, str]:
        """検索結果のハイライトを生成"""
        highlights = {}
        
        for field in ['name', 'description']:
            if field in component:
                text = component[field]
                highlighted_text = text
                
                # クエリトークンをハイライト
                for token in query_tokens:
                    # 大文字小文字を無視してマッチング
                    pattern = re.compile(re.escape(token), re.IGNORECASE)
                    highlighted_text = pattern.sub(
                        lambda m: f"**{m.group()}**",
                        highlighted_text
                    )
                
                if highlighted_text != text:
                    highlights[field] = highlighted_text
        
        return highlights
    
    def search_by_tag(self, tags: List[str]) -> List[str]:
        """タグで検索"""
        result_ids = set()
        
        for tag in tags:
            if tag in self.tag_index:
                result_ids.update(self.tag_index[tag])
        
        return list(result_ids)
    
    def get_suggestions(self, prefix: str, limit: int = 5) -> List[str]:
        """入力補完の候補を取得"""
        if not prefix:
            return []
        
        prefix_lower = prefix.lower()
        suggestions = []
        
        # コンポーネント名から候補を生成
        for comp in self.components:
            name = comp['name'].lower()
            if name.startswith(f"st.{prefix_lower}") or prefix_lower in name:
                suggestions.append(comp['name'])
                if len(suggestions) >= limit:
                    break
        
        return suggestions[:limit]
    
    def get_related_components(self, component_id: str, limit: int = 5) -> List[str]:
        """関連コンポーネントを取得"""
        if component_id not in self.index:
            return []
        
        component = self.index[component_id]
        related = []
        
        # relatedフィールドがある場合は優先
        if 'related' in component:
            for rel_id in component['related']:
                if rel_id in self.index and rel_id not in related:
                    related.append(rel_id)
                    if len(related) >= limit:
                        return related
        
        # 同じカテゴリのコンポーネント
        for comp in self.components:
            if comp['id'] != component_id and comp['category'] == component['category']:
                if comp['id'] not in related:
                    related.append(comp['id'])
                    if len(related) >= limit:
                        break
        
        return related


# グローバルインスタンス
search_engine = SearchEngine()