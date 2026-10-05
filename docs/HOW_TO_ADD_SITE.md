# Как добавить новый сайт

## Главное

**Код менять не нужно.** Только YAML-конфиг.

Добавить новый сайт = **3 шага**:
1. Разведка HTML
2. Создание YAML
3. Тест

**Время:** 15-30 минут для простого сайта.

## Шаг 1: Разведка HTML

**Запусти инструмент разведки:**

```bash
python tools/explore.py https://новый-сайт.com/каталог/ --delay 2
```
**Важно:** `--delay` — пауза между запросами. Проверь `robots.txt` сайта:
```bash
curl https://новый-сайт.com/robots.txt
```
**Что покажет инструмент:**

1. **Общую картину** — какие теги есть на странице
    
2. **Возможные контейнеры** — отсортированы по размеру HTML

**🔍 Возможные контейнеры элементов:
```
============================================================

Селектор                                            Кол-во     Размер
----------------------------------------------------------------------
article.tm-articles-list__item                          20     158320
div.article-snippet                                     20     155234
div.meta-container                                      20      32451
div.meta                                                25       4210
```
**Пример:** `article.tm-articles-list__item` — 20 раз, размер 158320 → **это контейнер.**
## Шаг 2: Посмотреть детали

**Узнай структуру одного элемента:**
```bash
python tools/explore.py https://новый-сайт.com/каталог/ --tag article --limit 1 --delay 2
```
**Покажет HTML одного `<article>`.** Ищи в нём:

- **Заголовок** — обычно `<h2>`, `<a>`
    
- **Ссылка** — `href` атрибут
    
- **Автор/цена/дата** — другие теги с классами
    

**Для каждого поля запиши:**

- **Селектор** (например, `a.title-link`)
    
- **Тип** (`text` или `attribute`)
    
- **Атрибут** (если `type: attribute`)
    

## Шаг 3: Создать YAML

**Скопируй существующий конфиг как шаблон:**
```bash
cp sites/habr.yaml sites/новый-сайт.yaml
```
**Открой и заполни:**

```bash
nano sites/новый-сайт.yaml
```
**Пример для сайта с товарами:**
```yaml
name: новый-сайт
base_url: "https://новый-сайт.com/каталог/"
request_delay: 2.0

list_selector: "article.tm-articles-list__item"

fields:
  title:
    selector: "a.tm-title__link"
    type: text
  link:
    selector: "a.tm-title__link"
    type: attribute
    attribute: "href"
  price:
    selector: "span.price-value"
    type: text
  author:
    selector: "a.tm-user-info__username"
    type: text
```
**Что менять:**

- `name` — имя сайта (совпадает с именем файла)
    
- `base_url` — URL страницы со списком
    
- `request_delay` — пауза (из `robots.txt`)
    
- `list_selector` — селектор контейнера (из шага 1)
    
- `fields` — что извлекать
    

## Шаг 4: Тест
```bash
python main.py --site новый-сайт
```

**Ожидаемый вывод:**
```text
🌐 Загружаем: https://новый-сайт.com/каталог/
📥 Загружено: 250000 символов
✅ Извлечено записей: 20
💾 JSON сохранён: output/новый-сайт.json
💾 CSV сохранён: output/новый-сайт.csv
```

**Проверь файлы:**
```bash
head -20 output/новый-сайт.csv
```
## Troubleshooting

### Проблема: `Найдено элементов: 0`

**Причина:** `list_selector` не находит элементы.

**Что делать:**
1. Запусти `explore.py` снова
2. Проверь селектор в выводе
3. Открой HTML через `--tag article` — есть ли нужный тег?

### Проблема: поля пустые (`""`)

**Причина:** селектор поля неправильный.

**Что делать:**
1. Открой `explore.py --tag article --limit 1`
2. Найди нужный элемент в HTML
3. Проверь класс, тег, атрибут
4. Обнови селектор в YAML

### Проблема: `request_delay` слишком маленький

**Симптом:** сервер возвращает ошибку, сайт блокирует.

**Что делать:**
1. Проверь `robots.txt` — там указан `Crawl-delay`
2. Увеличь `request_delay` в YAML
3. Для крупных сайтов — **10 секунд** и больше

### Проблема: `403 Forbidden`

**Причина:** сайт блокирует парсинг.

**Что делать:**
1. Проверь `robots.txt` — если `Disallow: /`, парсить **нельзя**
2. Если разрешено — попробуй другой `User-Agent`
3. В сложных случаях — нужен Selenium или прокси (не в этом проекте)

### Проблема: `FileNotFoundError: sites/сайт.yaml`

**Причина:** не создан YAML или опечатка в имени.

**Что делать:**
1. Проверь `ls sites/`
2. Убедись, что имя файла совпадает с `--site`

## Пример: добавление нового сайта с нуля

**Задача:** спарсить цитаты с `quotes.toscrape.com`.

### Шаг 1: Разведка

```bash
python tools/explore.py http://quotes.toscrape.com/ --delay 1
```
**Возможные контейнеры:**
```text
div.quote                                10     523
```
**Выбор:** `div.quote` — 10 раз, повторяется, есть класс.
### Шаг 2: Детали
```bash
python tools/explore.py http://quotes.toscrape.com/ --tag div --limit 1
```
**Видим HTML:**
```html
<div class="quote">
  <span class="text">"Текст цитаты"</span>
  <small class="author">Albert Einstein</small>
  <div class="tags">
    <a class="tag">change</a>
    <a class="tag">thinking</a>
  </div>
</div>
```
***Что извлекаем:**

- `text` → `span.text` (тип `text`)
    
- `author` → `small.author` (тип `text`)
    
- `tags` → `a.tag` (тип `list`, но пока не поддерживаем)
    

### Шаг 3: YAML
```bash
cp sites/habr.yaml sites/quotes.yaml
nano sites/quotes.yaml
```
**Заполняем:**
```yaml
name: quotes
base_url: "http://quotes.toscrape.com/"
request_delay: 1.0

list_selector: "div.quote"

fields:
  text:
    selector: "span.text"
    type: text
  author:
    selector: "small.author"
    type: text
```
### Шаг 4: Тест
```bash
python main.py --site quotes
```
**Проверяем:**
```bash
cat output/quotes.csv
```
  
```csv

text,author
"Текст цитаты","Albert Einstein"
...
```
**Готово!** Новый сайт добавлен за 10 минут, код не тронут.
