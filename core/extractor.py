"""
Извлечение данных из HTML по селекторам из конфига.

Отвечает за:
    - Применение селекторов к HTML-элементам
    - Извлечение текста или атрибутов
    - Обработку отсутствующих полей
"""

import logging
from typing import Dict, Any, List

from bs4 import BeautifulSoup
from bs4.element import Tag

logger = logging.getLogger(__name__)

def extract_field(element: Tag, field_name: str, field_config: Dict[str, Any]) -> str:
    """
    Извлекает одно поле из HTML-элемента по конфигу.

    Args:
        element: HTML-элемент (например, <article>)
        field_name: имя поля (для логов)
        field_config: конфиг поля из YAML

    Returns:
        Извлечённое значение (строка) или "" если не найдено
    """
    selector = field_config.get("selector")
    field_type = field_config.get("type", "text")

    found = element.select_one(selector)

    if found is None:
        logger.warning(f"Поле '{field_name}' не найдено по селектору '{selector}'")
        return ""

    if field_type == "text":
        return found.text.strip()

    if field_type == "attribute":
        attribute_name = field_config.get("attribute")
        if not attribute_name:
            logger.warning(f"Поле '{field_name}': type=attribute, но attribute не указан")
            return ""
        value = found.get(attribute_name)
        return value.strip() if value else ""

    logger.warning(f"Поле '{field_name}': неизвестный type '{field_type}'")
    return ""

def extract_fields(element: Tag, fields_config: Dict[str, Any]) -> Dict[str, str]:
    """
    Извлекает все поля из одного HTML-элемента.

    Args:
        element: HTML-элемент (например, <article>)
        fields_config: словарь полей из YAML

    Returns:
        Словарь {имя_поля: значение}
    """
    result = {}

    for field_name, field_config in fields_config.items():
        value = extract_field(element, field_name, field_config)
        result[field_name] = value

    return result

def extract_all(html: str, list_selector: str, fields_config: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Извлекает данные из всех элементов списка на странице.

    Args:
        html: HTML-код страницы
        list_selector: CSS-селектор для поиска элементов списка
        fields_config: словарь полей из YAML

    Returns:
        Список словарей с данными
    """
    soup = BeautifulSoup(html, "lxml")

    elements = soup.select(list_selector)
    logger.info(f"Найдено элементов: {len(elements)}")

    if not elements:
        logger.warning(f"Селектор '{list_selector}' ничего не нашёл")
        return []

    results = []
    for element in elements:
        data = extract_fields(element, fields_config)
        results.append(data)

    return results