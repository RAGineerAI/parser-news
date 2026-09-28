"""
Точка входа парсера.

Использование:
    python main.py --site habr
    python main.py --sites habr,rbc
    python main.py --all
"""

import argparse
import logging
import sys
from pathlib import Path

from core.config_loader import load_site_config
from core.fetcher import fetch_page
from core.extractor import extract_all
from core.exporter import export_all


def setup_logging(log_file: str = "parser.log") -> None:
    """
    Настраивает логирование: в консоль (INFO) и в файл (DEBUG).
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Формат сообщений
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Хендлер в файл (всё: DEBUG+)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Хендлер в консоль (только INFO+)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def process_site(site_name: str) -> bool:
    """
    Обрабатывает один сайт: загружает конфиг, HTML, извлекает, экспортирует.

    Args:
        site_name: имя сайта (например, "habr")

    Returns:
        True если успешно, False при ошибке
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Обработка сайта: {site_name}")

    try:
        # 1. Загружаем конфиг
        config = load_site_config(site_name)

        # 2. Загружаем HTML
        html = fetch_page(
            url=config["base_url"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            delay=config.get("request_delay", 1.0)
        )
        logger.info(f"Загружено {len(html)} символов")

        # 3. Извлекаем данные
        data = extract_all(
            html=html,
            list_selector=config["list_selector"],
            fields_config=config["fields"]
        )
        logger.info(f"Извлечено записей: {len(data)}")

        if not data:
            logger.warning(f"Нет данных для {site_name}")
            return False

        # 4. Экспортируем
        paths = export_all(data, site_name)
        logger.info(f"Сохранено: {paths['json']}")
        logger.info(f"Сохранено: {paths['csv']}")

        return True

    except FileNotFoundError as e:
        logger.error(f"Конфиг не найден: {e}")
        return False
    except Exception as e:
        logger.error(f"Ошибка при обработке {site_name}: {e}")
        return False  
    
def parse_args() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Парсер новостных сайтов"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--site",
        type=str,
        help="Имя одного сайта (например, habr)"
    )

    group.add_argument(
        "--sites",
        type=str,
        help="Несколько сайтов через запятую (habr,rbc)"
    )

    group.add_argument(
        "--all",
        action="store_true",
        help="Обработать все сайты из папки sites/"
    )

    return parser.parse_args()


def main() -> None:
    """Главная функция."""
    setup_logging()
    logger = logging.getLogger(__name__)

    args = parse_args()

    # Определяем список сайтов
    if args.site:
        sites = [args.site]
    elif args.sites:
        sites = [s.strip() for s in args.sites.split(",")]
    else:  # --all
        sites_dir = Path("sites")
        sites = [f.stem for f in sites_dir.glob("*.yaml")]

    logger.info(f"Сайтов к обработке: {len(sites)} → {', '.join(sites)}")

    # Обрабатываем
    success = 0
    for site in sites:
        if process_site(site):
            success += 1

    logger.info(f"Итог: {success}/{len(sites)} сайтов обработано")


if __name__ == "__main__":
    main()  