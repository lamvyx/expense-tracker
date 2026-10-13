import sys
import argparse

from . import service
from .storage import load_expenses, save_expenses
from .utils import (current_month_str,
    format_money,
    format_summary,
    format_table,
    today_str,
    validate_date,
    validate_month,
)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='expense_tracker',
        description="Personal expense management"
    ) 
    sub = parser.add_subparsers(dest="command", required=True)
    #add
    p = sub.add_parser("add", help="Add expense")
    p.add_argument("--amount", type=int, required=True, help="Số tiền (VND)")
    p.add_argument("--category", required=True, help="Danh mục")
    p.add_argument("--note", default="", help="Ghi chú")
    p.add_argument("--date", default=None, help="YYYY-MM-DD (mặc định: hôm nay)")
    
    # list
    p = sub.add_parser("list", help="Liệt kê khoản chi")
    p.add_argument("--month", default=None, help="Lọc theo tháng YYYY-MM")
    p.add_argument("--category", default=None, help="Lọc theo danh mục")

    # update
    p = sub.add_parser("update", help="Sửa khoản chi")
    p.add_argument("id", type=int, help="ID khoản chi")
    p.add_argument("--amount", type=int)
    p.add_argument("--category")
    p.add_argument("--note")
    p.add_argument("--date", help="YYYY-MM-DD")

    # delete
    p = sub.add_parser("delete", help="Xóa khoản chi")
    p.add_argument("id", type=int, help="ID khoản chi")

    # summary
    p = sub.add_parser("summary", help="Thống kê theo tháng")
    p.add_argument("--month", default=None, help="YYYY-MM (mặc định: tháng này)")

    return parser

def run(args: argparse.Namespace) -> None:
    expenses = load_expenses()
    
    if args.command == "add":
        date = validate_date(args.date) if args.date else today_str()
        e = service.add_expense(expenses, date, args.amount, args.category, args.note)
        save_expenses(expenses)
        print(f"Đã thêm #{e.id}: {format_money(e.amount)} - {e.category} ({e.date})")
    
    elif args.command == "list":
        month = validate_month(args.month) if args.month else None
        items = service.list_expenses(expenses, month=month, category=args.category)
        print(format_table(items))

    elif args.command == "update":
        changes = {
            "amount": args.amount,
            "category": args.category,
            "note": args.note,
            "date": validate_date(args.date) if args.date else None,
        }
        if all(v is None for v in changes.values()):
            raise ValueError("Cần ít nhất một trường để sửa (--amount, --category, --note, --date)")
        e = service.update_expense(expenses, args.id, **changes)
        save_expenses(expenses)
        print(f"Đã cập nhật #{e.id}")

    elif args.command == "delete":
        e = service.delete_expense(expenses, args.id)
        save_expenses(expenses)
        print(f"Đã xóa #{e.id}: {e.category} {format_money(e.amount)}")

    elif args.command == "summary":
        month = validate_month(args.month) if args.month else current_month_str()
        print(format_summary(service.summary_by_month(expenses, month)))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        run(args)
    except ValueError as err:
        print(f"Lỗi: {err}", file=sys.stderr)
        return 1
    return 0