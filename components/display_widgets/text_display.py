"""
テキスト表示コンポーネント
write, markdown, title, header, subheader, caption, code, text, latex, divider の実装
"""

import streamlit as st
from typing import Any, Dict, Optional, Union
import sys
from pathlib import Path
import json

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.base_component import BaseComponent
from utils.code_display import code_display
from utils.sample_data import sample_data


class WriteComponent(BaseComponent):
    """st.write コンポーネント"""
    
    def __init__(self):
        super().__init__("write", "display_widgets")
        self.metadata = {
            'id': 'write',
            'name': 'st.write',
            'category': 'display_widgets',
            'description': '万能表示関数。テキスト、データフレーム、グラフ、Markdownなど様々な形式を自動判別して表示。',
            'parameters': [
                {
                    'name': '*args',
                    'type': 'Any',
                    'required': True,
                    'default': None,
                    'description': '表示する内容（複数可）'
                },
                {
                    'name': 'unsafe_allow_html',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'HTMLの表示を許可'
                }
            ],
            'tips': [
                '最も汎用的な表示関数',
                '複数の引数を渡すと順番に表示',
                'DataFrameやチャートも自動で適切に表示',
                'Markdown記法も自動認識',
                'デバッグ時の変数確認に便利'
            ],
            'related': ['markdown', 'text', 'dataframe', 'json'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                content_type = st.selectbox(
                    "コンテンツタイプ",
                    ["テキスト", "Markdown", "データフレーム", "辞書/JSON", "複数要素"],
                    key=f"{self.id}_content_type"
                )
                
                if content_type == "テキスト":
                    text_content = st.text_area(
                        "表示内容",
                        value="これはst.writeで表示されたテキストです。",
                        key=f"{self.id}_text"
                    )
                    content = text_content
                elif content_type == "Markdown":
                    md_content = st.text_area(
                        "Markdown内容",
                        value="# 見出し\n**太字** と *イタリック*\n- リスト項目1\n- リスト項目2",
                        key=f"{self.id}_markdown"
                    )
                    content = md_content
                elif content_type == "データフレーム":
                    rows = st.slider("行数", 3, 10, 5, key=f"{self.id}_rows")
                    content = sample_data.generate_dataframe(rows=rows)
                elif content_type == "辞書/JSON":
                    content = sample_data.generate_json_data()
                else:  # 複数要素
                    content = None
            
            with col2:
                unsafe_allow_html = st.checkbox(
                    "HTMLを許可",
                    value=False,
                    help="HTMLタグの表示を許可（セキュリティ注意）",
                    key=f"{self.id}_html"
                )
                
                if unsafe_allow_html:
                    st.warning("⚠️ HTMLを許可すると、悪意のあるコードが実行される可能性があります")
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        if content_type == "複数要素":
            st.write(
                "文字列",
                123,
                {"key": "value"},
                sample_data.generate_dataframe(rows=3)
            )
        elif unsafe_allow_html and content_type == "テキスト":
            html_content = '<p style="color: blue;">これは<strong>HTML</strong>です</p>'
            st.write(html_content, unsafe_allow_html=True)
        else:
            st.write(content)
        
        # 様々な型の表示例
        with st.expander("🎯 様々な型の表示例"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**文字列:**", "Hello, World!")
                st.write("**数値:**", 42, 3.14159)
                st.write("**リスト:**", [1, 2, 3, 4, 5])
                st.write("**辞書:**", {"name": "Alice", "age": 30})
            
            with col2:
                st.write("**ブール値:**", True, False)
                st.write("**None:**", None)
                st.write("**タプル:**", (1, "two", 3.0))
                st.write("**Markdown:**", "**太字** *イタリック* `コード`")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return None
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st

# テキスト表示
st.write("Hello, Streamlit!")

# 複数の要素を一度に表示
st.write("テキスト", 123, {"key": "value"})

# Markdown記法も使える
st.write("# 見出し\\n**太字** と *イタリック*")

# DataFrameも表示可能
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
st.write(df)"""
        
        elif level == "advanced":
            return """import streamlit as st
import pandas as pd
import numpy as np

# 様々な型の表示
st.write("## st.writeの活用例")

# データ分析結果の表示
data = np.random.randn(100, 3)
df = pd.DataFrame(data, columns=['A', 'B', 'C'])

st.write("### データ統計")
st.write("**サンプル数:**", len(df))
st.write("**統計情報:**")
st.write(df.describe())

# 計算結果の表示
mean_values = df.mean()
st.write("**平均値:**", mean_values.to_dict())

# 条件付き表示
if df['A'].mean() > 0:
    st.write("✅ カラムAの平均は正の値です")
else:
    st.write("❌ カラムAの平均は負の値です")"""
        
        else:  # full
            return """import streamlit as st
import pandas as pd
import numpy as np
import json

def analyze_data(df):
    \"\"\"データ分析関数\"\"\"
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'null_counts': df.isnull().sum().to_dict(),
        'summary': df.describe().to_dict()
    }

def main():
    st.title("st.write デモアプリケーション")
    
    # サンプルデータ生成
    np.random.seed(42)
    df = pd.DataFrame({
        'ID': range(1, 101),
        'Value': np.random.randn(100),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'Date': pd.date_range('2024-01-01', periods=100)
    })
    
    # データ分析
    st.write("## データ分析レポート")
    
    analysis = analyze_data(df)
    
    # 分析結果の表示
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### データ概要")
        st.write("**データ形状:**", f"{analysis['shape'][0]}行 × {analysis['shape'][1]}列")
        st.write("**カラム:**", ", ".join(analysis['columns']))
        st.write("**データ型:**")
        for col, dtype in analysis['dtypes'].items():
            st.write(f"  - {col}: {dtype}")
    
    with col2:
        st.write("### 欠損値情報")
        st.write(analysis['null_counts'])
        
        st.write("### カテゴリ分布")
        category_counts = df['Category'].value_counts()
        st.write(category_counts.to_dict())
    
    # データプレビュー
    st.write("### データプレビュー")
    st.write(df.head(10))
    
    # 統計情報
    st.write("### 統計情報")
    st.write(pd.DataFrame(analysis['summary']))
    
    # JSON形式での出力
    if st.checkbox("JSON形式で表示"):
        st.write("### JSON出力")
        st.write(json.dumps(analysis, indent=2, default=str))

if __name__ == "__main__":
    main()"""


class MarkdownComponent(BaseComponent):
    """st.markdown コンポーネント"""
    
    def __init__(self):
        super().__init__("markdown", "display_widgets")
        self.metadata = {
            'id': 'markdown',
            'name': 'st.markdown',
            'category': 'display_widgets',
            'description': 'Markdown形式のテキストを表示。見出し、リスト、リンク、画像などをサポート。',
            'parameters': [
                {
                    'name': 'body',
                    'type': 'str',
                    'required': True,
                    'default': '',
                    'description': 'Markdown形式のテキスト'
                },
                {
                    'name': 'unsafe_allow_html',
                    'type': 'bool',
                    'required': False,
                    'default': False,
                    'description': 'HTMLタグの使用を許可'
                }
            ],
            'tips': [
                '見出し、太字、イタリック、リスト、リンクなどMarkdown記法をサポート',
                'unsafe_allow_html=TrueでHTMLタグも使用可能',
                'LaTeX数式も$$で囲むことで表示可能',
                'コードブロックは```で囲む',
                'カスタムCSSも適用可能'
            ],
            'related': ['write', 'text', 'latex', 'caption'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            markdown_text = st.text_area(
                "Markdown内容",
                value="""# Markdownデモ

## 基本的な書式

これは**太字**と*イタリック*、そして***太字イタリック***のテキストです。

### リスト

**順序なしリスト:**
- 項目1
- 項目2
  - サブ項目2.1
  - サブ項目2.2
- 項目3

**順序付きリスト:**
1. 最初の項目
2. 次の項目
3. 最後の項目

### リンクと画像

[Streamlitドキュメント](https://docs.streamlit.io)

### コードブロック

```python
def hello():
    print("Hello, World!")
```

### 引用

> これは引用文です。
> 複数行の引用も可能です。

### 表

| カラム1 | カラム2 | カラム3 |
|---------|---------|---------|
| データ1 | データ2 | データ3 |
| データ4 | データ5 | データ6 |

### 水平線

---

### 数式（LaTeX）

インライン数式: $E = mc^2$

ブロック数式:
$$
\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}
$$""",
                height=400,
                key=f"{self.id}_markdown"
            )
            
            unsafe_allow_html = st.checkbox(
                "HTMLを許可",
                value=False,
                key=f"{self.id}_html"
            )
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        st.markdown(markdown_text, unsafe_allow_html=unsafe_allow_html)
        
        # HTML例
        if unsafe_allow_html:
            st.divider()
            st.subheader("🎯 HTML使用例")
            html_markdown = """
<div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
    <h3 style="color: #FF4B4B;">カスタムスタイル</h3>
    <p style="font-size: 18px;">HTMLタグとCSSを使用した<span style="color: blue;">カラフル</span>なテキスト</p>
    <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
        ボタン（装飾のみ）
    </button>
</div>
"""
            st.markdown(html_markdown, unsafe_allow_html=True)
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key=f"{self.id}_demo_code")
        
        return None
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st

# Markdown表示
st.markdown("# 見出し1")
st.markdown("## 見出し2")
st.markdown("**太字** と *イタリック*")
st.markdown("- リスト項目1\\n- リスト項目2")

# リンク
st.markdown("[Streamlit](https://streamlit.io)")

# 数式
st.markdown("インライン数式: $E = mc^2$")"""
        
        elif level == "advanced":
            return """import streamlit as st

# カスタムスタイルのMarkdown
st.markdown(\"\"\"
<style>
.big-font {
    font-size: 30px !important;
    color: #FF4B4B;
}
</style>
\"\"\", unsafe_allow_html=True)

st.markdown('<p class="big-font">カスタムスタイルテキスト</p>', unsafe_allow_html=True)

# 複雑なMarkdown
st.markdown(\"\"\"
### 📊 データ分析レポート

**概要:**
本レポートでは、以下の項目について分析します：

1. **データ収集** - APIからのデータ取得
2. **前処理** - クリーニングと正規化
3. **分析** - 統計的手法の適用
4. **可視化** - グラフとチャート

---

#### 結果サマリー

| メトリクス | 値 | 前月比 |
|------------|-----|---------|
| 売上 | $10,000 | +15% |
| ユーザー数 | 1,500 | +8% |
| コンバージョン率 | 3.2% | +0.5% |

> 💡 **注意**: これらの数値は仮のデータです

$$
ROI = \\frac{利益 - 投資額}{投資額} \\times 100
$$
\"\"\")"""
        
        else:  # full
            return """import streamlit as st

def create_report(title, data, metrics):
    \"\"\"Markdownレポートを生成\"\"\"
    
    # レポートヘッダー
    st.markdown(f\"\"\"
    # {title}
    
    **作成日**: {pd.Timestamp.now().strftime('%Y年%m月%d日')}
    
    ---
    \"\"\")
    
    # メトリクスセクション
    st.markdown("## 📊 主要指標")
    
    cols = st.columns(len(metrics))
    for col, (key, value) in zip(cols, metrics.items()):
        with col:
            st.markdown(f\"\"\"
            <div style="text-align: center; padding: 20px; 
                        background-color: #f0f0f0; border-radius: 10px;">
                <h3 style="color: #262730; margin: 0;">{key}</h3>
                <p style="font-size: 24px; font-weight: bold; 
                         color: #FF4B4B; margin: 10px 0;">{value}</p>
            </div>
            \"\"\", unsafe_allow_html=True)
    
    # データテーブル
    st.markdown("## 📋 詳細データ")
    st.dataframe(data)
    
    # 分析結果
    st.markdown(\"\"\"
    ## 🔍 分析結果
    
    ### 主な発見
    
    1. **成長トレンド**
       - 前年比で25%の成長を達成
       - 特に第3四半期の伸びが顕著
    
    2. **改善ポイント**
       - コンバージョン率の最適化が必要
       - ユーザーエンゲージメントの向上余地あり
    
    ### 推奨アクション
    
    - [ ] A/Bテストの実施
    - [ ] UIの改善
    - [ ] パフォーマンス最適化
    
    ---
    
    > 📌 **次回レビュー**: 2週間後に進捗確認
    \"\"\")

def main():
    st.title("Markdownレポートジェネレーター")
    
    # サンプルデータ
    import pandas as pd
    import numpy as np
    
    data = pd.DataFrame({
        '月': ['1月', '2月', '3月', '4月', '5月'],
        '売上': [100, 120, 135, 128, 145],
        'ユーザー': [1000, 1200, 1350, 1300, 1450]
    })
    
    metrics = {
        '総売上': '$628,000',
        '平均成長率': '+15.2%',
        'ユーザー数': '6,300'
    }
    
    create_report("月次パフォーマンスレポート", data, metrics)

if __name__ == "__main__":
    main()"""


class HeadingComponents(BaseComponent):
    """見出し系コンポーネント (title, header, subheader, caption)"""
    
    def __init__(self):
        super().__init__("headings", "display_widgets")
        self.metadata = {
            'id': 'headings',
            'name': 'Heading Components',
            'category': 'display_widgets',
            'description': '見出し系コンポーネント。title, header, subheader, captionを含む。',
            'components': ['st.title', 'st.header', 'st.subheader', 'st.caption'],
            'tips': [
                'title: 最も大きい見出し（ページタイトル用）',
                'header: セクション見出し（H2相当）',
                'subheader: サブセクション見出し（H3相当）',
                'caption: 小さな説明文や注釈',
                'anchor引数でアンカーリンクを設定可能'
            ],
            'related': ['markdown', 'text', 'write'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                title_text = st.text_input(
                    "Title テキスト",
                    value="ページタイトル",
                    key="heading_title"
                )
                header_text = st.text_input(
                    "Header テキスト",
                    value="セクション見出し",
                    key="heading_header"
                )
            
            with col2:
                subheader_text = st.text_input(
                    "Subheader テキスト",
                    value="サブセクション",
                    key="heading_subheader"
                )
                caption_text = st.text_input(
                    "Caption テキスト",
                    value="これは説明文です",
                    key="heading_caption"
                )
                
                use_anchor = st.checkbox(
                    "アンカーリンクを使用",
                    value=False,
                    key="heading_anchor"
                )
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        # 各見出しの表示
        if use_anchor:
            st.title(title_text, anchor="title-anchor")
            st.header(header_text, anchor="header-anchor")
            st.subheader(subheader_text, anchor="subheader-anchor")
        else:
            st.title(title_text)
            st.header(header_text)
            st.subheader(subheader_text)
        
        st.caption(caption_text)
        
        # サイズ比較
        with st.expander("🎯 サイズ比較"):
            st.title("st.title - 最大サイズ")
            st.header("st.header - 大サイズ")
            st.subheader("st.subheader - 中サイズ")
            st.write("st.write - 通常サイズ")
            st.caption("st.caption - 小サイズ")
        
        # 実践例
        with st.expander("📝 実践的な使用例"):
            st.title("📊 売上分析ダッシュボード")
            st.caption("最終更新: 2024年1月1日")
            
            st.header("月次レポート")
            st.subheader("売上推移")
            st.caption("※ 前年同月比で15%増加")
            
            st.subheader("地域別実績")
            st.caption("※ 関東地域が全体の40%を占める")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="heading_demo_code")
        
        return None
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st

# 見出しの階層
st.title("ページタイトル")
st.header("セクション見出し")
st.subheader("サブセクション見出し")
st.caption("小さな説明文や注釈")

# アンカーリンク付き
st.header("セクション1", anchor="section-1")
st.subheader("サブセクション1.1", anchor="subsection-1-1")"""
        
        elif level == "advanced":
            return """import streamlit as st

# ページ構成の例
st.title("📊 データ分析アプリケーション")
st.caption("Version 1.0.0 | Last updated: 2024-01-01")

st.header("1. データ入力")
st.caption("CSVファイルをアップロードしてください")

# ファイルアップロード処理
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:
    st.header("2. データ分析")
    
    st.subheader("2.1 基本統計")
    st.caption("データの基本的な統計情報を表示")
    
    st.subheader("2.2 可視化")
    st.caption("グラフによるデータの可視化")
    
    st.header("3. レポート出力")
    st.caption("分析結果のダウンロード")"""
        
        else:  # full
            return """import streamlit as st
import pandas as pd

def create_dashboard():
    \"\"\"ダッシュボードの作成\"\"\"
    
    # ページヘッダー
    st.title("🚀 ビジネスインテリジェンスダッシュボード")
    st.caption(f"最終更新: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    
    # ナビゲーション
    tab1, tab2, tab3 = st.tabs(["📈 概要", "📊 詳細分析", "📋 レポート"])
    
    with tab1:
        st.header("エグゼクティブサマリー")
        st.caption("主要KPIの概要")
        
        # KPIカード
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("売上高")
            st.metric("2024年1月", "$1.2M", "+15%")
            st.caption("前年同月比")
        
        with col2:
            st.subheader("顧客数")
            st.metric("アクティブユーザー", "5,234", "+8%")
            st.caption("前月比")
        
        with col3:
            st.subheader("満足度")
            st.metric("NPS スコア", "72", "+5")
            st.caption("前四半期比")
    
    with tab2:
        st.header("詳細分析")
        
        st.subheader("トレンド分析")
        st.caption("過去12ヶ月の推移")
        
        # ダミーデータでチャート
        import numpy as np
        chart_data = pd.DataFrame(
            np.random.randn(12, 3),
            columns=['売上', '利益', 'コスト']
        )
        st.line_chart(chart_data)
        
        st.subheader("セグメント別分析")
        st.caption("顧客セグメント別の売上構成")
        
        # セグメントデータ
        segment_data = pd.DataFrame({
            'セグメント': ['エンタープライズ', '中小企業', '個人'],
            '売上': [500000, 400000, 300000],
            '構成比': ['41.7%', '33.3%', '25.0%']
        })
        st.dataframe(segment_data)
    
    with tab3:
        st.header("レポート生成")
        st.caption("分析結果をレポート形式で出力")
        
        st.subheader("レポート設定")
        
        report_type = st.selectbox(
            "レポートタイプ",
            ["月次レポート", "四半期レポート", "年次レポート"]
        )
        
        if st.button("レポート生成"):
            st.success("レポートを生成しました")
            st.download_button(
                label="PDFダウンロード",
                data=b"dummy pdf content",
                file_name=f"{report_type}.pdf",
                mime="application/pdf"
            )

def main():
    st.set_page_config(
        page_title="BIダッシュボード",
        page_icon="📊",
        layout="wide"
    )
    
    create_dashboard()

if __name__ == "__main__":
    main()"""


class CodeComponent(BaseComponent):
    """st.code コンポーネント"""
    
    def __init__(self):
        super().__init__("code", "display_widgets")
        self.metadata = {
            'id': 'code',
            'name': 'st.code',
            'category': 'display_widgets',
            'description': 'シンタックスハイライト付きのコードブロック表示。プログラミング言語を自動認識。',
            'parameters': [
                {
                    'name': 'body',
                    'type': 'str',
                    'required': True,
                    'default': '',
                    'description': '表示するコード'
                },
                {
                    'name': 'language',
                    'type': 'str',
                    'required': False,
                    'default': None,
                    'description': 'プログラミング言語'
                }
            ],
            'tips': [
                '150以上の言語をサポート',
                'language引数で言語を明示的に指定',
                '自動的にコピーボタンが表示される',
                '行番号は自動的に表示される',
                'Markdownのコードブロックよりも高機能'
            ],
            'related': ['markdown', 'text', 'echo'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                language = st.selectbox(
                    "プログラミング言語",
                    ["python", "javascript", "java", "cpp", "go", "rust", 
                     "sql", "html", "css", "bash", "yaml", "json"],
                    key="code_language"
                )
            
            with col2:
                sample_type = st.radio(
                    "サンプルタイプ",
                    ["基本", "関数", "クラス"],
                    key="code_sample"
                )
            
            # 言語別サンプルコード
            samples = {
                "python": {
                    "基本": "print('Hello, World!')\nx = 42\ny = x * 2",
                    "関数": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Fibonacci(10) = {result}")""",
                    "クラス": """class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"

person = Person("Alice", 30)
print(person.greet())"""
                },
                "javascript": {
                    "基本": "console.log('Hello, World!');\nconst x = 42;\nconst y = x * 2;",
                    "関数": """function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(10);
console.log(`Fibonacci(10) = ${result}`);""",
                    "クラス": """class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    greet() {
        return `Hello, I'm ${this.name}`;
    }
}

const person = new Person("Alice", 30);
console.log(person.greet());"""
                }
            }
            
            # デフォルトコード
            default_code = samples.get(language, {}).get(
                sample_type,
                f"// {language} code example\n// Sample {sample_type}"
            )
            
            code_input = st.text_area(
                "コード内容",
                value=default_code,
                height=200,
                key="code_input"
            )
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        st.code(code_input, language=language)
        
        # 複数言語の例
        with st.expander("🎯 様々な言語の表示例"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**SQL:**")
                st.code("""SELECT name, age, city
FROM users
WHERE age > 18
ORDER BY name ASC;""", language="sql")
                
                st.write("**JSON:**")
                st.code("""{
  "name": "John Doe",
  "age": 30,
  "email": "john@example.com"
}""", language="json")
            
            with col2:
                st.write("**HTML:**")
                st.code("""<div class="container">
  <h1>Title</h1>
  <p>Content</p>
</div>""", language="html")
                
                st.write("**YAML:**")
                st.code("""name: CI/CD Pipeline
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest""", language="yaml")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="code_demo_code")
        
        return None
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if level == "basic":
            return '''import streamlit as st

# コード表示（言語自動検出）
st.code("""
def hello():
    print("Hello, World!")
""")

# 言語を指定
st.code("""
SELECT * FROM users
WHERE age > 18
""", language="sql")'''
        
        elif level == "advanced":
            return '''import streamlit as st

# 動的なコード表示
language = st.selectbox("言語選択", ["python", "javascript", "sql"])

code_samples = {
    "python": """
def process_data(data):
    return [x * 2 for x in data]
    
result = process_data([1, 2, 3, 4, 5])
print(result)
""",
    "javascript": """
const processData = (data) => {
    return data.map(x => x * 2);
};

const result = processData([1, 2, 3, 4, 5]);
console.log(result);
""",
    "sql": """
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS total
    FROM orders
    GROUP BY 1
)
SELECT * FROM monthly_sales
ORDER BY month DESC;
"""
}

st.code(code_samples[language], language=language)'''
        
        else:  # full
            return '''import streamlit as st

def code_editor_demo():
    """コードエディタ風のデモ"""
    
    st.title("📝 コードスニペットマネージャー")
    
    # コードスニペットのカテゴリ
    category = st.selectbox(
        "カテゴリ",
        ["データ処理", "API連携", "機械学習", "Web開発"]
    )
    
    # カテゴリ別スニペット
    snippets = {
        "データ処理": {
            "CSVの読み込み": """import pandas as pd

# CSVファイルの読み込み
df = pd.read_csv('data.csv')

# 基本情報の表示
print(df.head())
print(df.info())
print(df.describe())""",
            
            "データクリーニング": """# 欠損値の処理
df.dropna(inplace=True)  # 欠損値を削除
# または
df.fillna(0, inplace=True)  # 欠損値を0で埋める

# 重複の削除
df.drop_duplicates(inplace=True)

# データ型の変換
df['date'] = pd.to_datetime(df['date'])
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')"""
        },
        "API連携": {
            "REST API呼び出し": """import requests

# GET リクエスト
response = requests.get('https://api.example.com/users')
if response.status_code == 200:
    data = response.json()
    print(data)

# POST リクエスト
payload = {'name': 'John', 'email': 'john@example.com'}
response = requests.post('https://api.example.com/users', json=payload)""",
            
            "認証付きAPI": """import requests

# Bearer Token認証
headers = {
    'Authorization': 'Bearer YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.example.com/protected',
    headers=headers
)"""
        }
    }
    
    # スニペット選択
    if category in snippets:
        snippet_name = st.selectbox(
            "スニペット",
            list(snippets[category].keys())
        )
        
        # コード表示
        st.subheader(f"📌 {snippet_name}")
        code = snippets[category][snippet_name]
        
        # 言語検出（簡易版）
        if "import pandas" in code or "import requests" in code:
            language = "python"
        else:
            language = None
        
        st.code(code, language=language)
        
        # アクション
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 コピー"):
                st.success("コピーしました！")
        with col2:
            if st.button("✏️ 編集"):
                st.info("編集モード（実装予定）")
        with col3:
            if st.button("🗑️ 削除"):
                st.warning("削除確認（実装予定）")
        
        # 説明
        with st.expander("📖 説明"):
            st.write(f"このスニペットは{category}に関する{snippet_name}のコード例です。")
            st.write("必要に応じてパラメータを調整してください。")

def main():
    code_editor_demo()

if __name__ == "__main__":
    main()'''


class MessageComponents(BaseComponent):
    """メッセージ系コンポーネント (success, info, warning, error)"""
    
    def __init__(self):
        super().__init__("messages", "display_widgets")
        self.metadata = {
            'id': 'messages',
            'name': 'Message Components',
            'category': 'display_widgets',
            'description': 'メッセージ表示コンポーネント。success, info, warning, errorの4種類。',
            'components': ['st.success', 'st.info', 'st.warning', 'st.error'],
            'tips': [
                'success: 成功メッセージ（緑）',
                'info: 情報メッセージ（青）',
                'warning: 警告メッセージ（黄）',
                'error: エラーメッセージ（赤）',
                'アイコンは自動的に表示される'
            ],
            'related': ['balloons', 'snow', 'toast', 'exception'],
            'version_added': '0.1.0'
        }
    
    def render_demo(self) -> Any:
        """デモをレンダリング"""
        with st.expander("⚙️ パラメータ設定", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                success_text = st.text_input(
                    "Success メッセージ",
                    value="✅ 処理が正常に完了しました",
                    key="msg_success"
                )
                info_text = st.text_input(
                    "Info メッセージ",
                    value="ℹ️ お知らせ：新機能が追加されました",
                    key="msg_info"
                )
            
            with col2:
                warning_text = st.text_input(
                    "Warning メッセージ",
                    value="⚠️ 注意：データの一部が不完全です",
                    key="msg_warning"
                )
                error_text = st.text_input(
                    "Error メッセージ",
                    value="❌ エラー：ファイルが見つかりません",
                    key="msg_error"
                )
            
            icon_usage = st.checkbox(
                "カスタムアイコンを含める",
                value=True,
                help="メッセージにアイコンを含めるかどうか",
                key="msg_icon"
            )
        
        # デモ実行
        st.divider()
        st.subheader("📺 実行結果")
        
        st.success(success_text)
        st.info(info_text)
        st.warning(warning_text)
        st.error(error_text)
        
        # 実践例
        with st.expander("🎯 実践的な使用例"):
            st.write("**フォーム送信の例:**")
            
            name = st.text_input("名前", key="form_name")
            email = st.text_input("メール", key="form_email")
            
            if st.button("送信"):
                if not name:
                    st.error("名前を入力してください")
                elif not email:
                    st.error("メールアドレスを入力してください")
                elif "@" not in email:
                    st.warning("有効なメールアドレスを入力してください")
                else:
                    st.success(f"フォームを送信しました！ ({name}, {email})")
                    st.info("確認メールを送信しました")
        
        # バリエーション
        with st.expander("💡 メッセージのバリエーション"):
            st.success("処理完了 ✅")
            st.success("データを正常に保存しました")
            st.success("🎉 おめでとうございます！目標を達成しました！")
            
            st.info("💡 ヒント：Ctrl+Sで保存できます")
            st.info("📢 新しいバージョンが利用可能です")
            st.info("🔄 データを更新中...")
            
            st.warning("⚠️ メモリ使用量が80%を超えています")
            st.warning("🔋 バッテリー残量が少なくなっています")
            st.warning("📊 一部のデータが欠損しています")
            
            st.error("🚫 アクセスが拒否されました")
            st.error("💔 接続が切断されました")
            st.error("⏰ タイムアウトエラー")
        
        # コード表示
        st.divider()
        st.subheader("💻 生成されたコード")
        code = self.get_code("basic")
        code_display.display_with_copy(code, key="messages_demo_code")
        
        return None
    
    def get_code(self, level: str = "basic", params: Optional[Dict] = None) -> str:
        """コードを取得"""
        if level == "basic":
            return """import streamlit as st

# メッセージの表示
st.success("処理が正常に完了しました")
st.info("新機能が追加されました")
st.warning("データの一部が不完全です")
st.error("ファイルが見つかりません")"""
        
        elif level == "advanced":
            return """import streamlit as st

# データ処理の状態表示
def process_data(data):
    try:
        st.info("データ処理を開始します...")
        
        # バリデーション
        if not data:
            st.error("データが空です")
            return None
        
        if len(data) < 10:
            st.warning("データが少ないため、精度が低い可能性があります")
        
        # 処理実行
        result = perform_analysis(data)
        
        st.success(f"✅ 処理完了！{len(result)}件のデータを分析しました")
        return result
        
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {str(e)}")
        return None

# フォームバリデーション
with st.form("data_form"):
    value = st.number_input("値を入力", min_value=0)
    submitted = st.form_submit_button("送信")
    
    if submitted:
        if value < 10:
            st.warning("値が小さすぎる可能性があります")
        elif value > 1000:
            st.warning("値が大きすぎる可能性があります")
        else:
            st.success("値が適切な範囲内です")"""
        
        else:  # full
            return """import streamlit as st
import time
import random

def file_upload_handler():
    \"\"\"ファイルアップロードのハンドラー\"\"\"
    
    st.header("📁 ファイルアップロード")
    
    uploaded_file = st.file_uploader(
        "ファイルを選択",
        type=['csv', 'txt', 'json']
    )
    
    if uploaded_file is not None:
        # ファイル情報
        file_details = {
            "ファイル名": uploaded_file.name,
            "ファイルサイズ": f"{uploaded_file.size:,} bytes",
            "ファイルタイプ": uploaded_file.type
        }
        
        st.info(f"📄 {uploaded_file.name} がアップロードされました")
        
        # ファイルサイズチェック
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            st.warning("⚠️ ファイルサイズが大きいため、処理に時間がかかる可能性があります")
        
        # 処理開始
        if st.button("ファイルを処理"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # ステップ1: バリデーション
                status_text.text("ファイルを検証中...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                # ファイルタイプチェック
                if uploaded_file.type not in ['text/csv', 'text/plain', 'application/json']:
                    st.error("❌ サポートされていないファイル形式です")
                    return
                
                # ステップ2: データ読み込み
                status_text.text("データを読み込み中...")
                progress_bar.progress(50)
                time.sleep(0.5)
                
                # ステップ3: 処理
                status_text.text("データを処理中...")
                progress_bar.progress(75)
                time.sleep(0.5)
                
                # ランダムな結果シミュレーション
                success_rate = random.random()
                
                if success_rate > 0.8:
                    # 成功
                    progress_bar.progress(100)
                    status_text.text("完了！")
                    st.success("✅ ファイルの処理が正常に完了しました")
                    st.balloons()
                    
                    # 結果表示
                    with st.expander("処理結果"):
                        st.write("**処理されたレコード数**: 1,234")
                        st.write("**処理時間**: 2.3秒")
                        st.write("**エラー数**: 0")
                    
                elif success_rate > 0.3:
                    # 部分的成功
                    progress_bar.progress(100)
                    st.warning("⚠️ 処理は完了しましたが、一部のデータにエラーがありました")
                    
                    with st.expander("詳細"):
                        st.write("**成功**: 1,200件")
                        st.write("**失敗**: 34件")
                        st.write("エラーの詳細はログファイルを確認してください")
                else:
                    # 失敗
                    st.error("❌ 処理中にエラーが発生しました")
                    st.error("データ形式を確認してください")
                    
            except Exception as e:
                st.error(f"❌ 予期しないエラー: {str(e)}")
                st.info("サポートにお問い合わせください")
            
            finally:
                progress_bar.empty()
                status_text.empty()
    
    else:
        st.info("ℹ️ ファイルをアップロードしてください")

def main():
    st.title("メッセージコンポーネントデモ")
    
    file_upload_handler()
    
    # ステータスダッシュボード
    st.header("📊 システムステータス")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if random.random() > 0.2:
            st.success("✅ API: 正常")
        else:
            st.error("❌ API: 接続エラー")
    
    with col2:
        if random.random() > 0.3:
            st.success("✅ DB: 正常")
        else:
            st.warning("⚠️ DB: 遅延あり")
    
    with col3:
        st.info("ℹ️ キャッシュ: 更新中")

if __name__ == "__main__":
    main()"""


# コンポーネントのエクスポート
__all__ = [
    'WriteComponent', 
    'MarkdownComponent', 
    'HeadingComponents',
    'CodeComponent',
    'MessageComponents'
]