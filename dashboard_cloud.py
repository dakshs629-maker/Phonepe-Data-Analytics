import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai
import google.ai.generativelanguage as glm

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
    padding: 1.2rem;
    border-radius: 10px;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Helper for currency formatting
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

# ---------- 3. SECURE KEY HANDLING ----------
api_key = st.secrets.get("GEMINI_API_KEY", "").strip()

# ---------- 4. DATA LOADING ----------
@st.cache_data
def load_default():
    return pd.read_csv("Phonepe Dataset.csv")

@st.cache_data
def load_uploaded(file):
    return pd.read_csv(file)

st.sidebar.header("📊 Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload PhonePe CSV", type="csv")
df = None
default_file = "Phonepe Dataset.csv"

if uploaded_file:
    df = load_uploaded(uploaded_file)
    st.sidebar.success("✅ Custom File Loaded")
elif os.path.exists(default_file):
    df = load_default()
    st.sidebar.info("📂 Using Repository Dataset")

# ---------- 5. MAIN UI ----------
st.title(f"💳 {CONFIG['title']}")

if df is not None:
    # --- DATA CLEANING ---
    amount_col = next((col for col in df.columns if CONFIG["amount_keyword"] in col.lower()), None)
    if amount_col:
        df[amount_col] = pd.to_numeric(df[amount_col].astype(str).str.replace("₹|Rs|,|\\s", "", regex=True), errors="coerce")
    
    total_rev = df[amount_col].sum() if amount_col else 0
    total_txns = len(df)

    # KPI Layout
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
            st.warning("⚠️ Please add your GEMINI_API_KEY in Streamlit Secrets to enable AI Analysis.")
        else:
            user_query = st.text_input("Ask a business question:", placeholder="e.g., list all services")
            if user_query:
                try:
                    # Force stable v1 API endpoint
                    import google.generativeai as genai
                    genai.configure(
                        api_key=api_key,
                        client_options={"api_endpoint": "generativelanguage.googleapis.com"}
                    )
                    model = genai.GenerativeModel('models/gemini-1.5-flash')

                    # PRO MBA CONTEXT: Explicitly inject unique services list to prevent category skipping
                    all_services = df['Service'].unique().tolist() if 'Service' in df.columns else []
                    context = {
                        "Revenue": indian_format(total_rev),
                        "Volume": total_txns,
                        "Unique_Services_List": all_services
                    }

                    # SYSTEM INSTRUCTION: Forcing business analyst behavior
                    prompt = (
                        f"Act as a Senior FinTech Analyst. Answer using this context: {context}. "
                        f"Question: {user_query}. "
                        "Rule: If asked to list services, you MUST list every single category in Unique_Services_List, "
                        "especially low-volume ones like Insurance."
                    )

                    with st.spinner("AI Analyst is thinking..."):
                        response = model.generate_content(prompt)
                        st.markdown(f'<div class="ask-box"><b>AI Analyst:</b><br>{response.text}</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"⚠️ Debug Error: {str(e)}")

        with st.expander("📊 Quick Stats", expanded=True):
            if amount_col:
                top_row = df.nlargest(1, amount_col).iloc[0]
                txn_id = top_row.get('Transaction_ID', 'N/A')
                st.markdown(f"• **Top txn:** {txn_id} | {indian_format(top_row[amount_col])}")

                status_col = next((col for col in df.columns if any(w in col.lower() for w in ['status', 'payment'])), None)
                if status_col:
                    rate = df[status_col].astype(str).str.contains('success|complete|paid', case=False).mean()
                    st.markdown(f"• **Success rate:** {rate:.1%} ({status_col})")

                st.markdown(f"• **Records analyzed:** {total_txns:,}")

else:
    st.info("👋 Welcome! Please upload your dataset to begin.")

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>{CONFIG['footer']}</p>", unsafe_allow_html=True)
