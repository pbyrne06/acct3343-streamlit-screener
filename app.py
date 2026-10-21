import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Technology & Software Academic Screener", layout="wide")

# --- App Headers ---
st.title("🎓 ACCT 3343: Quantitative Financial Analysis Screener")
st.write("Designed as a production-ready dashboard applying dual fundamental trading philosophies to an enterprise universe of ~100 US Software and Tech entities.")

@st.cache_data
def load_data():
    df = pd.read_csv('universe.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ 'universe.csv' was not found. Please execute the data gathering pipeline inside Colab first.")
    st.stop()

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Screening Parameters")

# Sidebar filters - Sellers (We flag companies exceeding metric limits)
st.sidebar.markdown("### 🔴 SELL Side (Earnings Quality & Distress Flags)")
sta_max = st.sidebar.slider("Max Scaled Total Accruals (STA)", min_value=float(df['Metric_1_STA'].dropna().min()), max_value=float(df['Metric_1_STA'].dropna().max()), value=float(df['Metric_1_STA'].dropna().quantile(0.80)))
z_min = st.sidebar.slider("Min Altman Z-Score Proxy (Distress Limit)", min_value=float(df['Metric_2_Z_Score'].dropna().min()), max_value=float(df['Metric_2_Z_Score'].dropna().max()), value=float(df['Metric_2_Z_Score'].dropna().quantile(0.20)))
snoa_max = st.sidebar.slider("Max Scaled Net Operating Assets (SNOA)", min_value=float(df['Metric_3_SNOA'].dropna().min()), max_value=float(df['Metric_3_SNOA'].dropna().max()), value=float(df['Metric_3_SNOA'].dropna().quantile(0.80)))

# Sidebar filters - Buyers (We capture high quality and valuation discount)
st.sidebar.markdown("### 🟢 BUY Side (Quality & Value Parameters)")
gpa_min = st.sidebar.slider("Min Gross Profitability (GPA)", min_value=float(df['Metric_4_GPA'].dropna().min()), max_value=float(df['Metric_4_GPA'].dropna().max()), value=float(df['Metric_4_GPA'].dropna().quantile(0.50)))
bm_min = st.sidebar.slider("Min Book-to-Market Ratio (B/M)", min_value=float(df['Metric_5_BM'].dropna().min()), max_value=float(df['Metric_5_BM'].dropna().max()), value=float(df['Metric_5_BM'].dropna().quantile(0.50)))

# --- Metrics Panels Summary ---
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Universe Under Analysis", value=f"{len(df)} Firms")

# Filter logic
sell_candidates = df[
    (df['Metric_1_STA'] > sta_max) |
    (df['Metric_2_Z_Score'] < z_min) |
    (df['Metric_3_SNOA'] > snoa_max)
]

buy_candidates = df[
    (df['Metric_4_GPA'] >= gpa_min) &
    (df['Metric_5_BM'] >= bm_min)
]

col2.metric(label="🔴 Identified Sell Candidates", value=f"{len(sell_candidates)} Firms")
col3.metric(label="🟢 Identified Buy Candidates", value=f"{len(buy_candidates)} Firms")

# --- Display Tables ---
st.markdown("--- ")

st.header("🔴 SELL Candidate Table (Earnings Quality Risk / Distress Flags)")
st.info("Displays companies where accruals are high (STA), distress indicators are alarming (Z-Score), or balance sheet bloating is observed (SNOA).")
if not sell_candidates.empty:
    st.dataframe(sell_candidates[['Ticker', 'Company_Name', 'Metric_1_STA', 'Metric_2_Z_Score', 'Metric_3_SNOA']].style.format({
        'Metric_1_STA': '{:.4f}',
        'Metric_2_Z_Score': '{:.2f}',
        'Metric_3_SNOA': '{:.4f}'
    }))
else:
    st.write("No candidates match current high-risk threshholds.")

st.markdown("--- ")

st.header("🟢 BUY Candidate Table (Quality & Value Strategy)")
st.success("Captures high core operating franchise capabilities (GPA) and high Book-to-Market (B/M) values expressing absolute price protection.")
if not buy_candidates.empty:
    st.dataframe(buy_candidates[['Ticker', 'Company_Name', 'Metric_4_GPA', 'Metric_5_BM']].style.format({
        'Metric_4_GPA': '{:.4f}',
        'Metric_5_BM': '{:.4f}'
    }))
else:
    st.write("No candidates meet premium quality and high value conditions concurrently.")
