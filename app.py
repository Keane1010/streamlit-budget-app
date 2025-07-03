import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(page_title="Bi‑Weekly Budget App", layout="wide")

st.title("🧾 Budget Manager with OCR")
st.markdown("Upload bank statement **images** to extract transactions and track expenses (bi‑weekly view coming soon 📊).")

uploaded_file = st.file_uploader("Upload a bank statement image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Bank Statement", use_column_width=True)
    with st.spinner("🔍 Extracting text with OCR..."):
        extracted_text = pytesseract.image_to_string(image)
    st.subheader("📝 Extracted Text")
    st.text(extracted_text)
    st.info("🔧 Auto-categorization, credit‑card & account tracking, and bi‑weekly graphs coming soon!")

st.markdown("---")
st.markdown("👨‍👩‍👧 This app will eventually support income tracking, credit‑card balances (Marriott, AMEX, TD), and bi‑weekly summaries.")
