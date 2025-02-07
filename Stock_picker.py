import yfinance as yf
import numpy as np
import pandas as pd
import joblib
from transformers import pipeline  # NLP for earnings sentiment
import torch

# ✅ Load Pretrained MLQuant Model (Fundamentals)
mlquant_model = joblib.load("mlquant_model.pkl")

# ✅ Load StockSentimentBERT Model (Earnings Sentiment)
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

# 📌 Step 1: Fetch Stock Fundamentals
def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    return {
        "Revenue": stock.financials.loc["Total Revenue"][0],
        "Net Income": stock.financials.loc["Net Income"][0],
        "ROE": stock.financials.loc["Net Income"][0] / stock.balance_sheet.loc["Total Shareholder Equity"][0],
        "Debt/Equity": stock.balance_sheet.loc["Total Liabilities"][0] / stock.balance_sheet.loc["Total Shareholder Equity"][0],
        "FCF": stock.cashflow.loc["Total Cash From Operating Activities"][0] - stock.cashflow.loc["Capital Expenditures"][0],
        "P/E": stock.info["trailingPE"] if "trailingPE" in stock.info else np.nan
    }

# 📌 Step 2: Earnings Sentiment Analysis (StockSentimentBERT)
def earnings_sentiment(ticker):
    earnings_text = fetch_earnings_call_transcript(ticker)  # Custom function needed
    sentiment_score = sentiment_pipeline(earnings_text)[0]["score"]
    return sentiment_score  # -1 (negative) to 1 (positive)

# 📌 Step 3: Compute Intrinsic Value (DCF Model)
def compute_intrinsic_value(ticker):
    data = get_fundamentals(ticker)
    future_cashflows = [data["FCF"] * (1.05 ** i) for i in range(10)]  # Assume 5% growth
    discount_rate = 0.08  # Buffett typically uses 8%
    dcf_value = sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(future_cashflows))
    return dcf_value

# 📌 Step 4: Predict Long-Term Potential (MLQuant Model)
def evaluate_stock(ticker, weight_fundamentals, weight_sentiment):
    fundamentals = get_fundamentals(ticker)
    sentiment = earnings_sentiment(ticker)

    # Convert to DataFrame for MLQuant model
    features = pd.DataFrame([{**fundamentals, "Sentiment": sentiment}])
    quant_score = mlquant_model.predict(features)[0]  # MLQuant Score (0-100)

    # Final Rating (User-defined Weights)
    final_score = (weight_fundamentals * quant_score) + (weight_sentiment * (sentiment * 100))

    return {
        "Ticker": ticker,
        "Fundamental Score": quant_score,
        "Earnings Sentiment": sentiment,
        "Final Score": final_score,
        "Verdict": "Strong Buy" if final_score > 75 else "Hold" if final_score > 50 else "Avoid",
        "Intrinsic Value Estimate": compute_intrinsic_value(ticker),
    }

# 🔥 Run Interactive Stock Analysis
ticker = input("Enter stock ticker: ").upper()

# 🎛️ Let user pick weight distribution
print("\n🎛️ Customize Weighting (Default: 70% Fundamentals, 30% Sentiment)")
weight_fundamentals = float(input("Enter weight for FUNDAMENTALS (0 to 1): ") or 0.7)
weight_sentiment = float(input("Enter weight for SENTIMENT (0 to 1): ") or 0.3)

# Ensure weights add up to 1
total_weight = weight_fundamentals + weight_sentiment
if total_weight != 1:
    weight_fundamentals /= total_weight
    weight_sentiment /= total_weight

analysis = evaluate_stock(ticker, weight_fundamentals, weight_sentiment)

# 📊 Display Analysis Results
print("\n🔍 **Stock Analysis Summary**")
print(f"📈 Ticker: {analysis['Ticker']}")
print(f"💰 Fundamental Score: {analysis['Fundamental Score']:.2f}/100")
print(f"🧠 Management Sentiment: {analysis['Earnings Sentiment']:.2f} (-1 to 1)")
print(f"📊 Final Score: {analysis['Final Score']:.2f}/100")
print(f"💎 Intrinsic Value Estimate: ${analysis['Intrinsic Value Estimate']:.2f}")
print(f"🛒 Verdict: **{analysis['Verdict']}**")
