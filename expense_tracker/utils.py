from datetime import date, datetime

from .models import Expense

def validate_date(value: str) -> str:
    try:
        # Kiem tra dinh dang tra ve YYYY-mm-dd
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Date '{value}' is invalid, need YYYY-MM-DD")
    return value

def validate_month(value: str) -> str:
    """Kiểm tra định dạng YYYY-MM."""
    try:
        datetime.strptime(value, "%Y-%m")
    except ValueError:
        raise ValueError(f"Tháng '{value}' không hợp lệ, cần dạng YYYY-MM")
    return value

def today_str() -> str:
    return date.today().isoformat()

def current_month_str() -> str:
    return date.today().strftime("%Y-%m")
        
def format_money(amount: int) -> str:
    return f"{amount:,}VND"

def format_table(expenses: list[Expense]) -> str:
    """Trả về bảng text căn cột. Danh sách rỗng thì báo không có dữ liệu."""
    if not expenses:
        return "Không có khoản chi nào."

    headers = ["ID", "Ngày", "Số tiền", "Danh mục", "Ghi chú"]
    rows = [
        [str(e.id), e.date, format_money(e.amount), e.category, e.note]
        for e in expenses
    ]

    # độ rộng mỗi cột = chuỗi dài nhất trong cột đó (kể cả tiêu đề)
    widths = [max(len(r[i]) for r in [headers] + rows) for i in range(len(headers))]

    def line(cells):
        return " | ".join(c.ljust(w) for c, w in zip(cells, widths))

    sep = "-+-".join("-" * w for w in widths)
    return "\n".join([line(headers), sep] + [line(r) for r in rows])


def format_summary(summary: dict) -> str:
    """Định dạng kết quả của summary_by_month."""
    lines = [
        f"Thống kê tháng {summary['month']}",
        f"Số khoản chi : {summary['count']}",
        f"Tổng chi     : {format_money(summary['total'])}",
    ]
    if summary["by_category"]:
        lines.append("Theo danh mục:")
        # sắp xếp giảm dần theo số tiền
        for cat, total in sorted(
            summary["by_category"].items(), key=lambda x: x[1], reverse=True
        ):
            lines.append(f"  - {cat}: {format_money(total)}")
    return "\n".join(lines)