import streamlit as st
import pandas as pd
import numpy as np
import ollama

# CONFIG - Change these 5 lines for new projects
CONFIG = {
    "title": "PhonePe Transaction Intelligence",      
    "amount_keyword": "amount",                       
    "ai_context": "Business analyst for PhonePe. Focus on revenue, top customers, growth.",  
    "footer": "MBA Data Portfolio"                    
}

# Proper Indian Rupee formatting (₹34,74,32,194)
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

# Professional CSS
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}
.ask-box {
    background: rgba(79, 172, 254, 0.1);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid #1f77b4;
    margin: 1rem 0;
}
.summary-box {
    background: rgba(46, 125, 50, 0.1);
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #4caf50;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title=CONFIG["title"].replace(" ", ""), layout="wide")
st.title(f"💳 {CONFIG['title']}")
st.markdown("**Interactive analytics dashboard for payment data**")

# Sidebar
st.sidebar.header("📊 Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Smart amount column detection using CONFIG
    amount_col = None
    for col in df.columns:
        if CONFIG["amount_keyword"] in col.lower():
            amount_col = col
            break

    if amount_col:
        df[amount_col] = df[amount_col].astype(str).str.replace('₹|Rs|,|\\s', '', regex=True)
        df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
        st.sidebar.success(f"✅ Using: **{amount_col}**")

    # Business metrics
    total_rev = df[amount_col].sum() if amount_col else 0
    avg_amt = df[amount_col].mean() if amount_col else 0
    max_amt = df[amount_col].max() if amount_col else 0

    # Compact sidebar summary (no duplication)
    st.sidebar.markdown(f"""
    <div class="summary-box">
        <b>{len(df):,}</b> txns | <b>{indian_format(total_rev)}</b> revenue
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards (main attraction)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{len(df):,}</h2>
            <p>Total Transactions</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{indian_format(total_rev)}</h2>
            <p>Total Revenue</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{indian_format(avg_amt)}</h2>
            <p>Avg Transaction</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='font-size: 2rem'>{indian_format(max_amt)}</h2>
            <p>Highest Amount</p>
        </div>
        """, unsafe_allow_html=True)

    # Main layout - AUTO SHOW ALL COLUMNS
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 Recent Transactions")
        st.dataframe(df.head(15), use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🤖 Smart AI")

        question = st.text_input(
            "💬 Ask about your data:",
            placeholder="top service type? biggest spender?",
            label_visibility="collapsed"
        )

        if question and amount_col:
            top_spenders = df.nlargest(3, amount_col)[['Transaction_ID', amount_col, 'Service']].to_dict('records')

            service_counts = {}
            service_type_counts = {}
            if 'Service' in df.columns:
                service_counts = df['Service'].value_counts().head(3).to_dict()
            if 'Service Type' in df.columns:
                service_type_counts = df['Service Type'].value_counts().head(3).to_dict()

            context = f"""BUSINESS DATA:
Total: {len(df):,} transactions, {indian_format(total_rev)} revenue
TOP 3 SPENDERS: {top_spenders}
Services: {service_counts}
Service Types: {service_type_counts}"""

            try:
                response = ollama.chat(
                    model='llama3.2:1b',
                    messages=[
                        {
                            'role': 'system',
                            'content': CONFIG["ai_context"]
                        },
                        {
                            'role': 'user',
                            'content': f"Data: {context}\n\nQuestion: {question}\n\nBusiness insight:"
                        }
                    ]
                )
                st.markdown(f"""
                <div class="ask-box">
                    <b>🤖 AI:</b> {response['message']['content']}
                </div>
                """, unsafe_allow_html=True)
            except Exception:
                st.markdown(f"""
                <div class="ask-box">
                    <b>💡 Quick Facts:</b><br>
                    • Revenue: {indian_format(total_rev)}<br>
                    • Top spenders shown above
                </div>
                """, unsafe_allow_html=True)

        # FIXED QUICK STATS: Smart success detection + more insights
        with st.expander("📊 Quick Stats", expanded=False):
            if amount_col:
                top_txn = df.nlargest(1, amount_col).iloc[0]
                st.markdown("**Key Insights:**")
                st.markdown(f"• **Top txn:** {top_txn.get('Transaction_ID', 'N/A')} | {indian_format(top_txn[amount_col])}")
                
                # SMART success rate detection (works with 'successful', 'SUCCESS', 'paid', etc.)
                status_col = None
                for col in df.columns:
                    if any(word in col.lower() for word in ['status', 'payment_status']):
                        status_col = col
                        break
                
                if status_col:
                    status_values = df[status_col].astype(str).str.lower()
                    success_rate = status_values.str.contains('success|complete|paid|approved', case=False, na=False).mean()
                    st.markdown(f"• **Success rate:** {success_rate:.1%} ({status_col})")
                
                st.markdown(f"• **Records analyzed:** {len(df):,}")
                
                # Top service/category/product
                for col in ['Service', 'Category', 'Product']:
                    if col in df.columns:
                        top_item = df[col].value_counts().index[0]
                        st.markdown(f"• **Top {col.lower()}:** {top_item}")
                        break

else:
    st.info("👆 **Upload your CSV** to get started!")
    st.markdown("### **Features**")
    st.markdown("""
- **Advanced business analytics**
- **Automated column validation**
- **Robust error recovery**
    """)

st.markdown("---")
st.markdown(f"*{CONFIG['footer']}*")







