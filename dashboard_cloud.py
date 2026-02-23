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

# Helper for currency formatting
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

# ---------- 3. SECURE KEY HANDLING ----------
# Priority 1: Check Streamlit Cloud Secrets. Priority 2: Sidebar Manual Input.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.header("🔑 AI Configuration")
    api_key = st.sidebar.text_input("Enter Gemini API Key (Manual)", type="password")

# ---------- 4. DATA LOADING ----------
st.sidebar.header("📊 Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload new PhonePe CSV", type="csv")

df = None
default_file = "Phonepe Dataset.csv"

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Custom File Loaded")
elif os.path.exists(default_file):
    df = pd.read_csv(default_file)
    st.sidebar.info("📂 Using Repository Dataset")
else:
    st.sidebar.warning("⚠️ No dataset found. Please upload a CSV.")

# ---------- 5. MAIN UI ----------
st.title(f"💳 {CONFIG['title']}")

if df is not None:
    # --- DATA CLEANING ---
    amount_col = next((col for col in df.columns if CONFIG["amount_keyword"] in col.lower()), None)
    if amount_col:
        df[amount_col] = df[amount_col].astype(str).str.replace("₹|Rs|,|\\s", "", regex=True)
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    
    total_rev = df[amount_col].sum() if amount_col else 0
    total_txns = len(df)

    # KPI Cards
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
            st.warning("Please provide a Gemini API Key to enable AI analysis.")
        else:
            user_query = st.text_input("Ask a business question:", placeholder="e.g., List all service categories")
            if user_query:
                try:
                    genai.configure(api_key=api_key)
                    # FIX: Explicit model path to resolve 404 errors
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    
                    # Robust context to ensure all services (like Insurance) are visible
                    all_services = df['Service'].unique().tolist() if 'Service' in df.columns else []
                    context = {
                        "Total Revenue": indian_format(total_rev),
                        "Volume": total_txns,
                        "Unique_Services": all_services
                    }
                    
                    prompt = (
                        f"Role: MBA FinTech Analyst. Answer using this context: {context}. "
                        f"Question: {user_query}. "
                        "Note: Ensure you include all low-volume services like Insurance if asked to list categories."
                    )
                    
                    with st.spinner("Analyzing data..."):
                        response = model.generate_content(prompt)
                        st.markdown(f'<div class="ask-box"><b>AI Analyst:</b><br>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI Connection Error: {e}")

        # --- MATCHED QUICK STATS BOX ---
        with st.expander("📊 Quick Stats", expanded=True):
            st.markdown("**Key Insights:**")
            if amount_col:
                # Top Transaction Row
                top_row = df.nlargest(1, amount_col).iloc[0]
                txn_id = top_row.get('Transaction_ID', 'N/A')
                st.markdown(f"• **Top txn:** {txn_id} | {indian_format(top_row[amount_col])}")
                
                # Dynamic Success Rate
                status_col = next((col for col in df.columns if any(w in col.lower() for w in ['status', 'payment'])), None)
                if status_col:
                    rate = df[status_col].astype(str).str.contains('success|complete|paid', case=False).mean()
                    st.markdown(f"• **Success rate:** {rate:.1%} ({status_col})")
                
                st.markdown(f"• **Records analyzed:** {total_txns:,}")
                
                # Top Service Type
                if 'Service' in df.columns:
                    top_service = df['Service'].value_counts().index[0]
                    st.markdown(f"• **Top service:** {top_service}")

else:
    st.info("👋 Welcome! Please upload your dataset in the sidebar to begin analysis.")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>{CONFIG['footer']}</p>", unsafe_allow_html=True)