import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def categorize_expense(title: str) -> str:
    reponse = client.chat.completions.create(
        model="gpt-4o-mini",
         messages=[
            {
                "role": "system",
                "content": (
                    "You are an expense categorization system.\n"
                    "Allowed categories: Food, Travel, Shopping, Bills, Entertainment, Other.\n"
                    "Rules:\n"
                    "- Respond with ONLY ONE WORD\n"
                    "- No explanation\n"
                    "- No punctuation\n"
                    "- If unsure, respond Other"
                )
            },
            {"role": "user", "content": title}
        ]
    )

    category = reponse.choices[0].message.content.strip()
    return category.split()[0]  # Return only the first word


def generate_monthly_insights(expenses):
    if not expenses:
        return "No expenses recorded yet."

    text = "\n".join(
        [f"{e.title} - {e.amount} - {e.category}" for e in expenses]
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You analyze monthly expenses and give insights"
            },
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()


def budget_alert(expenses, budget: float) -> str:
    total = sum(e.amount for e in expenses)

    if total <= budget:
        return f"✅ You are within budget. Total spent: ₹{total}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a financial advisor"
            },
            {
                "role": "user",
                "content": (
                    f"My monthly budget is ₹{budget}. "
                    f"I have spent ₹{total}. "
                    "Give a warning and suggestions."
                )
            }
        ]
    )
    return response.choices[0].message.content.strip()