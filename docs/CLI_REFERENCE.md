# CLI Reference — справочник команд

## `main.py` — парсер

### Базовое использование

```bash
python main.py --site ИМЯ_САЙТА
```
### Примеры

**Один сайт:**

```bash
python main.py --site habr
```
**Несколько сайтов:**

```bash
python main.py --sites habr,quotes
```
**Все сайты:**

```bash
python main.py --all
```
## `tools/explore.py` — разведка HTML
### Базовое использование
```bash
python tools/explore.py URL
```
### Примеры

**Общая разведка:**

```bash
python tools/explore.py https://habr.com/ru/articles/ --delay 10
```
**Детали тега:**

```bash
python tools/explore.py https://habr.com/ru/articles/ --tag article --limit 1 --delay 10
```
## Частые команды

### Добавить новый сайт

```bash
# 1. Разведка
python tools/explore.py https://новый-сайт.com/ --delay 5
# 2. Создать YAML
cp sites/habr.yaml sites/новый-сайт.yaml
nano sites/новый-сайт.yaml
# 3. Тест
python main.py --site новый-сайт
```
### Перезапустить парсер
```bash
python main.py --site habr
```
### Посмотреть логи

```bash
# Последние 20 строк
tail -20 parser.log
# Всё
cat parser.log
# Поиск ошибок
grep ERROR parser.log
```
## Коды возврата

**`main.py`** возвращает 0 при успехе. При ошибке — логирует и продолжает.

|Итог|Что значит|
|---|---|
|`1/1 сайтов обработано`|Успех|
|`0/1 сайтов обработано`|Ошибка (см. лог)|
|`2/3 сайтов обработано`|Частичный успех|
