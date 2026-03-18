from datetime import datetime

import requests

from config import settings


def parse_habit_time(time_str):
    """
    Парсит время из строки, поддерживая форматы HH:MM и HH:MM:SS.
    Возвращает объект time или None в случае ошибки.
    """
    if not time_str:
        return None

    # разные форматы времени
    formats = ["%H:%M:%S", "%H:%M"]

    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except (ValueError, TypeError):
            continue

    return None


def send_telegram_message(chat_id, message):
    """Интеграция сервиса с мессенджером Телеграм"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as e:
        return e
