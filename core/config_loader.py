"""
Загрузка и валидация конфигов сайтов.

Отвечает за:
    - Чтение YAML-файлов
    - Проверку обязательных полей
    - Понятные ошибки при проблемах
"""

import logging
from pathlib import Path
from typing import Dict, Any

import yaml

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["name", "base_url", "list_selector", "fields"]

def load_site_config(site_name: str, sites_dir: str = "sites") -> Dict[str, Any]:
    """
    Загружает конфиг сайта из YAML и валидирует обязательные поля.

    Args:
        site_name: имя сайта (без .yaml), например "habr"
        sites_dir: папка с конфигами

    Returns:
        Словарь с настройками сайта

    Raises:
        FileNotFoundError: если YAML не найден
        ValueError: если отсутствуют обязательные поля
    """
    config_path = Path(sites_dir) / f"{site_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Конфиг не найден: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError(f"Конфиг пустой: {config_path}")

    # Проверяем обязательные поля
    missing = [field for field in REQUIRED_FIELDS if field not in config]

    if missing:
        raise ValueError(
            f"В конфиге {config_path} отсутствуют поля: {', '.join(missing)}"
        )

    logger.info(f"Загружен конфиг: {config_path}")

    return config