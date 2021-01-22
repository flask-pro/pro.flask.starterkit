import requests
from flask import current_app

from nucleus.config import Config

TELEGRAM_API_URL = Config.TELEGRAM_API_URL
TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = Config.TELEGRAM_CHAT_ID


def send_to_telegram(message: str):
    if not (TELEGRAM_API_URL and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        current_app.logger.warning(
            "Telegram "
            "| Not set settings TELEGRAM_API_URL or TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID."
        )

    else:
        LINES_PER_MESSAGE = 50

        lines = message.splitlines(True)

        start_msg = 0
        msg_chunk = lines[start_msg:LINES_PER_MESSAGE]
        while msg_chunk:
            text = "".join(msg_chunk)
            try:
                response = requests.post(
                    f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendMessage",
                    data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
                )

                if response.status_code != 200:
                    current_app.logger.warning(
                        f"Telegram "
                        f"| Bad response "
                        f"| status code: {response.status_code} "
                        f"| body: {response.text}"
                    )
            except requests.exceptions.ConnectionError as exc:
                current_app.logger.warning(f"Telegram | Connection error | {repr(exc)}")

            start_msg = start_msg + LINES_PER_MESSAGE
            end_msg = start_msg + LINES_PER_MESSAGE
            msg_chunk = lines[start_msg:end_msg]
