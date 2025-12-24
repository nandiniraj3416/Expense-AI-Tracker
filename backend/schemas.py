from pydantic import BaseModel
from typing import List

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    date: str

class DeleteExpense(BaseModel):
    ids: List[int]