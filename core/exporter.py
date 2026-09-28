"""
Экспорт данных в JSON и CSV.

Отвечает за:
    - Сохранение списка словарей в JSON
    - Сохранение в CSV (с обработкой списков)
    - Автоматическое создание папки output/
"""

import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def save_json(data: List[Dict[str, Any]], site_name: str, output_dir: str = "output") -> Path:
    """
    Сохраняет данные в JSON-файл.

    Args:
        data: список словарей
        site_name: имя сайта (для имени файла)
        output_dir: папка для сохранения

    Returns:
        Path к сохранённому файлу
    """
    if not data:
        logger.warning("Нет данных для JSON")
        return Path()

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    filepath = output_path / f"{site_name}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"JSON сохранён: {filepath} ({len(data)} записей)")

    return filepath

def save_csv(data: List[Dict[str, Any]], site_name: str, output_dir: str = "output") -> Path:
    """
    Сохраняет данные в CSV-файл.

    Списки превращаются в строки через ", ".join(...).

    Args:
        data: список словарей
        site_name: имя сайта (для имени файла)
        output_dir: папка для сохранения

    Returns:
        Path к сохранённому файлу
    """
    if not data:
        logger.warning("Нет данных для CSV")
        return Path()

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    filepath = output_path / f"{site_name}.csv"

    fieldnames = list(data[0].keys())

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            clean_row = {}
            for key, value in row.items():
                if isinstance(value, list):
                    clean_row[key] = ", ".join(str(v) for v in value)
                else:
                    clean_row[key] = value
            writer.writerow(clean_row)

    logger.info(f"CSV сохранён: {filepath} ({len(data)} записей)")

    return filepath

def export_all(data: List[Dict[str, Any]], site_name: str, output_dir: str = "output") -> Dict[str, Path]:
    """
    Сохраняет данные и в JSON, и в CSV.

    Args:
        data: список словарей
        site_name: имя сайта
        output_dir: папка для сохранения

    Returns:
        Словарь {формат: путь к файлу}
    """
    json_path = save_json(data, site_name, output_dir)
    csv_path = save_csv(data, site_name, output_dir)

    return {
        "json": json_path,
        "csv": csv_path,
    }