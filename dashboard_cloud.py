import streamlit as st
import pandas as pd
import numpy as np
import os

# ---------- 1. PAGE CONFIG (MUST BE FIRST) ----------
# This prevents the "oven" from getting stuck or crashing during startup
st.set_page_config(
    page_title="PhonePe Transaction Intelligence",
    page_icon="💳",
    layout="wide"
)

# ---------- 2. CONFIG & STYLING ----------
CONFIG = {
    "title": "PhonePe Transaction Intelligence",
    "amount_keyword": "amount",
    "footer": "MBA Data Portfolio | B.A. (Hons) Economics Graduate",
}

st.markdown(
    """
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
.summary-box {
    background: rgba(46, 125, 50, 0.1);
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #4caf50;
    margin: 1rem 0;
}
.insights-box {
    background: rgba(30, 136, 229, 0.1);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid #1e88e5;
    margin: 1rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- 3. HELPERS ----------
def indian_format(num):
    """Formats numbers to Indian Rupee standard (Lakhs/Crores)"""
    try:
        num = float(num)
    except (TypeError, ValueError):
        return str(num)

    neg = num < 0
    num = abs(int(round(num)))
    s = str(num)
    
    if len(s) <= 3:
        result = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.append(rest)
        parts.reverse()
        result = ",".join(parts) + "," + last3

    return f"{'-' if neg else ''}₹{result}"

# ---------- 4. DATA LOADING LOGIC ----------
st.sidebar.header("📊 Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload new PhonePe CSV", type="csv")

# This section ensures the dashboard isn't empty on first load
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Custom File Loaded")
else:
    # Attempt to load the dataset already in your GitHub repo
    default_file = "Phonepe Dataset.csv"
    if os.path.exists(default_file):
        df = pd.read_csv(default_file)
        st.sidebar.info("📂 Using Repository Dataset")
    else:
        st.sidebar.warning("⚠️ No dataset found. Please upload a CSV.")

# ---------- 5. DASHBOARD MAIN UI ----------
st.title(f"💳 {CONFIG['title']}")
st.markdown("**FinTech Analytics Dashboard | Transaction Pattern Analysis**")

if df is not None:
    # --- DATA CLEANING ---
    # Detect and clean the amount column
    amount_col = None
    for col in df.columns:
        if CONFIG["amount_keyword"] in col.lower():
            amount_col = col
            break

    if amount_col:
        df[amount_col] = (
            df[amount_col]
            .astype(str)
            .str.replace("₹|Rs|,|\\s", "", regex=True)
        )
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    
    # Calculate Core Metrics
    total_rev = df[amount_col].sum() if amount_col else 0
    avg_amt = df[amount_col].mean() if amount_col else 0
    max_amt = df[amount_col].max() if amount_col else 0
    total_txns = len(df)

    # --- KPI CARDS ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><h2>{total_txns:,}</h2><p>Transactions</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h2>{indian_format(total_rev)}</h2><p>Total Revenue</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><h2>{indian_format(avg_amt)}</h2><p>Avg Ticket Size</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><h2>{indian_format(max_amt)}</h2><p>Peak Transaction</p></div>', unsafe_allow_html=True)

    # --- VISUALIZATION SECTION ---
    st.markdown("---")
    left, right = st.columns([2, 1])

    with left:
        st.subheader("📋 Raw Transaction Log (Latest)")
        st.dataframe(df.head(15), use_container_width=True, hide_index=True)

    with right:
        st.subheader("📊 Strategic Summary")
        if amount_col and total_txns > 0:
            top_txn = df.nlargest(1, amount_col).iloc[0]
            st.markdown(
                f"""
                <div class="insights-box">
                    <b>Transaction Deep-Dive</b><br>
                    • <b>Scale:</b> {indian_format(total_rev)} analyzed<br>
                    • <b>High Value:</b> {indian_format(top_txn[amount_col])} (ID: {top_txn.get('Transaction_ID', 'N/A')})<br>
                    • <b>Stability:</b> {indian_format(avg_amt)} average txn value
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with st.expander("🔍 Categorical Distribution"):
            for col in ["Service", "Category", "Product", "Payment_Mode"]:
                if col in df.columns:
                    st.write(f"**Top {col}:** {df[col].value_counts().index[0]}")

else:
    st.info("👋 Welcome! Please upload your dataset in the sidebar to begin analysis.")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>{CONFIG['footer']}</p>", unsafe_allow_html=True)




