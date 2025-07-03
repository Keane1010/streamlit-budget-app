# Bi‑Weekly Budget Web App

A simple Streamlit app to upload bank statements, extract transaction text with OCR, and build toward a bi‑weekly budgeting tool.

## Features

- Upload scanned bank statement images
- Perform OCR using easyocr (compatible with Streamlit Cloud)
- Display extracted text
- Future: categorize, graph, and track credit cards and accounts

## Deployment

Deploy on [Streamlit Cloud](https://streamlit.io/cloud):

1. Push this repo to GitHub
2. Go to https://share.streamlit.io/deploy
3. Enter:
   - Repository: your-username/streamlit-budget-app
   - Branch: main
   - Main file path: app.py
4. Click Deploy
