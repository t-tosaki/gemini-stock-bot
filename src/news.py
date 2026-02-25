import re
from html.parser import HTMLParser

import feedparser

ECONOMIC_NEWS_RSS_URL = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtcGhHZ0pLVUNnQVAB?hl=ja&ceid=JP:ja&gl=JP"

class HTMLToTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data.strip())

    def get_text(self):
        return ' '.join([t for t in self.text if t])


def _remove_html_tags(html_text: str) -> str:
    li_pattern = r'<li[^>]*>(.*?)</li>'
    li_items = re.findall(li_pattern, html_text, re.DOTALL)

    cleaned_lines = []
    for item in li_items:
        parser = HTMLToTextParser()
        parser.feed(item)
        text = parser.get_text()

        if text:
            if not text.endswith(('。', '．', '.')):
                text += '。'
            cleaned_lines.append(text)

    return ''.join(cleaned_lines)

def get_economic_news(limit: int = 15) -> list[dict]:
    try:
        feed = feedparser.parse(ECONOMIC_NEWS_RSS_URL)

        if not feed.entries:
            raise RuntimeError("Failed to retrieve economic news: no entries found.")

        news_list = []
        for i in range(min(limit, len(feed.entries))):
            entry = feed.entries[i]
            summary_html = entry.get('summary', '')
            summary_text = _remove_html_tags(summary_html)

            news_item = {
                "title": entry.get('title'),
                "link": entry.get('link'),
                "publishTime": entry.get('published'),
                "summary": summary_text
            }
            news_list.append(news_item)

        return news_list
    except Exception:
        return []

if __name__ == "__main__":
    news = get_economic_news()
    print(news)