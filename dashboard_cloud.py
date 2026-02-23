import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai

# ---------- 1. PAGE CONFIG ----------
st.set_page_config(
    page_title="PhonePe Transaction Intelligence",
    page_icon="💳",
    layout="wide"
)

# ---------- 2. CONFIG & STYLING ----------
CONFIG = {
    "title": "PhonePe Transaction Intelligence",
    "amount_keyword": "amount",
    "footer": "MBA Data Portfolio",
}

st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
.ask-box {
    background: rgba(102, 126, 234, 0.05);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Helper for currency
def indian_format(num):
    try:
        num = float(num)
    except: return str(num)
    neg = num < 0
    num = abs(int(round(num)))
    s = str(num)
    if len(s) <= 3: result = s
    else:
        last3 = s[-3:]; rest = s[:-3]; parts = []
        while len(rest) > 2:
            parts.append(rest[-2:]); rest = rest[:-2]
        if rest: parts.append(rest)
        parts.reverse()
        result = ",".join(parts) + "," + last3
    return f"{'-' if neg else ''}₹{result}"

# ---------- 3. SIDEBAR (API KEY & UPLOAD) ----------
st.sidebar.header("🔑 AI Configuration")
# Recruiters can put their own key, or you can set it in Streamlit Secrets
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.header("📊 Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload PhonePe CSV", type="csv")

df = None
default_file = "Phonepe Dataset.csv"

if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif os.path.exists(default_file):
    df = pd.read_csv(default_file)

# ---------- 4. MAIN UI ----------
st.title(f"💳 {CONFIG['title']}")

if df is not None:
    amount_col = next((col for col in df.columns if CONFIG["amount_keyword"] in col.lower()), None)
    if amount_col:
        df[amount_col] = df[amount_col].astype(str).str.replace("₹|Rs|,|\\s", "", regex=True)
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    
    total_rev = df[amount_col].sum() if amount_col else 0
    total_txns = len(df)

    # KPI Cards
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><h2>{total_txns:,}</h2><p>Transactions</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><h2>{indian_format(total_rev)}</h2><p>Total Revenue</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><h2>{indian_format(df[amount_col].mean() if amount_col else 0)}</h2><p>Avg Ticket Size</p></div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("📋 Transaction Data")
        st.dataframe(df.head(15), use_container_width=True)

    with right:
        st.subheader("🤖 Gemini AI Analysis")
        if not api_key:
            st.warning("Please enter a Gemini API Key in the sidebar to use the AI features.")
        else:
            user_query = st.text_input("Ask a question about this data:")
            if user_query:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Creating a rich context for Gemini
                    context = {
                        "Total Revenue": indian_format(total_rev),
                        "Volume": total_txns,
                        "Services": df['Service'].unique().tolist() if 'Service' in df.columns else "N/A",
                    }
                    
                    prompt = f"As a FinTech Analyst, answer this based on the data context: {context}. Question: {user_query}"
                    
                    response = model.generate_content(prompt)
                    st.markdown(f'<div class="ask-box"><b>Gemini:</b><br>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI Error: {e}")

        with st.expander("📊 Quick Stats", expanded=True):
            if amount_col:
                st.markdown(f"• **Peak Transaction:** {indian_format(df[amount_col].max())}")
                status_col = next((col for col in df.columns if 'status' in col.lower()), None)
                if status_col:
                    rate = df[status_col].astype(str).str.contains('success|paid', case=False).mean()
                    st.markdown(f"• **Success Rate:** {rate:.1%}")

else:
    st.info("Upload a CSV to begin.")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>{CONFIG['footer']}</p>", unsafe_allow_html=True)