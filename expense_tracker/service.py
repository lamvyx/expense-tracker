from collections import defaultdict
from .models import Expense

# Tự động tạo id mới dựa trên id lớn nhất hiện tại.
def _next_id(expense: list[Expense]) -> int:
    return max((e.id for e in expense), default=0)+1

def add_expense(expenses: list[Expense], 
                date:str, 
                amount:int, category:str, note:str="") -> Expense:
    if amount <= 0:
        raise ValueError("Amount should be larger than 0")
    expense = Expense(_next_id(expenses), date, amount, category, note)
    expenses.append(expense)
    return expense

# Lọc danh sách chi tiêu theo tháng, theo danh mục
def list_expenses(expenses: list[Expense], 
                  month:str | None=None, 
                  category:str | None=None,) -> list[Expense]:
    result = expenses
    if month:
        result = (e for e in result if e.date.startswith(month))
    if category:
        result = (e for e in result if e.category==category)
    # sorted : sắp xếp result, key=lambda chỉ định tiêu chí sắp xếp và tạo 1 một hàm nhỏ 
    # để lấy khóa sắp xếp. Ưu tiên ngày xong tới id e.date, e.id
    return sorted(result, key=lambda e: (e.date, e.id))

def _find(expenses: list[Expense], expense_id: int) -> Expense:
    for e in expenses:
        if e.id == expense_id:
            return e
    raise ValueError(f'Can not found expense with id={expense_id}')

# **change la cac thuoc tinh con lai o trong expense
def update_expense(expenses: list[Expense], expense_id: int, **changes) -> Expense:
    expense = _find(expenses, expense_id)
    if "amount" in changes and changes["amount"] is not None and changes["amount"] <= 0:
        raise ValueError("Amount should be larger than 0.")
    for field, value in changes.items():
        if value is not None:
            setattr(expense,field,value) # like expense.field = value
    return expense

def delete_expense(expenses: list[Expense], expense_id:int) -> Expense:
    expense = _find(expenses, expense_id)
    expenses.remove(expense)
    return expense

def summary_by_month(expenses: list[Expense], month:str) -> dict:
    # Loc khoang chi theo thang
    items = list_expenses(expenses, month=month)
    # Tao dict de cong tien theo danh muc
    by_category = defaultdict(int) # tu tao gia tri mac dinh = 0
    for e in items:
        by_category[e.category] += e.amount 
    return {
        "month" : month,
        "count" : len(items),
        "total" : sum(e.amount for e in items),
        "by_category" : dict(by_category)
    }