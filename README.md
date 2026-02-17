# PhonePe Transaction & Financial Health Analytics

## 📌 Project Overview
This project provides a comprehensive end-to-end analysis of **300,000 PhonePe transactions**. The objective was to identify transaction patterns across diverse services (Loans, Insurance, Recharges) and utilize inferential statistics to uncover the root causes of payment failures.

The project transitions from **Exploratory Data Analysis (EDA)** and **Statistical Hypothesis Testing** in Python to a **Business Intelligence Dashboard** in Power BI.

## 📊 Key Insights & Statistical Findings
* **Transaction Distribution:** Initial analysis revealed a heavily right-skewed distribution of transaction amounts, indicating that the vast majority of transactions are of low value.
* **Service Comparison (T-Test):** A T-test confirmed a statistically significant difference ($p < 0.05$) between Loan and Insurance transaction sizes. While Insurance transactions are strictly capped at ₹20,000, Loan amounts frequently reach up to ₹100,000.
* **Failure Analysis (Chi-Square):** A Chi-Square Test of Independence revealed a significant relationship between Service type and Payment Status.
* **Domain-Specific Failures:** "Bank Denied" and "Wrong Info" are failure reasons unique to the **Loans** service, while "Wrong PIN" and "Server Error" are common across all categories.

[Image of a data science project lifecycle]

## 🛠️ Tech Stack
* **Data Processing:** Python (Pandas, NumPy)
* **Statistical Analysis:** Scipy.stats (T-Tests, Chi-Square)
* **Visualization:** Seaborn, Matplotlib, Power BI
* **Dataset:** 300,000 records including Transaction ID, Amount, Service Type, and Payment Status.

## 📂 File Structure
* `Phonepe.csv`: The primary dataset containing 300,000 transaction records.
* `Python Analytics Phonepe.ipynb`: Jupyter Notebook containing data cleaning, univariate/bivariate analysis, and inferential statistics.
* `PhonePe Dashboard.pbix`: Power BI dashboard for interactive visual exploration of transaction trends and failure rates.

## 🚀 How to Run
1. **Python Analysis:** Open
