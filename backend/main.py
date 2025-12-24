from fastapi import FastAPI, UploadFile, File
import pandas as pd
from database import engine, SessionLocal
from models import Base, Expense
from schemas import ExpenseCreate, DeleteExpense
from ai_utils import (
    categorize_expense,
    generate_monthly_insights,
    budget_alert
)

app = FastAPI(title="Expense Tracker with AI")

Base.metadata.create_all(bind=engine)

# ------------------ ADD SINGLE EXPENSE ------------------
@app.post("/expenses")
def add_expense(expense: ExpenseCreate):
    db = SessionLocal()
    category = categorize_expense(expense.title)

    db.add(
        Expense(
            title=expense.title,
            amount=expense.amount,
            category=category,
            date=expense.date
        )
    )
    db.commit()
    return {"message": "Expense added"}


# ------------------ BULK UPLOAD (CSV / EXCEL) ------------------
@app.post("/expenses/upload")
def upload_expenses(file: UploadFile = File(...)):
    db = SessionLocal()

    # Read file
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file.file)
    else:
        return {"error": "Only CSV or Excel files allowed"}

    # Normalize columns
    df.columns = df.columns.str.lower()

    required_cols = {"title", "amount", "date"}
    if not required_cols.issubset(df.columns):
        return {"error": "File must contain title, amount, date columns"}

    for _, row in df.iterrows():
        category = categorize_expense(str(row["title"]))

        db.add(
            Expense(
                title=str(row["title"]),
                amount=float(row["amount"]),
                category=category,
                date=str(row["date"])
            )
        )

    db.commit()
    return {"message": f"{len(df)} expenses uploaded successfully"}


# ------------------ GET EXPENSES (MONTH-WISE) ------------------
@app.get("/expenses")
def get_expenses(month: str | None = None):
    db = SessionLocal()
    query = db.query(Expense)

    if month:
        query = query.filter(Expense.date.startswith(month))

    return query.all()


# ------------------ DELETE EXPENSES ------------------
@app.delete("/expenses")
def delete_expenses(data: DeleteExpense):
    db = SessionLocal()
    db.query(Expense).filter(
        Expense.id.in_(data.ids)
    ).delete(synchronize_session=False)
    db.commit()
    return {"message": "Expenses deleted"}


# ------------------ AI INSIGHTS ------------------
@app.get("/insights")
def insights(budget: float, month: str):
    db = SessionLocal()
    expenses = db.query(Expense).filter(
        Expense.date.startswith(month)
    ).all()

    return {
        "summary": generate_monthly_insights(expenses),
        "budget_alert": budget_alert(expenses, budget)
    }
