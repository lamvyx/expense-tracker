import pytest

from expense_tracker.models import Expense
from expense_tracker.utils import (
    format_money,
    format_summary,
    format_table,
    validate_date,
    validate_month,
)


def test_validate_date_ok():
    assert validate_date("2026-10-12") == "2026-10-12"


@pytest.mark.parametrize("bad", ["12/10/2026", "2026-02-30", "abc", ""])
def test_validate_date_bad(bad):
    with pytest.raises(ValueError):
        validate_date(bad)


def test_validate_month():
    assert validate_month("2026-10") == "2026-10"
    with pytest.raises(ValueError):
        validate_month("2026-13")


def test_format_money():
    assert format_money(50000) == "50,000VND"
    assert format_money(1234567) == "1,234,567VND"


def test_format_table_empty():
    assert format_table([]) == "Không có khoản chi nào."


def test_format_table_has_rows():
    out = format_table([Expense(1, "2026-10-12", 50000, "an-uong", "Cơm trưa")])
    assert "50,000VND" in out
    assert "Cơm trưa" in out


def test_format_summary():
    out = format_summary(
        {"month": "2026-10", "count": 2, "total": 80000,
         "by_category": {"an-uong": 50000, "di-chuyen": 30000}}
    )
    assert "80,000VND" in out
    assert out.index("an-uong") < out.index("di-chuyen")  # giảm dần