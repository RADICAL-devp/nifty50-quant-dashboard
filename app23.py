import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="NIFTY 50 Quant Dashboard",
    page_icon="📈"
)

# -------------------------------------------------
# SIMPLE AUTHENTICATION (SESSION BASED)
# -------------------------------------------------
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 Login Required")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "quant123":  # CHANGE THIS
                st.session_state.authenticated = True
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Invalid password")
        st.stop()

authenticate()

# -------------------------------------------------
# HELPER FUNCTIONS (CACHED)
# -------------------------------------------------
@st.cache_data(ttl=3600)
def load_data(start, end):
    nifty = yf.download("^NSEI", start=start, end=end, progress=False)
    rates = yf.download("^TNX", start=start, end=end, progress=False)

    prices = nifty[['Adj Close']].rename(columns={'Adj Close': 'Price'})
    rates = rates[['Adj Close']].rename(columns={'Adj Close': 'Rate'})
    return prices.merge(rates, left_index=True, right_index=True).dropna()

@st.cache_data(ttl=3600)
def calculate_returns(data):
    df = data.copy()
    df['Returns'] = df['Price'].pct_change()
    df['Rate_Change'] = df['Rate'].pct_change()
    df['Vol_21D'] = df['Returns'].rolling(21).std() * np.sqrt(252)
    df['Vol_63D'] = df['Returns'].rolling(63).std() * np.sqrt(252)
    df['Cumulative'] = (1 + df['Returns']).cumprod()
    df['Peak'] = df['Cumulative'].cummax()
    df['Drawdown'] = (df['Cumulative'] - df['Peak']) / df['Peak']
    return df.dropna()

@st.cache_data(ttl=3600)
def momentum_strategy(df, lookback):
    d = df.copy()
    d['Momentum'] = d['Returns'].rolling(lookback).mean()
    d['Signal'] = np.where(d['Momentum'] > 0, 1, 0)
    d['Strategy_Return'] = d['Signal'].shift(1) * d['Returns']
    return d

@st.cache_data(ttl=3600)
def performance_metrics(returns):
    returns = returns.dropna()
    cagr = (1 + returns).prod() ** (252 / len(returns)) - 1
    vol = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    downside = returns[returns < 0].std() * np.sqrt(252)
    sortino = (returns.mean() * 252) / downside if downside > 0 else 0
    max_dd = ((1 + returns).cumprod() / (1 + returns).cumprod().cummax() - 1).min()
    win_rate = (returns > 0).mean()
    return cagr, vol, sharpe, sortino, max_dd, win_rate

@st.cache_data(ttl=3600)
def alpha_beta(strategy, benchmark):
    df = pd.concat([strategy, benchmark], axis=1).dropna()
    df.columns = ["strategy", "benchmark"]
    X = sm.add_constant(df['benchmark'])
    model = sm.OLS(df['strategy'], X).fit()
    alpha = model.params['const'] * 252
    beta = model.params['benchmark']
    return alpha, beta, model.rsquared

@st.cache_data(ttl=3600)
def rolling_var(returns, window, confidence):
    return returns.rolling(window).quantile(1 - confidence)

@st.cache_data(ttl=3600)
def monte_carlo(mu, sigma, sims):
    np.random.seed(42)
    sims_data = np.random.normal(mu, sigma * 3, (sims, 252))
    return 100 * np.cumprod(1 + sims_data, axis=1)

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
st.sidebar.title("📊 Controls")

start = st.sidebar.date_input("Start Date", datetime(2015, 1, 1))
end = st.sidebar.date_input("End Date", datetime(2025, 1, 1))

strategy = st.sidebar.selectbox("Strategy", ["Momentum", "Buy & Hold"])
lookback = st.sidebar.slider("Momentum Lookback", 60, 504, 252)
confidence = st.sidebar.slider("VaR Confidence", 0.90, 0.99, 0.95)
mc_sims = st.sidebar.slider("Monte Carlo Sims", 1000, 10000, 5000, 1000)

# -------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------
st.title("📈 NIFTY 50 Quantitative Dashboard")

data = load_data(start, end)
data = calculate_returns(data)

if strategy == "Momentum":
    data = momentum_strategy(data, lookback)
    strat_returns = data['Strategy_Return']
else:
    strat_returns = data['Returns']

# -------------------------------------------------
# MARKET OVERVIEW
# -------------------------------------------------
st.header("1️⃣ Market Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price", f"₹{data['Price'].iloc[-1]:,.2f}")
c2.metric("21D Volatility", f"{data['Vol_21D'].iloc[-1]:.2%}")
c3.metric("Current Drawdown", f"{data['Drawdown'].iloc[-1]:.2%}")
c4.metric("Days Analyzed", len(data))

# -------------------------------------------------
# PERFORMANCE
# -------------------------------------------------
st.header("2️⃣ Strategy Performance")

cagr, vol, sharpe, sortino, max_dd, win = performance_metrics(strat_returns)
bcagr, _, _, _, _, _ = performance_metrics(data['Returns'])

a, b, r2 = alpha_beta(strat_returns, data['Returns'])

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("CAGR", f"{cagr:.2%}", f"{cagr - bcagr:.2%}")
c2.metric("Volatility", f"{vol:.2%}")
c3.metric("Sharpe", f"{sharpe:.2f}")
c4.metric("Sortino", f"{sortino:.2f}")
c5.metric("Max DD", f"{max_dd:.2%}")
c6.metric("Win Rate", f"{win:.2%}")

c7, c8, c9 = st.columns(3)
c7.metric("Alpha (Annual)", f"{a:.2%}")
c8.metric("Beta", f"{b:.2f}")
c9.metric("R²", f"{r2:.2f}")

# -------------------------------------------------
# EQUITY CURVE
# -------------------------------------------------
st.subheader("Equity Curve")

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot((1 + strat_returns).cumprod(), label="Strategy")
ax.plot((1 + data['Returns']).cumprod(), label="Benchmark", alpha=0.7)
ax.legend()
ax.grid(True)
st.pyplot(fig)
plt.close()

# -------------------------------------------------
# RISK ANALYSIS
# -------------------------------------------------
st.header("3️⃣ Risk Analysis")

rolling_VaR = rolling_var(data['Returns'], 60, confidence)

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(rolling_VaR, color="red")
ax.set_title("Rolling VaR")
ax.grid(True)
st.pyplot(fig)
plt.close()

# Monte Carlo
st.subheader("Monte Carlo Stress Test")

mu, sigma = data['Returns'].mean(), data['Returns'].std()
paths = monte_carlo(mu, sigma, mc_sims)

fig, ax = plt.subplots(figsize=(14, 5))
for i in range(100):
    ax.plot(paths[i], color="red", alpha=0.05)
ax.grid(True)
st.pyplot(fig)
plt.close()

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("Quantitative dashboard for strategy research & risk analysis")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")