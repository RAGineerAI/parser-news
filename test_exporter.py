from core.exporter import export_all

data = [
    {"title": "Статья 1", "tags": ["python", "ai"]},
    {"title": "Статья 2", "tags": ["rag"]},
]

paths = export_all(data, "test")
print(f"JSON: {paths['json']}")
print(f"CSV: {paths['csv']}")