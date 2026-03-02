# 💳 PhonePe Transaction Intelligence — End-to-End Data Portfolio

India's UPI ecosystem processed over ₹200 trillion in FY24, with PhonePe commanding ~48% market share. But volume dominance masks a structural tension: zero-MDR on UPI limits direct revenue per transaction, making service-mix and ticket-size optimisation critical for sustainable growth. This project analyses transaction patterns across service types, identifies revenue concentration risk, and deploys an AI-integrated dashboard that allows non-technical stakeholders to query data in natural language — reducing analyst dependency for routine business questions.

### 🔗 Live Dashboard: [phonepe-data-analytics-dedtwcb7rffgzbveeraa8m.streamlit.app](https://phonepe-data-analytics-dedtwcb7rffgzbveeraa8m.streamlit.app/)

---

## 📊 Project Overview

A full-stack analytics project spanning **Business Intelligence (Power BI)** → **Statistical Analysis (Python)** → **AI-Powered Interactive Dashboard (Streamlit + Gemini)** — built on PhonePe transaction data covering multiple service types and payment categories.

### Key Features
- **Power BI Dashboard:** Multi-page report with slicers for service type, payment method, and status — covering Revenue, Transaction Volume, Average Ticket Size, and Success Rate.
- **Python EDA:** Data cleaning, distribution analysis across service types, revenue segmentation, and outlier detection.
- **AI-Integrated Streamlit App:** Natural language Q&A on live transaction data using Google Gemini (cloud deployment) or LLaMA 3.2 via Ollama (local).
- **Dual Deployment Architecture:** A local version for offline use and a cloud-deployed version — demonstrating understanding of environment-specific engineering constraints.
- **Indian Rupee Formatting Engine:** Custom ₹ lakh/crore formatter built from scratch for accurate financial display in the Indian number system.

---

## 📈 Key Insights

**1. Revenue Concentration (Pareto Effect)**
Loans alone account for ~73% of total transaction value ($2.53bn out of $3.47bn) despite being one of four service categories. Money Transfer, Insurance, and Recharge & Bills collectively account for the remaining 27%. This concentration creates platform dependency risk — a regulatory change or competitive pressure on the lending vertical could materially impact total platform revenue. Diversification into higher-frequency categories like Recharge & Bills is the strategic long-term hedge.

**2. Critical Success Rate Variance Across Services**
Payment success rates vary by over 40 percentage points across service categories — from 96% in Recharge & Bills and Money Transfer down to just 56% in Loans. Nearly half of all loan transactions failing is a significant operational red flag, with "Bank Denied" and "Wrong Info" as the leading failure reasons. This represents both direct revenue leakage and churn risk — failed transactions have a well-documented correlation with app abandonment in fintech. Loan transaction success rate improvement is the single highest-leverage operational fix available.

**3. Ticket Size Segmentation**
Average ticket size differs significantly between service categories — Loans average ~$199K per transaction vs. ~$4 per transaction in Recharge & Bills, implying two fundamentally distinct user segments: high-value low-frequency B2B/lending users and low-value high-frequency B2C utility users. These segments require entirely different retention strategies — reliability SLAs and reconciliation tooling for lending users; loyalty rewards and cashbacks for utility users.

**4. AI Query Utility — The Dashboard Differentiator**
The Gemini-integrated Q&A layer reduces time-to-insight for business questions from hours (analyst query → report) to seconds (natural language → answer). This architecture mirrors what fintech analytics teams at companies like Razorpay and CRED are actively building — making this project directly relevant to roles in product analytics, growth, and fintech strategy.

---

## 🛠️ Technical Stack

| Layer | Tool | Purpose |
| :--- | :--- | :--- |
| Visualisation | Power BI | Revenue, volume, and success rate dashboards |
| Statistics | Python / pandas / scipy | EDA, distribution analysis, outlier detection |
| AI (Cloud) | Google Gemini 2.0 Flash | Natural language Q&A via API |
| AI (Local) | Ollama / LLaMA 3.2:1b | On-device Q&A without API dependency |
| Application | Streamlit | Live interactive deployment |

---

## 🤖 AI Integration — Technical Note

> The Gemini Q&A layer operates on summarised data context (aggregated KPIs and column samples) rather than full record-level querying. This is a deliberate architectural choice for cloud deployment efficiency, keeping API payload sizes within rate limits. A planned enhancement will implement a RAG (Retrieval-Augmented Generation) pipeline for granular record-level natural language querying.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `Phonepe.csv` | PhonePe transaction dataset |
| `Python_Analytics_Phonepe_.ipynb` | Jupyter Notebook — EDA and data cleaning |
| `dashboard.py` | Local Streamlit app with Ollama/LLaMA integration |
| `dashboard_cloud.py` | Cloud Streamlit app with Google Gemini integration |
| `PowerBI_Dashboard.pbix` | Power BI multi-page report |
| `requirements.txt` | Python dependencies |

---

## ⚙️ Installation & Usage

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/phonepe-transaction-intelligence.git
cd phonepe-transaction-intelligence
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the local dashboard (requires Ollama):**
```bash
ollama pull llama3.2:1b
streamlit run dashboard.py
```

**4. Run the cloud dashboard:**

Add your Gemini API key to Streamlit Secrets:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-key-here"
```
Then:
```bash
streamlit run dashboard_cloud.py
```

---

## 🛠️ Roadmap

- **Near-term:** Add KMeans clustering (k=3) to Python notebook for customer segmentation — `Low-Value Frequent`, `Mid-Value Regular`, `High-Value Occasional` — to enrich the analytical narrative.
- **Near-term:** Expand Gemini context to include full dataframe summary and top/bottom record samples for richer Q&A responses.
- **Post-certification:** Fraud detection model using Isolation Forest on transaction outliers — directly applicable to PhonePe's risk and trust use case.
- **Long-term:** RAG pipeline (LangChain + Chroma) over transaction data for true record-level natural language querying; live database connection replacing static CSV.

---

**Developed by Daksh Sharma** | *Data Analytics & Business Intelligence Portfolio*
