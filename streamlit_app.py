import os
import streamlit as st

# API key ko environment variable se uthaein
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY set nahi hai!")
else:
    # Yahan apna genai wala code likhiyeimport streamlit as st
import pandas as pd

# Safe library import with fallback
try:
    import google.generativeai as genai
    LIB_LOADED = True
except ImportError:
    LIB_LOADED = False

st.set_page_config(page_title="Data Studio", layout="wide")

if not LIB_LOADED:
    st.error("Library load nahi ho paayi. Kripya requirements.txt check karein.")
    st.stop()

st.title("📊 Enterprise AI Insights Studio")

# API Key check
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets mein GEMINI_API_KEY set nahi hai.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# File Uploader
uploaded_file = st.file_uploader("CSV ya Excel file upload karein", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.write("Data Preview:", df.head())
    
    user_query = st.text_input("Data ke baare mein kuch puchein:")
    if user_query:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Data: {df.head().to_string()}\n\nQuestion: {user_query}")
        st.write("AI Answer:", response.text)
