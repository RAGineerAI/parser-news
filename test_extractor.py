from core.fetcher import fetch_page
from core.config_loader import load_site_config
from core.extractor import extract_all

# 1. Загружаем конфиг сайта
config = load_site_config("habr")
print(f"🔧 Конфиг загружен: {config['name']}")
print(f"⏱️  Задержка: {config['request_delay']} сек")

# 2. Загружаем HTML
html = fetch_page(
    config["base_url"],
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    delay=config["request_delay"]
)
print(f"📥 HTML загружен: {len(html)} символов")

# 3. Извлекаем данные
results = extract_all(
    html,
    list_selector=config["list_selector"],
    fields_config=config["fields"]
)

print(f"✅ Извлечено статей: {len(results)}")

# 4. Показываем первые 3
print("\n📊 Первые 3 статьи:")
for i, article in enumerate(results[:3], start=1):
    print(f"\n  {i}.")
    for field, value in article.items():
        print(f"     {field}: {value}")