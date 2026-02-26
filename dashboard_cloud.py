import streamlit as st
import pandas as pd
import numpy as np
import os
import requests

# ---------- 1. PAGE CONFIG ----------
st.set_page_config(
    page_title="PhonePe Transaction Intelligence",
    page_icon="💳",
    layout="wide"
)

CONFIG = {
    "title": "PhonePe Transaction Intelligence",
    "amount_keyword": "amount",
    "footer": "Daksh Sharma · Data Analytics Portfolio",
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
    padding: 1.2rem;
    border-radius: 10px;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def indian_format(num):
    try:
        num = float(num)
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
    except: return str(num)

# Using gemini-2.5-flash — best free tier availability on AI Studio
def call_gemini(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 429:
            return "⚠️ Rate limit reached — please wait a moment and try again."
        if r.status_code == 400:
            return "⚠️ Invalid request — check your API key in Streamlit Secrets."
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

api_key = st.secrets.get("GEMINI_API_KEY", "").strip()

@st.cache_data
def load_data():
    return pd.read_csv("Phonepe.csv")

st.sidebar.header("📊 Data Controls")
st.sidebar.file_uploader("🔒 Dataset Pre-Loaded — No Upload Needed", type="csv", disabled=True, help="This dashboard runs on a fixed dataset. Upload is disabled.")

df = None
try:
    df = load_data()
    st.sidebar.info("📂 Dataset Loaded")
except Exception as e:
    st.sidebar.error(f"❌ Could not load dataset: {e}")

st.title(f"💳 {CONFIG['title']}")

if df is not None:
    amount_col = next((col for col in df.columns if CONFIG["amount_keyword"] in col.lower()), None)
    if amount_col:
        df[amount_col] = pd.to_numeric(df[amount_col].astype(str).str.replace("₹|Rs|,|\\s", "", regex=True), errors="coerce")

    total_rev = df[amount_col].sum() if amount_col else 0
    total_txns = len(df)

    # Dashboard Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><h2>{total_txns:,}</h2><p>Total Transactions</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><h2>{indian_format(total_rev)}</h2><p>Total Revenue</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><h2>{indian_format(df[amount_col].mean() if amount_col else 0)}</h2><p>Avg Ticket Size</p></div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("📋 Transaction Data")
        st.dataframe(df.head(15), use_container_width=True, hide_index=True)

    with right:
        st.subheader("🤖 Smart AI Analysis")
        if not api_key:
            st.warning("⚠️ Please add your GEMINI_API_KEY in Streamlit Secrets.")
        else:
            user_query = st.text_input("Ask a business question:", placeholder="e.g., which service has highest failure rate?")
            if user_query:
                try:
                    # --- Rich context build ---
                    service_summary = df.groupby('Service').agg(
                        Total_Revenue=(amount_col, 'sum'),
                        Avg_Transaction=(amount_col, 'mean'),
                        Volume=('Transaction_ID', 'count'),
                        Success_Rate=('Payment_Status', lambda x: round((x == 'Successful').mean() * 100, 2)),
                        Failure_Rate=('Payment_Status', lambda x: round((x != 'Successful').mean() * 100, 2))
                    ).round(2).to_dict()

                    failure_reasons = df[df['Payment_Status'] != 'Successful']['Reason'].value_counts().head(10).to_dict() if 'Reason' in df.columns else {}

                    monthly_revenue = df.groupby(df['Date'].str[:7] if 'Date' in df.columns else df.index // 1000)[amount_col].sum().round(2).to_dict() if 'Date' in df.columns else {}

                    service_type_revenue = df.groupby('Service Type')[amount_col].sum().sort_values(ascending=False).head(10).round(2).to_dict() if 'Service Type' in df.columns else {}

                    context = {
                        "Overall": {
                            "Total_Transactions": total_txns,
                            "Total_Revenue": indian_format(total_rev),
                            "Avg_Ticket_Size": indian_format(df[amount_col].mean()),
                            "Overall_Success_Rate": f"{(df['Payment_Status'] == 'Successful').mean() * 100:.2f}%"
                        },
                        "By_Service": service_summary,
                        "Top_Failure_Reasons": failure_reasons,
                        "Monthly_Revenue_Trend": monthly_revenue,
                        "Top_Service_Types_by_Revenue": service_type_revenue
                    }

                    prompt = (
                        f"You are a Senior FinTech Analyst. Answer the question using ONLY the data provided. "
                        f"Be specific with numbers. Do not say you lack information — all data needed is in the context.\n\n"
                        f"DATA CONTEXT:\n{context}\n\n"
                        f"QUESTION: {user_query}\n\n"
                        f"ANSWER:"
                    )
                    with st.spinner("AI Analyst is thinking..."):
                        result = call_gemini(api_key, prompt)
                        st.markdown(f'<div class="ask-box"><b>AI Analyst:</b><br>{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

        with st.expander("📊 Quick Stats", expanded=True):
            if amount_col:
                top_row = df.nlargest(1, amount_col).iloc[0]
                txn_id = top_row.get('Transaction_ID', 'N/A')
                st.markdown("**Key Insights:**")
                st.markdown(f"• **Top txn:** {txn_id} | {indian_format(top_row[amount_col])}")

                status_col = next((col for col in df.columns if any(word in col.lower() for word in ['status', 'payment_status'])), None)
                if status_col:
                    rate = df[status_col].astype(str).str.contains('success|complete|paid|approved', case=False, na=False).mean()
                    st.markdown(f"• **Success rate:** {rate:.1%} ({status_col})")

                st.markdown(f"• **Records analyzed:** {total_txns:,}")

                for col in ['Service', 'Category', 'Product']:
                    if col in df.columns:
                        top_item = df[col].value_counts().index[0]
                        st.markdown(f"• **Top {col.lower()}:** {top_item}")
                        break
else:
    st.info("👋 System is ready. Ensure 'Phonepe.csv' is uploaded to your GitHub repository.")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>{CONFIG['footer']}</p>", unsafe_allow_html=True)

