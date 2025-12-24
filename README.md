# 💰 Expense Tracker with AI Insights

An intelligent expense tracking application built with FastAPI backend and Streamlit frontend. Automatically categorizes expenses, provides AI-driven insights, and helps you manage your budget efficiently.

## Features

✨ **Core Features:**
- ➕ Add individual expenses with automatic AI-based categorization
- 📤 Bulk upload expenses via CSV or Excel files
- 📅 View expenses filtered by month
- 🗑️ Delete expenses with multi-select functionality
- 📊 Visual analytics with pie charts for category-wise spending
- 🤖 AI-powered monthly insights and budget alerts
- 💸 Monthly budget tracking and spending analysis

## Tech Stack

**Backend:**
- FastAPI - Modern web framework
- SQLAlchemy - ORM for database operations
- SQLite - Lightweight database
- OpenAI API - AI categorization and insights

**Frontend:**
- Streamlit - Interactive web interface
- Pandas - Data manipulation
- Matplotlib - Data visualization

## Project Structure

```
Expense-AI-Tracker/
├── backend/
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # Database configuration
│   └── ai_utils.py          # AI integration functions
├── frontend/
│   └── app.py               # Streamlit application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Expense-AI-Tracker
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_key_here
```

## Running the Application

### Start Backend (FastAPI):
```powershell
cd backend
uvicorn main:app --reload
```
Backend runs on: `http://localhost:8000`

### Start Frontend (Streamlit):
Open a new terminal in the `frontend` directory:
```powershell
streamlit run app.py
```
Frontend runs on: `http://localhost:8501`

## API Endpoints

**Base URL:** `http://localhost:8000`

### Add Single Expense
```
POST /expenses
{
  "title": "Grocery Shopping",
  "amount": 500.0,
  "date": "2025-12-24"
}
```

### Get All Expenses (with optional month filter)
```
GET /expenses
GET /expenses?month=2025-12
```

### Bulk Upload Expenses
```
POST /expenses/upload
- Upload CSV or Excel file with columns: title, amount, date
```

### Delete Expenses
```
DELETE /expenses
{
  "ids": [1, 2, 3]
}
```

### Get AI Insights
```
GET /insights?budget=10000&month=2025-12
```

## Database

SQLite database file: `expense_tracker.db`

**Table: expensetracker**
- id (Integer, Primary Key)
- title (String)
- amount (Float)
- category (String)
- date (String)

## Features in Detail

### 🤖 AI Categorization
Expenses are automatically categorized using OpenAI API based on the expense title.

### 📊 Monthly Insights
Get AI-generated summaries of:
- Total spending by category
- Budget utilization
- Spending patterns and trends

### 💡 Budget Alerts
Automatic warnings when spending exceeds your monthly budget.

## Requirements

See `requirements.txt`:
- fastapi
- uvicorn
- sqlalchemy
- streamlit
- requests
- openai
- pandas
- matplotlib
- python-multipart
- openpyxl
- python-dotenv

## Usage Tips

1. Set a monthly budget in the Streamlit app
2. Add expenses individually or upload a bulk file
3. View expenses filtered by month
4. Check AI insights for spending patterns
5. Use checkboxes to delete multiple expenses at once

## Notes

- Ensure backend is running before starting Streamlit
- Database file is created automatically on first run
- AI features require a valid OpenAI API key

## License

MIT
