class Expense:
    def __init__(self, id:int, date:str, amount:int, category:str, note:str=""):
        self.id = id
        self.date = date
        self.amount = amount
        self.category = category
        self.note = note
        
    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "note": self.note
        }
    
    @classmethod
    # dict to class
    def from_dict(cls, data:dict) -> "Expense":
        return cls(
            id=data["id"],
            date=data["date"],
            amount=data["amount"],
            category=data['category'],
            note=data.get("note","")
        )
        
    def __str__(self):
        return (
        f"Expense(id={self.id}, date={self.date}, "
        f"amount={self.amount}, category={self.category}, "
        f"note={self.note})"
    )
        
    def __eq__(self, other):
        if not isinstance(other, Expense): # kiểm tra object có thuộc 1 cls
            return NotImplemented
        return self.to_dict() == other.to_dict()