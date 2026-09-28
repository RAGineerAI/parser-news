import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config_loader import load_site_config

config = load_site_config("habr")
print(f"Сайт: {config['name']}")
print(f"URL: {config['base_url']}")
print(f"Задержка: {config['request_delay']}")
print(f"Полей: {len(config['fields'])}")
for field_name in config["fields"]:
    print(f"  - {field_name}")