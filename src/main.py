import json
from pathlib import Path

from dotenv import load_dotenv

from stock import get_market_conditions, get_stock_info
from news import get_economic_news
from discord import send_markdown
from gemini import generate_content

PROJECT_ROOT = Path(__file__).parent.parent
TICKERS_FILE = PROJECT_ROOT / "config" / "tickers.json"
MARKDOWN_TEMPLATE = PROJECT_ROOT / "config" / "template.md"

load_dotenv()

def build_system_instruction() -> str:
    with open(MARKDOWN_TEMPLATE, "r") as f:
        markdown_template = f.read()

    return \
f"""
あなたはプロの証券アナリストです。
提供されたjsonデータを元に、客観的な視点で分析を行なってください。

## 出力ルール
- 挨拶、結びの言葉、ユーザーへの問いかけは一切禁止します
- 出力フォーマットのMarkdownテンプレートに従って出力してください
- 出力フォーマットに含まれる「（状況コメント）」は、その行に対する簡潔なコメントに置き換えて出力してください

## 出力フォーマット
```markdown
{markdown_template}
```
"""


def build_prompt(data: dict) -> str:
    return \
f"""\
以下の銘柄のデータを分析してください。
```json
{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}
```
"""

if __name__ == "__main__":
    with open(TICKERS_FILE, "r") as f:
        tickers = json.load(f)

    system_instruction = build_system_instruction()

    economic_news = get_economic_news()
    market_conditions = get_market_conditions()

    for ticker in tickers:
        stock_info = get_stock_info(ticker)

        response = generate_content(
            contents=build_prompt({
                "economic_news": economic_news,
                "market_conditions": market_conditions,
                "stock_info": stock_info,
            }),
            config={"system_instruction": system_instruction}
        )

        send_markdown(response)