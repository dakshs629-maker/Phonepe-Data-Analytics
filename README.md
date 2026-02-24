# 💳 PhonePe Transaction & Financial Health Analytics

> An end-to-end data analytics project covering **300,000 PhonePe transactions** — from raw data exploration to statistical hypothesis testing to an AI-powered interactive dashboard.

---

🌐 Live Demo: https://phonepe-data-analytics-dedtwcb7rffgzbveeraa8m.streamlit.app/

---

## 📌 Project Overview

This project analyses a synthetic dataset of 300,000 PhonePe transactions spanning three major service categories: **Loans**, **Insurance**, and **Recharge & Bills**. The goal is to uncover transaction patterns, quantify payment failure drivers, and surface business-ready insights through both Python analytics and an interactive Streamlit dashboard.

The project is structured in three stages:

1. **Python EDA & Inferential Statistics** — Data cleaning, distribution analysis, and hypothesis testing in a Jupyter Notebook.
2. **Power BI Dashboard** — Static BI report for stakeholder-facing visual exploration.
3. **Streamlit Web App** — A live, AI-powered dashboard deployable locally (via Ollama) or to the cloud (via Gemini API).

---

## 📊 Dataset

**File:** `Phonepe.csv` — 300,000 records

| Column | Description |
|---|---|
| `Transaction_ID` | Unique transaction identifier (e.g., `RCG_0C338474B366`) |
| `Amount` | Transaction value in INR |
| `User_ID` | Anonymised user identifier |
| `Service` | Top-level category (`Recharge_Bills`, `Loans`, `Insurance`) |
| `Service Type` | Sub-category (e.g., `DTH`, `Mobile Recharge`, `FASTag Recharge`, `Cable TV`) |
| `Payment_Status` | Outcome: `Successful` or `Failed` |
| `Reason` | Reason for outcome (e.g., `Bank Denied`, `Wrong PIN`, `Server Error`) |
| `Date` | Transaction date (2024) |

---

## 📈 Key Analytical Findings

**Transaction Distribution**
The distribution of transaction amounts is heavily right-skewed — the vast majority of transactions are small-value, with a long tail of high-value loan disbursements pulling the mean upward.

**Service Comparison — Independent Samples T-Test**
A two-sample T-test confirmed a statistically significant difference (*p* < 0.05) between Loan and Insurance transaction sizes. Insurance transactions are capped at ₹20,000 by design, while Loan amounts regularly reach ₹1,00,000 — validating the structural difference in product risk profiles.

**Failure Analysis — Chi-Square Test of Independence**
A Chi-Square test revealed a statistically significant association between Service type and Payment Status. Failure reasons are not uniformly distributed across services: `Bank Denied` and `Wrong Info` are failure modes unique to the **Loans** service, while `Wrong PIN` and `Server Error` appear across all categories — pointing to both product-specific and infrastructure-level issues.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| Statistical Testing | SciPy (`ttest_ind`, `chi2_contingency`) |
| Visualisation (Python) | Matplotlib, Seaborn |
| BI Dashboard | Power BI Desktop |
| Web App | Streamlit |
| Cloud AI | Google Gemini API (`gemini-2.5-flash`) |

---

## 📂 File Structure

```
├── Phonepe.csv                        # Primary dataset (300,000 records)
├── Python_Analytics_Phonepe_.ipynb    # EDA, univariate/bivariate analysis, hypothesis tests
├── PowerBI_Dashboard.pbix             # Power BI interactive report
├── dashboard_cloud.py                 # Streamlit app — cloud deployment (Gemini AI)
└── requirements.txt                   # Python dependencies
```

---

## 🚀 How to Run

### 1. Python Analysis
Open `Python_Analytics_Phonepe_.ipynb` in Jupyter Lab or Google Colab. Ensure `Phonepe.csv` is in the same directory before running.

### 2. Power BI Dashboard
Open `PowerBI_Dashboard.pbix` in Power BI Desktop to explore the interactive visual report.

### 3. Streamlit Dashboard — Cloud (Gemini)

Designed for deployment on [Streamlit Community Cloud](https://streamlit.io/cloud). Add your Gemini API key as a secret:

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-key-here"
```

Then deploy `dashboard_cloud.py` as the entry point. The app will auto-load `Phonepe.csv` if placed in the repository root, or accept a user-uploaded CSV via the sidebar.

---

## 🤖 Dashboard Features

- **KPI Cards** — Total transactions, total revenue, average ticket size (Indian lakh/crore formatting: ₹X,XX,XX,XXX)
- **Transaction Table** — Paginated preview of the most recent records
- **Smart AI Q&A** — Ask natural language business questions; answered by Gemini 2.5 Flash
- **Quick Stats Panel** — Auto-detects success/failure columns, top service category, and highest-value transaction
- **Auto Column Detection** — Intelligently identifies the amount column using keyword matching

---

## 📦 Dependencies

```
streamlit==1.38.0
pandas==2.2.2
numpy==2.1.1
requests==2.32.3
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🔭 Future Scope

- **Failure Prediction** — Train a Random Forest or XGBoost classifier to predict transaction failure probability based on service type, amount tier, and user history.
- **Time-Series Forecasting** — Apply SARIMA or Prophet on the `Date` column to forecast peak transaction windows and support infrastructure capacity planning.
- **Anomaly Detection** — Flag unusually large transactions or sudden spikes in failure rates as potential fraud signals.
- **Cohort Analysis** — Track User_ID behaviour across dates to identify retention patterns and repeat transaction tendencies.

---

## 👤 Author

**MBA Data Portfolio**
Built as a demonstration of end-to-end data analytics — from hypothesis-driven Python analysis to production-ready dashboard deployment.
