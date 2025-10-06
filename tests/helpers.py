import json
import os.path as path
from typing import Any


def load_json_data(file_path: str) -> dict[str, Any]:
    with open(path.join(path.dirname(__file__), file_path), "r") as file:
        data = json.load(file)
    return data
