import streamlit as st
import pandas as pd
import numpy as np

# ---------- CONFIG ----------
CONFIG = {
    "title": "PhonePe Transaction Intelligence",
    "amount_keyword": "amount",
    "footer": "MBA Data Portfolio",
}

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title=CONFIG["title"].replace(" ", ""), layout="wide")

# ---------- CSS ----------
st.markdown(
    """
<style>
.metric-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}
.summary-box {
    background: rgba(46, 125, 50, 0.1);
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #4caf50;
    margin: 1rem 0;
}
.insights-box {
    background: rgba(156, 39, 176, 0.1);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid #9c27b0;
    margin: 1rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HELPERS ----------
def indian_format(num):
    """Indian lakhs/crores: 347432194 → ₹34,74,32,194"""
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

# ---------- HEADER ----------
st.title(f"💳 {CONFIG['title']}")
st.markdown("**Interactive analytics dashboard for payment data**")

# ---------- SIDEBAR ----------
st.sidebar.header("📊 Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Detect amount column
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
        st.sidebar.success(f"✅ Using: **{amount_col}**")
    else:
        st.sidebar.error("No amount column detected.")

    # Metrics
    total_rev = df[amount_col].sum() if amount_col else 0
    avg_amt = df[amount_col].mean() if amount_col else 0
    max_amt = df[amount_col].max() if amount_col else 0

    # Sidebar summary (compact)
    st.sidebar.markdown(
        f"""
    <div class="summary-box">
        <b>{len(df):,}</b> txns | <b>{indian_format(total_rev)}</b> revenue
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ---------- KPI CARDS ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{len(df):,}</h2>
            <p>Total Transactions</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{indian_format(total_rev)}</h2>
            <p>Total Revenue</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{indian_format(avg_amt)}</h2>
            <p>Avg Transaction</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{indian_format(max_amt)}</h2>
            <p>Highest Amount</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ---------- MAIN LAYOUT ----------
    left, right = st.columns([2, 1])

    # Recent transactions: ALL columns
    with left:
        st.subheader("📋 Recent Transactions")
        st.dataframe(df.head(15), use_container_width=True, hide_index=True)

    # Insights + Quick Stats
    with right:
        st.subheader("📊 Key Insights")

        if amount_col and len(df) > 0:
            top_txn = df.nlargest(1, amount_col).iloc[0]
            st.markdown(
                f"""
            <div class="insights-box">
                <b>Revenue Summary</b><br>
                • Total: {indian_format(total_rev)}<br>
                • Top txn: {top_txn.get('Transaction_ID', 'N/A')} | {indian_format(top_txn[amount_col])}<br>
                • Avg txn: {indian_format(avg_amt)}
            </div>
            """,
                unsafe_allow_html=True,
            )

        with st.expander("📊 Quick Stats", expanded=False):
            if amount_col and len(df) > 0:
                st.markdown("**Key Insights:**")
                st.markdown(
                    f"• **Top txn:** {top_txn.get('Transaction_ID', 'N/A')} | {indian_format(top_txn[amount_col])}"
                )

                # status / success rate
                status_col = None
                for col in df.columns:
                    if any(word in col.lower() for word in ["status", "payment_status"]):
                        status_col = col
                        break

                if status_col:
                    status_values = df[status_col].astype(str).str.lower()
                    success_rate = status_values.str.contains(
                        "success|complete|paid|approved",
                        case=False,
                        na=False,
                    ).mean()
                    st.markdown(
                        f"• **Success rate:** {success_rate:.1%} ({status_col})"
                    )

                st.markdown(f"• **Records analyzed:** {len(df):,}")

                # Top service/category/product
                for col in ["Service", "Category", "Product"]:
                    if col in df.columns:
                        top_item = df[col].value_counts().index[0]
                        st.markdown(f"• **Top {col.lower()}:** {top_item}")
                        break

else:
    st.info("👆 **Upload your CSV** to get started!")
    st.markdown("### **Features**")
    st.markdown(
        """
- **Advanced business analytics**
- **Automated column validation**
- **Robust error recovery**
"""
    )

st.markdown("---")
st.markdown(f"*{CONFIG['footer']}*")



