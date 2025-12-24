import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Expense Tracker AI", layout="wide")
st.title("💰 Expense Tracker with AI Insights")

# =====================================================
# MONTH SELECTION (Calendar Picker)
# =====================================================
st.header("📅 Select Month")
selected_date = st.date_input("Select Month", value=date.today())
selected_month = selected_date.strftime("%Y-%m")  # YYYY-MM format for API
st.markdown(f"**Selected month:** {selected_date.strftime('%B %Y')}")

# =====================================================
# BUDGET INPUT
# =====================================================
st.header("💸 Monthly Budget")
budget = st.number_input(
    "Enter your monthly budget (₹)",
    min_value=0.0,
    value=10000.0,
    step=500.0
)

# =====================================================
# ADD EXPENSE
# =====================================================
st.header("➕ Add Expense")
title = st.text_input("Expense Title")
amount = st.number_input("Amount (₹)", min_value=0.0)
expense_date = st.date_input("Date", value=date.today(), key="add_expense_date")

if st.button("Add Expense"):
    if title and amount > 0:
        try:
            requests.post(
                f"{API_URL}/expenses",
                json={
                    "title": title,
                    "amount": amount,
                    "date": str(expense_date)
                }
            )
            st.success("Expense added successfully")
            st.rerun()
        except requests.exceptions.ConnectionError:
            st.error("Backend server not running")
    else:
        st.error("Please enter valid expense details")

# =====================================================
# UPLOAD CSV / EXCEL
# =====================================================
st.header("📤 Upload Expenses (CSV / Excel)")
uploaded_file = st.file_uploader(
    "Upload file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    if st.button("Upload Expenses"):
        files = {"file": uploaded_file}
        try:
            response = requests.post(
                f"{API_URL}/expenses/upload",
                files=files
            )

            if response.status_code == 200:
                st.success(response.json()["message"])
                st.rerun()
            else:
                st.error("Upload failed")
        except requests.exceptions.ConnectionError:
            st.error("Backend server not running")

# =====================================================
# VIEW EXPENSES (TABLE WITH CHECKBOX)
# =====================================================
st.header("📄 Expenses")

try:
    response = requests.get(
        f"{API_URL}/expenses",
        params={"month": selected_month}
    )
    expenses = response.json()
except requests.exceptions.ConnectionError:
    st.error("Backend server not running")
    st.stop()

delete_ids = []

if expenses:
    df = pd.DataFrame(expenses)

    # -------- TABLE HEADER --------
    h1, h2, h3, h4, h5 = st.columns([0.6, 2.5, 1.2, 1.5, 1.5])
    h1.markdown("**Delete**")
    h2.markdown("**Title**")
    h3.markdown("**Amount (₹)**")
    h4.markdown("**Category**")
    h5.markdown("**Date**")

    st.divider()

    # -------- TABLE ROWS --------
    for _, row in df.iterrows():
        c1, c2, c3, c4, c5 = st.columns([0.6, 2.5, 1.2, 1.5, 1.5])

        with c1:
            if st.checkbox("", key=f"del_{row['id']}"):
                delete_ids.append(row["id"])

        with c2:
            st.write(row["title"])

        with c3:
            st.write(f"₹{row['amount']}")

        with c4:
            st.write(row["category"])

        with c5:
            st.write(row["date"])

    # -------- DELETE BUTTON --------
    if delete_ids:
        if st.button("🗑️ Delete Selected Expenses"):
            try:
                requests.delete(
                    f"{API_URL}/expenses",
                    json={"ids": delete_ids}
                )
                st.success("Selected expenses deleted")
                st.rerun()
            except requests.exceptions.ConnectionError:
                st.error("Backend server not running")

    # =====================================================
    # PIE CHART
    # =====================================================
    st.subheader("🥧 Category-wise Spending")
    category_sum = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(
        category_sum,
        labels=category_sum.index,
        autopct="%1.1f%%"
    )
    ax.set_title("Expense Distribution")
    st.pyplot(fig)

else:
    st.info("No expenses found for this month")

# =====================================================
# AI INSIGHTS
# =====================================================
st.header("🤖 AI Insights")

if st.button("Get Monthly Insights"):
    try:
        response = requests.get(
            f"{API_URL}/insights",
            params={
                "budget": budget,
                "month": selected_month
            }
        ).json()

        st.subheader("📊 Monthly Summary")
        st.write(response["summary"])

        st.subheader("🚨 Budget Alert")
        st.warning(response["budget_alert"])
    except requests.exceptions.ConnectionError:
        st.error("Backend server not running")
