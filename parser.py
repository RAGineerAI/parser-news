"""
Простой парсер цитат с quotes.toscrape.com

Извлекает: текст, автора, теги.
Сохраняет в JSON и CSV.
"""

import json
import csv
import time
from typing import List, Dict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import BASE_URL, OUTPUT_DIR, REQUEST_DELAY, USER_AGENT

def fetch_page(url: str) -> str:
    """
    Загружает HTML-страницу по URL.

    Args:
        url: адрес страницы

    Returns:
        HTML-код страницы (строка)

    Raises:
        requests.HTTPError: если сервер вернул ошибку (4xx, 5xx)
    """
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # выбросит ошибку, если статус >= 400

    # Вежливая пауза
    time.sleep(REQUEST_DELAY)

    return response.text

def parse_quote(quote_element) -> Dict:
    """
    Извлекает данные из одной цитаты.

    Args:
        quote_element: BeautifulSoup-элемент div.quote

    Returns:
        Словарь: {"text": ..., "author": ..., "tags": [...]}
    """
    text = quote_element.find("span", class_="text").text.strip()
    author = quote_element.find("small", class_="author").text.strip()

    tags_elements = quote_element.find_all("a", class_="tag")
    tags = [t.text.strip() for t in tags_elements]

    return {
        "text": text,
        "author": author,
        "tags": tags,
    }

def parse_page(url: str) -> List[Dict]:
    """
    Парсит одну страницу и возвращает список цитат.

    Args:
        url: адрес страницы

    Returns:
        Список словарей с цитатами
    """
    html = fetch_page(url)
    soup = BeautifulSoup(html, "lxml")

    quote_elements = soup.find_all("div", class_="quote")

    quotes = []
    for quote_element in quote_elements:
        quote = parse_quote(quote_element)
        quotes.append(quote)

    return quotes

def save_json(quotes: List[Dict], filename: str = "quotes.json") -> None:
    """Сохраняет цитаты в JSON-файл."""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    filepath = Path(OUTPUT_DIR) / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    print(f"💾 JSON сохранён: {filepath}")


def save_csv(quotes: List[Dict], filename: str = "quotes.csv") -> None:
    """Сохраняет цитаты в CSV-файл."""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    filepath = Path(OUTPUT_DIR) / filename

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()

        for quote in quotes:
            row = quote.copy()
            row["tags"] = ", ".join(row["tags"])  # список → строка
            writer.writerow(row)

    print(f"💾 CSV сохранён: {filepath}")

def main():
    """Главная функция парсера."""
    print("🚀 Запуск парсера цитат")
    print("=" * 50)

    url = BASE_URL
    print(f"🌐 Загружаем: {url}")

    quotes = parse_page(url)
    print(f"✅ Найдено цитат: {len(quotes)}")

    save_json(quotes)
    save_csv(quotes)

    print("\n📊 Первые 3 цитаты:")
    for i, quote in enumerate(quotes[:3], start=1):
        print(f"\n  {i}. {quote['author']}")
        print(f"     {quote['text'][:80]}...")
        print(f"     Теги: {', '.join(quote['tags'])}")


if __name__ == "__main__":
    main()