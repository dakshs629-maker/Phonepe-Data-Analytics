import streamlit as st
import pandas as pd
import numpy as np

# CONFIG first
CONFIG = {
    "title": "PhonePe Transaction Intelligence",      
    "amount_keyword": "amount",                       
    "footer": "MBA Data Portfolio"                    
}

# Page config BEFORE any markdown
st.set_page_config(page_title=CONFIG["title"].replace(" ", ""), layout="wide")

# CSS AFTER config (safe position)
st.markdown("""
<style>
.metric-card {background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin: 0.5rem 0;}
.summary-box {background: rgba(46, 125, 50, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #4caf50; margin: 1rem 0;}
.insights-box {background: rgba(156, 39, 176, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #9c27b0; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# Rest of your code stays IDENTICAL...
st.title(f"💳 {CONFIG['title']}")
# ... (everything else unchanged)

