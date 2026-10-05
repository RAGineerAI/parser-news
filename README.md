# 🕷️ Parser News

[![Status](https://img.shields.io/badge/status-MVP_completed-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

Многосайтовый парсер на Python. Собирает данные с HTML-страниц и сохраняет в JSON + CSV.

**Ключевая идея:** код — движок, конфиг — задача. Для нового сайта не нужно менять код — только YAML.

## 🎯 Что умеет

- ✅ Парсинг HTML-страниц (статьи, товары, цитаты, каталоги)
- ✅ Работа через YAML-конфиги (новый сайт за 15 минут)
- ✅ Выгрузка в JSON и CSV
- ✅ Разведка HTML (`tools/explore.py`)
- ✅ Логирование (консоль + файл)

## 🚀 Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/RAGineerAI/parser-news.git
cd parser-news

# 2. Окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Запустить парсер
python main.py --site habr
```
**Результат:** `output/habr.json` и `output/habr.csv`
## 📊 Пример

**Команда:**

```bash
python main.py --site habr
```
**Вывод:**

```text
🌐 Загружаем: https://habr.com/ru/articles/
📥 Загружено: 250000 символов
✅ Извлечено записей: 20
💾 JSON сохранён: output/habr.json
💾 CSV сохранён: output/habr.csv
✅ Итог: 1/1 сайтов обработано
```
**Файл `output/habr.csv`:**

```csv
title,link,author,counter,datetime
"Теория возможностей...","/ru/articles/1087094/","Ir1na","1.7K","2026-09-27T10:24:13.000Z"
...
```
## 🏗️ Архитектура

```text

main.py → process_site() → fetcher → extractor → exporter
                              ↓         ↓          ↓
                           HTML     данные    JSON+CSV
```
**Подробно:** [docs/ARCHITECTURE.md](https://docs/ARCHITECTURE.md)
## 📁 Структура проекта

```text
parser-news/
├── main.py                  # CLI, оркестратор
├── core/                    # Движок
│   ├── fetcher.py           # Загрузка HTML
│   ├── config_loader.py     # Чтение YAML
│   ├── extractor.py         # Извлечение данных
│   └── exporter.py          # JSON + CSV
├── sites/                   # Конфиги сайтов
│   └── habr.yaml
├── tools/
│   └── explore.py           # Разведка HTML
├── tests/                   # Тесты
├── docs/                    # Документация
└── output/                  # Результаты
```
## 📖 Документация

|Документ|Что внутри|
|---|---|
|[ARCHITECTURE.md](https://docs/ARCHITECTURE.md)|Как устроен проект|
|[HOW_TO_ADD_SITE.md](https://docs/HOW_TO_ADD_SITE.md)|Как добавить новый сайт|
|[CLI_REFERENCE.md](https://docs/CLI_REFERENCE.md)|Справочник команд|

## 🔧 Как добавить новый сайт

**3 шага:**
```bash

# 1. Разведка
python tools/explore.py https://новый-сайт.com/ --delay 5
# 2. Создать YAML
cp sites/habr.yaml sites/новый-сайт.yaml
nano sites/новый-сайт.yaml
# 3. Тест
python main.py --site новый-сайт
```
**Код не трогаем.**
## 🛠️ Стек

| Компонент    | Технология           |
| ------------ | -------------------- |
| Язык         | Python 3.12          |
| HTTP         | requests             |
| Парсинг HTML | BeautifulSoup + lxml |
| Конфиги      | PyYAML               |
| CLI          | argparse             |
| Логирование  | logging              |
| Данные       | json, csv            |
## 👤 Автор

**RAGineerAI** — [GitHub](https://github.com/RAGineerAI)

## 📄 Лицензия

MIT