import streamlit as st
from PIL import Image
import easyocr
import pandas as pd
import numpy as np
import io
import datetime
import re

st.set_page_config(page_title="📊 Budget Manager", layout="wide")

st.title("📊 Bi-Weekly Budget App with OCR, CSV & Graphs")
st.markdown("Upload your **bank statement image or CSV**, extract transactions, and track expenses automatically.")

# Helper: Extract transactions from raw text
def parse_transactions(text):
    lines = text.split('\n')
    transactions = []
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s+(.+?)\s+(-?\d+\.\d{2})')
    for line in lines:
        match = pattern.search(line)
        if match:
            date, description, amount = match.groups()
            category = auto_categorize(description)
            transactions.append({
                "Date": date,
                "Description": description.strip(),
                "Amount": float(amount),
                "Category": category
            })
    return pd.DataFrame(transactions)

# Helper: Auto-categorize transactions based on keywords
def auto_categorize(description):
    desc = description.lower()
    if any(word in desc for word in ["enmax", "mortgage", "rent", "telus", "rogers"]):
        return "Home"
    elif any(word in desc for word in ["hyundai", "fuel", "insurance"]):
        return "Car"
    elif any(word in desc for word in ["netflix", "apple", "disney", "youtube", "spotify", "lingokids", "ipsy"]):
        return "Subscriptions"
    elif "brightpath" in desc or "gym" in desc:
        return "House"
    elif any(word in desc for word in ["unicef", "charity", "cancer", "trust"]):
        return "Charity"
    elif "investment" in desc:
        return "Investment"
    else:
        return "Other"

# Upload section
uploaded_file = st.file_uploader("📤 Upload bank statement (image or CSV)", type=["png", "jpg", "jpeg", "csv"])
df = pd.DataFrame()

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        if "Date" in df.columns and "Description" in df.columns and "Amount" in df.columns:
            st.success("✅ CSV uploaded successfully!")
            if "Category" not in df.columns:
                df["Category"] = df["Description"].apply(auto_categorize)
        else:
            st.error("❌ CSV must include Date, Description, and Amount columns.")
            df = pd.DataFrame()
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Bank Statement", use_column_width=True)

        with st.spinner("🔍 Extracting text with OCR..."):
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext(np.array(image), detail=0)
            extracted_text = "\n".join(result)

        df = parse_transactions(extracted_text)

# Process and display if data is available
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    st.subheader("📋 Transactions")
    df["Period"] = df["Date"].apply(lambda d: f"{d.year}-W{int(d.strftime('%U'))//2 + 1}")
    selected_period = st.selectbox("🗓 Select Bi-Weekly Period", sorted(df["Period"].unique(), reverse=True))
    filtered_df = df[df["Period"] == selected_period]

    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, file_name="transactions.csv", mime="text/csv")

    st.subheader("📊 Spending by Category")
    pie_data = filtered_df.groupby("Category")["Amount"].sum()
    st.plotly_chart({
        "data": [{
            "labels": pie_data.index,
            "values": pie_data.values,
            "type": "pie"
        }],
        "layout": {"title": "Category Breakdown"}
    })

    st.subheader("📈 Spending Over Time")
    bar_data = filtered_df.groupby("Date")["Amount"].sum()
    st.bar_chart(bar_data)
else:
    st.info("📌 Upload an image or CSV file to begin.")
