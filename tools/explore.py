"""
Инструмент разведки HTML-страниц.

Помогает найти селекторы для нового сайта:
    - Показывает какие теги есть на странице
    - Сколько раз каждый встречается
    - Возможные контейнеры элементов

Использование:
    python tools/explore.py https://habr.com/ru/articles/
    python tools/explore.py https://habr.com/ru/articles/ --tag article
"""

import sys
import argparse
from pathlib import Path
from collections import Counter

import requests
from bs4 import BeautifulSoup

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.fetcher import fetch_page


# 🆕 Теги, которые могут быть контейнерами
CONTAINER_TAGS = {"article", "div", "li", "tr", "section", "ul", "ol"}


def explore_tags(soup: BeautifulSoup, top_n: int = 20) -> None:
    """
    Показывает какие теги есть на странице и возможные контейнеры.
    """
    all_tags = [tag.name for tag in soup.find_all()]

    if not all_tags:
        print("❌ Не найдено ни одного тега")
        return

    counter = Counter(all_tags)

    print(f"\n{'='*60}")
    print(f"📊 Уникальных тегов: {len(counter)}")
    print(f"📊 Всего тегов: {len(all_tags)}")
    print(f"{'='*60}\n")

    # Общий список тегов
    print(f"{'Тег':<15} {'Количество':>12}")
    print("-" * 30)
    for tag_name, count in counter.most_common(top_n):
        print(f"{tag_name:<15} {count:>12}")

    # Подозрительные контейнеры
    print(f"\n{'='*60}")
    print("🔍 Возможные контейнеры элементов:")
    print(f"{'='*60}\n")

    containers = []

    for tag in soup.find_all():
        # Только теги-контейнеры
        if tag.name not in CONTAINER_TAGS:
            continue

        # Только теги с классом
        classes = tag.get("class")
        if not classes:
            continue

        class_str = ".".join(classes)
        selector = f"{tag.name}.{class_str}"

        count = len(soup.select(selector))

        # Отбираем «золотую середину»
        if 5 <= count <= 100:
            containers.append((selector, count))

    # Убираем дубликаты, сортируем
    unique_containers = dict(containers)

    sorted_containers = sorted(
        unique_containers.items(),
        key=lambda x: x[1],
        reverse=True
    )

    if not sorted_containers:
        print("Не найдено подозрительных контейнеров")
        return

    print(f"{'Селектор':<50} {'Количество':>12}")
    print("-" * 65)
    for selector, count in sorted_containers[:15]:
        print(f"{selector:<50} {count:>12}")


def explore_element(soup: BeautifulSoup, tag_name: str, limit: int = 1) -> None:
    """
    Показывает HTML первых N элементов указанного тега.
    """
    elements = soup.find_all(tag_name)

    if not elements:
        print(f"❌ Тег '{tag_name}' не найден на странице")
        return

    print(f"\n{'='*60}")
    print(f"🔍 Тег '{tag_name}': найдено {len(elements)} элементов")
    print(f"Показываю первые {min(limit, len(elements))}")
    print(f"{'='*60}\n")

    for i, element in enumerate(elements[:limit], start=1):
        print(f"--- Элемент #{i} ---")
        print(element.prettify()[:2000])
        print()


def parse_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент разведки HTML-страниц"
    )

    parser.add_argument(
        "url",
        type=str,
        help="URL страницы для исследования"
    )

    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Показать детали конкретного тега (например, article)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Сколько элементов показать (по умолчанию 1)"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Пауза между запросами (сек)"
    )

    return parser.parse_args()


def main() -> None:
    """Главная функция."""
    args = parse_args()

    print(f"🌐 Загружаем: {args.url}")

    html = fetch_page(
        url=args.url,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        delay=args.delay
    )

    print(f"📥 Загружено: {len(html)} символов")

    soup = BeautifulSoup(html, "lxml")

    if args.tag:
        explore_element(soup, args.tag, args.limit)
    else:
        explore_tags(soup)


if __name__ == "__main__":
    main()