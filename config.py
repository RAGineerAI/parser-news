"""
Настройки парсера.

Здесь хранятся все константы: URL, пути, параметры.
"""

# URL сайта для парсинга
BASE_URL = "http://quotes.toscrape.com/"

# Путь для сохранения результатов
OUTPUT_DIR = "output"

# Задержка между запросами (сек) — вежливость к серверу
REQUEST_DELAY = 1.0

# User-Agent — представляемся браузером
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)