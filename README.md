# 💳 PhonePe Transaction Intelligence: End-to-End Data Portfolio

A full-stack data analytics project simulating a real-world fintech payment environment. Built on PhonePe transaction data, this project spans the complete analytics pipeline: **Business Intelligence (Power BI)**, **Statistical Analysis (Python)**, and **AI-Powered Interactive Dashboard (Streamlit + Gemini)**.

### 🔗 Live Interactive Dashboard: *[Add your Streamlit app URL here]*

---

## 📊 Project Overview

The objective is to analyze payment transaction performance, identify revenue drivers, and surface actionable insights through an AI-integrated dashboard. The dashboard features a locally-run LLM (Ollama/LLaMA) for offline use and a cloud-deployed version powered by Google Gemini.

### Key Features

- **Power BI Dashboard**: Multi-view BI report covering revenue trends, service-level breakdowns, and payment success rates.
- **Python EDA**: Deep exploratory analysis with data cleaning, distribution analysis, and statistical validation.
- **AI-Integrated Streamlit App**: Natural language Q&A on live transaction data using Google Gemini (cloud) or LLaMA 3.2 via Ollama (local).
- **Indian Rupee Formatting**: Custom ₹ lakh/crore formatting engine built from scratch for accurate financial display.
- **Smart Column Detection**: Auto-detects amount and status columns, making the dashboard reusable across datasets.

---

## 🛠️ Technical Stack & Core Logic

### 1. Analytics Layer: Power BI 📊
**File:** `PowerBI_Dashboard.pbix`
- Multi-page report with slicers for service type, payment method, and status.
- KPIs: Total Revenue, Transaction Volume, Average Ticket Size, Success Rate.

### 2. Statistical Layer: Python EDA 🐍
**File:** `Python_Analytics_Phonepe_.ipynb`
- Data cleaning and null handling on raw transaction records.
- Distribution analysis across service types and payment categories.
- Revenue segmentation and outlier detection.

### 3. Application Layer: Streamlit Dashboard 🚀

**Two versions included:**

| File | Description |
| :--- | :--- |
| `dashboard.py` | Local version — uses **Ollama (LLaMA 3.2:1b)** for on-device AI Q&A. |
| `dashboard_cloud.py` | Cloud version — uses **Google Gemini 2.0 Flash** API for deployed app. |

**Core capabilities:**
- KPI metric cards with custom CSS (gradient dark-mode design).
- Natural language AI analyst — ask questions like *"Which service generates the most revenue?"*
- Smart success rate detection across varied column naming conventions.
- `@st.cache_data` for optimized CSV loading and filter responsiveness.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `Phonepe.csv` | Dataset containing PhonePe transaction records. |
| `Python_Analytics_Phonepe_.ipynb` | Jupyter Notebook for EDA and data cleaning. |
| `dashboard.py` | Local Streamlit app with Ollama/LLaMA AI integration. |
| `dashboard_cloud.py` | Cloud Streamlit app with Google Gemini AI integration. |
| `PowerBI_Dashboard.pbix` | Power BI file for visual storytelling. |
| `requirements.txt` | Environment dependencies. |

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

**3. Launch the local dashboard:**
```bash
streamlit run dashboard.py
```

**4. For the cloud version**, add your Gemini API key to Streamlit Secrets:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-key-here"
```
Then run:
```bash
streamlit run dashboard_cloud.py
```

> **Note:** The local version requires [Ollama](https://ollama.com/) to be installed and running with the `llama3.2:1b` model pulled (`ollama pull llama3.2:1b`).

---

## 📈 Key Insights

- **Revenue Concentration**: A small subset of high-value services accounts for a disproportionate share of total revenue.
- **Payment Success Patterns**: Success rates vary significantly across service types, highlighting operational gaps.
- **Ticket Size Distribution**: Average transaction values differ considerably between B2B and B2C service categories.
- **AI Utility**: Natural language querying surfaces insights faster than manual filter-based exploration.

---

## 🛠️ Roadmap & Future Enhancements (WIP) 🚧

- **Predictive Modeling**: Churn prediction and fraud detection using XGBoost/Random Forest.
- **Live Database Connection**: Transition from static CSV to a live SQL or Firebase connection.
- **RAG Pipeline**: Retrieval-Augmented Generation for context-aware financial Q&A over large datasets.
- **Multi-Dataset Support**: Extend the dashboard to support other fintech datasets (Paytm, Razorpay).

---

**Developed by Daksh Sharma** | *Data Analytics & Business Intelligence Portfolio*
