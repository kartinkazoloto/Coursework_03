import os
from pathlib import Path
import json


def save_json(data, file_name) -> list:
    """Сохранение инфо в файл JSON"""
    save_dir = Path(__file__).parent.parent / "data"
    save_dir.mkdir(parents=True, exist_ok=True)
    # file_name = "data.json"
    path_file = save_dir / file_name
    try:
        with open(path_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные успешно сохранены в {file_name}")
        return data
    except IOError as e:
        print(f"Ошибка при записи в файл {file_name}: {e}")