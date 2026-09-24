# 🕷️ Parser Basic

[![Status](https://img.shields.io/badge/status-MVP_completed-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

Простой парсер HTML-страниц на Python (requests + BeautifulSoup).

**Проект 2.6 — шаблон для быстрой адаптации под задачи парсинга **
## 🎯 Что решает

Собирает данные с HTML-страниц и сохраняет в **JSON** и **CSV**.

Подходит для:
- Парсинга новостей, статей, каталогов
- Сбора цен, отзывов, объявлений
- Любых статичных сайтов (без JS)

## 🛠️ Стек

| Компонент | Технология |
|-----------|------------|
| **HTTP-запросы** | requests |
| **Парсинг HTML** | BeautifulSoup + lxml |
| **Сохранение** | JSON, CSV |
| **Язык** | Python 3.12 |

## 🚀 Быстрый старт

### Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/RAGineerAI/parser-basic.git
cd parser-basic

# 2. Создать окружение
python3 -m venv venv
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить парсер
python parser.py
```

---
## 📁 Структура проекта

parser-basic/  
├── parser.py # Основная логика парсера  
├── config.py # Настройки (URL, задержки)  
├── requirements.txt # Зависимости  
└── output/ # Результаты (JSON, CSV)


## 🎯 Как адаптировать под новую задачу

Парсер легко переделать под любой сайт. Нужно изменить **3 вещи**:


## 🎯 Как адаптировать под новую задачу

Парсер легко переделать под любой сайт. Нужно изменить **3 вещи**:

### 1. URL сайта

В `config.py`:
```python
BASE_URL = "https://нужный-сайт.com/"
```
### 2. Селекторы (что искать)

В `parser.py` → `parse_page()`:

# Было:
```bash
quote_elements = soup.find_all("div", class_="quote")
# Стало (пример):
quote_elements = soup.find_all("article", class_="post")
```
### 3. Поля (что извлекать)

В `parser.py` → `parse_quote()`:
```bash
return {
    "title": ...,
    "price": ...,
    "description": ...,
}
```
## 🔧 Что внутри

- ✅ Вежливые паузы между запросами
    
- ✅ User-Agent (притворяется браузером)
    
- ✅ Обработка ошибок HTTP
    
- ✅ Сохранение в JSON и CSV
    

## 👤 Автор

**RAGineerAI** — [GitHub](https://github.com/RAGineerAI)

## 📄 Лицензия

MIT