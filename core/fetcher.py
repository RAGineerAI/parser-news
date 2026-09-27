"""
Модуль загрузки HTML-страниц.

Отвечает за:
    - HTTP-запросы к сайтам
    - Вежливые паузы между запросами
    - Логирование процесса загрузки
"""

import time
import logging

import requests

logger = logging.getLogger(__name__)

def fetch_page(url: str, user_agent: str, delay: float = 1.0) -> str:
    """
    Загружает HTML-страницу по URL.

    Args:
        url: адрес страницы
        user_agent: строка User-Agent для заголовка
        delay: пауза после запроса (сек)

    Returns:
        HTML-код страницы (строка)

    Raises:
        requests.HTTPError: если сервер вернул 4xx/5xx
        requests.RequestException: при таймауте или ошибке соединения
    """
    logger.info(f"Загрузка: {url}")

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.error(f"HTTP-ошибка для {url}: {e}")
        raise
    except requests.RequestException as e:
        logger.error(f"Ошибка соединения для {url}: {e}")
        raise

    time.sleep(delay)

    logger.info(f"Успешно загружено: {len(response.text)} символов")

    return response.text