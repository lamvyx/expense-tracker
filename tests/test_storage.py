from expense_tracker.models import Expense
from expense_tracker.storage import load_expenses, save_expenses


def test_load_returns_empty_when_file_missing(tmp_path):
    assert load_expenses(tmp_path / "none.json") == []


def test_save_then_load(tmp_path):
    file = tmp_path / "expenses.json"
    data = [
        Expense(1, "2026-10-12", 50000, "an-uong", "Cơm trưa"),
        Expense(2, "2026-10-13", 30000, "di-chuyen"),
    ]
    save_expenses(data, file)
    assert load_expenses(file) == data