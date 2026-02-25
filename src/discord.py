import os
import sys
from pathlib import Path

import requests

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL is not set")

def send_markdown(content: str) -> None:
    messages = []

    sections = content.split('\n## ')
    current_message = sections[0]

    for section in sections[1:]:
        section_with_header = f"\n## {section}"

        if len(current_message) + len(section_with_header) > 1900:
            if current_message.strip():
                messages.append(current_message)
            current_message = section_with_header
        else:
            current_message += section_with_header
    else:
        if current_message.strip():
            messages.append(current_message)

    for i, message in enumerate(messages, 1):
        try:
            response = requests.post(
                WEBHOOK_URL,
                json={"content": message},
                headers= {"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except Exception as e:
            print(f"エラー: メッセージ {i} の送信中にエラーが発生しました: {e}")

if __name__ == "__main__":
    send_markdown(sys.argv[1])