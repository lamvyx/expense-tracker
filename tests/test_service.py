import pytest

from expense_tracker.service import (
    add_expense,
    delete_expense,
    list_expenses,
    summary_by_month,
    update_expense,
)


def test_add_assigns_incremental_ids():
    data = []
    a = add_expense(data, "2026-10-01", 50000, "an-uong")
    b = add_expense(data, "2026-10-02", 30000, "di-chuyen")
    assert (a.id, b.id) == (1, 2)


def test_id_not_reused_after_delete():
    data = []
    add_expense(data, "2026-10-01", 1000, "a")
    add_expense(data, "2026-10-02", 2000, "a")
    add_expense(data, "2026-10-03", 3000, "a")
    delete_expense(data, 2)
    new = add_expense(data, "2026-10-04", 4000, "a")
    assert new.id == 4


def test_add_rejects_non_positive_amount():
    with pytest.raises(ValueError):
        add_expense([], "2026-10-01", 0, "an-uong")


def test_list_filter_by_month():
    data = []
    add_expense(data, "2026-09-30", 1000, "a")
    add_expense(data, "2026-10-01", 2000, "a")
    result = list_expenses(data, month="2026-10")
    assert [e.amount for e in result] == [2000]


def test_update_only_given_fields():
    data = []
    e = add_expense(data, "2026-10-01", 1000, "an-uong", "cũ")
    update_expense(data, e.id, amount=5000, note=None)
    assert e.amount == 5000
    assert e.note == "cũ"          # None => giữ nguyên


def test_delete_missing_id_raises():
    with pytest.raises(ValueError):
        delete_expense([], 99)


def test_summary_by_month():
    data = []
    add_expense(data, "2026-10-01", 50000, "an-uong")
    add_expense(data, "2026-10-05", 30000, "an-uong")
    add_expense(data, "2026-10-06", 20000, "di-chuyen")
    add_expense(data, "2026-09-30", 99999, "khac")   # khác tháng, bị loại
    s = summary_by_month(data, "2026-10")
    assert s["total"] == 100000
    assert s["count"] == 3
    assert s["by_category"] == {"an-uong": 80000, "di-chuyen": 20000}