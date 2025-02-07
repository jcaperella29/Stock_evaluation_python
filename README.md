# Stock_evaluation_Python 🏦📊

A Python script to classify companies based on financial metrics like the **Piotroski F-Score** and **Stock Valuation**. It processes CSV financial data for multiple companies and outputs a classification (`Strong`, `Medium`, or `Weak`) for each company.

---

## Features 🚀
- Computes **Piotroski F-Score** based on profitability, leverage, and efficiency metrics.
- Calculates **Stock Valuation** using **P/E Ratio** and **P/B Ratio**.
- Classifies companies into `Strong`, `Medium`, or `Weak` based on their metrics.
- Handles missing or invalid financial data gracefully.
- Saves the results as a CSV file.

---

## How It Works 🛠️
1. Loads financial data from CSV files for specified company tickers.
2. Computes the following metrics:
   - **Piotroski F-Score**: Combines 9 financial metrics to score financial health.
   - **Stock Valuation**: The sum of P/E Ratio and P/B Ratio.
3. Classifies companies based on the metrics:
   - `Strong`: F-Score ≥ 7 and Valuation < 20
   - `Medium`: F-Score ≥ 4 and Valuation < 30
   - `Weak`: All others
4. Outputs a CSV file with the results.

---

## Usage 🖥️
### **1. Install Dependencies**
Ensure you have **Python 3.7+** and the following Python libraries installed:
```bash
pip install pandas
. Directory Setup
Organize your data in the following structure:

Copy
Edit
financial_data/
│
├── GM_ratios.csv
├── GM_cash_flow.csv
├── GM_balance_sheet.csv
├── GM_income_statement.csv
├── TSLA_ratios.csv
├── TSLA_cash_flow.csv
├── TSLA_balance_sheet.csv
├── TSLA_income_statement.csv
├── AAPL_ratios.csv
├── AAPL_cash_flow.csv
├── AAPL_balance_sheet.csv
├── AAPL_income_statement.csv
3. Run the Script
Save the script as stock_picker.py, and execute it:





