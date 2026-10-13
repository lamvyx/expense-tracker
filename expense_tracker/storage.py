from pathlib import Path
import json
from .models import Expense

# Đường dẫn tới file chứ data
DATA_FILE = Path(__file__).resolve().parent.parent/'data'/'expense.json'

def load_expenses(path: Path = DATA_FILE) -> list[Expense]:
    if not path.exists():
        return []
    text = path.read_text(encoding='utf-8').strip()
    if not text:
        return []
    # loads: đọc từ 1 chuỗi, load: đọc từ 1 file
    raw = json.loads(text)  
    return [Expense.from_dict(item) for item in raw]

def save_expenses(expenses: list[Expense], path: Path = DATA_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True) # Tạo thư mục data
    data = [e.to_dict() for e in expenses] # chuyển obj về dict
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )