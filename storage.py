from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from data_model import SchoolData
from seed_data import build_school_data

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
SCHOOL_JSON = DATA_DIR / 'school.json'


def save_school(data: SchoolData, path: Optional[Path] = None) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    target = path or SCHOOL_JSON
    target.write_text(
        json.dumps(data.to_dict(), ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    return target


def load_school(path: Optional[Path] = None) -> SchoolData:
    target = path or SCHOOL_JSON
    if target.exists():
        raw = json.loads(target.read_text(encoding='utf-8'))
        return SchoolData.from_dict(raw)
    data = build_school_data()
    save_school(data, target)
    return data


def reset_to_seed() -> SchoolData:
    data = build_school_data()
    save_school(data)
    return data
