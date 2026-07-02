import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px
import io

# Page configuration - Premium Analytics Theme
st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling Matrix (Premium Dark Interface Setup)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #58a6ff 0%, #f2ea79 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .metric-card {
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        padding: 1.6rem;
        border-radius: 14px;
        border: 1px solid #30363d;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 10px 30px rgba(88, 166, 255, 0.15);
        transform: translateY(-3px);
    }
    .summary-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }
    div[data-testid="stChatInputContainer"], div[data-testid="stTextInput"] > div {
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stChatInputContainer"]:focus-within, div[data-testid="stTextInput"] > div:focus-within {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 1px #58a6ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔒 SECURE BACKEND CREDENTIALS MANAGEMENT
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    elif "google_api_key" in st.secrets: 
        API_KEY = st.secrets["google_api_key"]
    else:
        st.error("🔒 Configuration Error: Please ensure 'GEMINI_API_KEY' is active in Render or Streamlit Secrets.")
        st.stop()

genai.configure(api_key=API_KEY)

# 🛠️ MULTI-STRING AUTOMATED BACKEND INITIALIZATION (2026 Models Setup)
model = None
model_names_to_try = ['gemini-2.5-flash', 'models/gemini-2.5-flash', 'gemini-1.5-flash', 'models/gemini-1.5-flash']

for name in model_names_to_try:
    try:
        model = genai.GenerativeModel(name)
        model.generate_content("Ping")
        break
    except Exception:
        continue

if model is None:
    st.error("🚨 API Engine Resolution Failed. Check your Gemini API Key parameters inside Google AI Studio.")
    st.stop()

# Helper function to get clean report bytes for download
def get_report_bytes(text_content):
    clean_text = text_content.replace("**", "").replace("### ", "").replace("## ", "")
    return io.BytesIO(clean_text.encode('utf-8'))

# Clean Sidebar Dashboard Control
with st.sidebar:
    st.markdown("<h2 style='color:#fff; font-size: 1.6rem;'>⚙️ Control Center</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Engine Infrastructure")
    st.success("Super-Intelligence Matrix: Active")
    st.markdown("---")
    st.markdown("💡 **Tip:** Hover on charts to filter, isolate, or view exact metrics interactively!")

# App Header
st.markdown('<h1 class="main-title">📊 AI Data Analyst Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem;">An advanced enterprise data intelligence studio featuring interactive charts and automated reporting.</p>', unsafe_allow_html=True)

st.markdown('<div class="section-header">📂 Ingest Spreadsheet Matrix</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        df.columns = df.columns.str.strip()
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        sales_col = next((c for c in df.columns if 'sales' in c.lower() or 'amount' in c.lower() or 'price' in c.lower()), None)
        profit_col = next((c for c in df.columns if 'profit' in c.lower() or 'gain' in c.lower()), None)
        product_col = next((c for c in df.columns if 'product' in c.lower() or 'category' in c.lower() or 'item' in c.lower()), None)
        
        # --- ⚡ NEW: QUICK AUTOMATED DATA BLUEPRINT SUMMARY ---
        st.markdown('<div class="section-header">🔍 Live Data Asset Blueprint</div>', unsafe_allow_html=True)
        sum_col1, sum_col2, sum_col3 = st.columns(3)
        
        with sum_col1:
            st.markdown('<div class="summary-box">', unsafe_allow_html=True)
            st.markdown("#### 📑 Matrix Features")
            st.markdown(f"*- Quantitative/Numeric Columns:* `{len(numeric_cols)}`")
            st.markdown(f"*- Categorical/Text Columns:* `{len(text_cols)}`")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with sum_col2:
            st.markdown('<div class="summary-box">', unsafe_allow_html=True)
            st.markdown("#### 🩺 Integrity Health")
            total_nulls = df.isnull().sum().sum()
            if total_nulls == 0:
                st.markdown("*- Missing/Null Cells:* `None (Perfect Cleansed state)`")
            else:
                st.markdown(f"*- Missing/Null Cells:* `{total_nulls} blank fields detected`")
            st.markdown(f"*- Detected Target Column:* `{sales_col if sales_col else (numeric_cols[0] if numeric_cols else 'None')}`")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with sum_col3:
            st.markdown('<div class="summary-box">', unsafe_allow_html=True)
            st.markdown("#### ⏱️ Dimension Boundaries")
            st.markdown(f"*- Total Structural Cells:* `{df.size:,}`")
            if len(df) > 0:
                st.markdown(f"*- Head/Tail Range:* `1 to {len(df):,}`")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # --- EXEC EXECUTIVE KPI GRID ---
        st.markdown('<div class="section-header">📋 Core Performance Indicators</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">TOTAL RECORDS</p><h2 style="margin:0.4rem 0 0 0;color:#58a6ff;font-size:1.8rem;">{df.shape[0]:,}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">DIMENSIONALITY</p><h2 style="margin:0.4rem 0 0 0;color:#58a6ff;font-size:1.8rem;">{df.shape[1]} Columns</h2></div>', unsafe_allow_html=True)
        
        with col3:
            if sales_col:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">GROSS VOLUME</p><h2 style="margin:0.4rem 0 0 0;color:#34d399;font-size:1.6rem;">₹{df[sales_col].sum():,.2f}</h2></div>', unsafe_allow_html=True)
            elif len(numeric_cols) > 0:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">AGGREGATE ({numeric_cols[0]})</p><h2 style="margin:0.4rem 0 0 0;color:#34d399;font-size:1.6rem;">{df[numeric_cols[0]].sum():,}</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">GROSS VOLUME</p><h2 style="margin:0.4rem 0 0 0;color:#8b949e;font-size:1.6rem;">N/A</h2></div>', unsafe_allow_html=True)
                
        with col4:
            if profit_col:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">OPERATIONAL PROFIT</p><h2 style="margin:0.4rem 0 0 0;color:#ff7b72;font-size:1.6rem;">₹{df[profit_col].sum():,.2f}</h2></div>', unsafe_allow_html=True)
            elif product_col and not df[product_col].empty:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">DOMINANT CLASS</p><h2 style="margin:0.4rem 0 0 0;color:#ff7b72;font-size
