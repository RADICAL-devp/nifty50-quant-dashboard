# NIFTY 50 Quantitative Dashboard

A comprehensive web-based quantitative analysis dashboard for the NIFTY 50 index, built with Streamlit. This tool provides institutional-grade risk metrics, strategy backtesting, and performance analytics for traders and quantitative analysts.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

### Market Analysis
- **Real-time Price Data**: Fetches historical NIFTY 50 data via Yahoo Finance
- **Volatility Analysis**: 21-day and 63-day rolling volatility calculations
- **Drawdown Tracking**: Real-time drawdown from peak analysis
- **Interest Rate Correlation**: Analyzes relationship between returns and rate changes

### Strategy Backtesting
- **Momentum Strategy**: Configurable lookback period (60-504 days)
- **Buy & Hold Benchmark**: Compare active strategies against passive investing
- **Performance Metrics**:
  - CAGR (Compound Annual Growth Rate)
  - Annualized Volatility
  - Sharpe Ratio
  - Sortino Ratio
  - Maximum Drawdown
  - Win Rate
  - Alpha & Beta
  - R-squared

### Risk Management
- **Value at Risk (VaR)**: Rolling VaR calculations with configurable confidence levels
- **Monte Carlo Simulation**: Stress testing with 1,000-10,000 simulation paths
- **Risk-adjusted Returns**: Comprehensive downside risk metrics

### Additional Features
- **Session-based Authentication**: Secure access to the dashboard
- **Data Caching**: Optimized performance with 1-hour TTL
- **Interactive Controls**: Real-time parameter adjustments via sidebar
- **Professional Visualizations**: Clean, publication-ready charts

## Quick Start

### Prerequisites

```bash
Python 3.8 or higher
pip (Python package installer)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nifty50-quant-dashboard.git
cd nifty50-quant-dashboard
```

2. **Create a virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run app23.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

### Default Login Credentials

```
Password: quant123
```

 **Important**: Change the default password in the code before deploying to production!

## Dependencies

Create a `requirements.txt` file with the following packages:

```txt
streamlit>=1.28.0
yfinance>=0.2.28
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
statsmodels>=0.14.0
scipy>=1.10.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Usage Guide

### 1. Authentication
- Enter the password (default: `quant123`) to access the dashboard
- Session remains active until browser is closed

### 2. Configure Parameters

**Sidebar Controls:**
- **Start Date**: Beginning of analysis period (default: 2015-01-01)
- **End Date**: End of analysis period (default: 2025-01-01)
- **Strategy**: Choose between "Momentum" or "Buy & Hold"
- **Momentum Lookback**: Adjust lookback period (60-504 days)
- **VaR Confidence**: Set confidence level for VaR (90%-99%)
- **Monte Carlo Sims**: Number of simulation paths (1,000-10,000)

### 3. Analyze Results

The dashboard displays:

**Section 1: Market Overview**
- Current NIFTY 50 price
- 21-day volatility
- Current drawdown percentage
- Total days analyzed

**Section 2: Strategy Performance**
- Complete performance metrics comparison
- Equity curve visualization
- Alpha, Beta, and R² statistics

**Section 3: Risk Analysis**
- Rolling VaR visualization
- Monte Carlo stress test scenarios

## Strategy Details

### Momentum Strategy

The momentum strategy generates signals based on rolling average returns:

```python
Signal = 1 (Long) if Average Returns > 0
Signal = 0 (Flat) if Average Returns <= 0
```

**Parameters:**
- Lookback period: 60-504 days (default: 252 days / 1 year)

**Logic:**
- Calculates rolling average returns over the lookback period
- Goes long when momentum is positive
- Exits to cash when momentum turns negative

### Buy & Hold Strategy

Simple passive investment approach:
- Buy and hold the NIFTY 50 index throughout the analysis period
- Serves as the benchmark for comparison

## Customization

### Change Authentication Password

Edit line 30 in `app23.py`:
```python
if password == "your_secure_password":  # Change this
```

### Add New Strategies

Add new strategy functions following this template:

```python
@st.cache_data(ttl=3600)
def your_strategy(df, param1, param2):
    d = df.copy()
    # Your strategy logic here
    d['Signal'] = ...  # Generate signals
    d['Strategy_Return'] = d['Signal'].shift(1) * d['Returns']
    return d
```

### Modify Data Sources

To use different indices or securities, modify the ticker symbols in `load_data()`:

```python
nifty = yf.download("YOUR_TICKER", start=start, end=end, progress=False)
```

### Customize Visualizations

All charts use matplotlib. Modify styling in the respective plotting sections:

```python
fig, ax = plt.subplots(figsize=(width, height))
ax.plot(..., color='your_color', linewidth=2)
ax.set_title('Your Title')
```

## Performance Metrics Explained

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **CAGR** | Compound Annual Growth Rate | Average annual return over the period |
| **Volatility** | Annualized standard deviation | Higher = more risk |
| **Sharpe Ratio** | Risk-adjusted return | >1 is good, >2 is excellent |
| **Sortino Ratio** | Downside risk-adjusted return | Only penalizes downside volatility |
| **Max Drawdown** | Largest peak-to-trough decline | Maximum loss from peak |
| **Win Rate** | % of positive return periods | Higher = more consistent |
| **Alpha** | Excess return vs benchmark | Positive = outperformance |
| **Beta** | Sensitivity to market moves | >1 = more volatile than market |
| **R²** | Correlation with benchmark | 1 = perfectly correlated |

## Security Considerations

**For Production Deployment:**

1. **Replace Simple Authentication** with proper auth:
   - Use Streamlit's built-in authentication
   - Implement OAuth2
   - Use environment variables for credentials

2. **Secure Password Storage**:
```python
import os
password = os.environ.get('DASHBOARD_PASSWORD')
```

3. **Add HTTPS** when deploying online

4. **Set up rate limiting** for API calls

5. **Implement user session management**

## Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t nifty-dashboard .
docker run -p 8501:8501 nifty-dashboard
```

### Heroku Deployment

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Create `Procfile`:
```
web: sh setup.sh && streamlit run app23.py
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Data Sources

- **NIFTY 50 Data**: Yahoo Finance (^NSEI)
- **Interest Rate Data**: 10-Year Treasury Note (^TNX)
- **Data Frequency**: Daily close prices
- **Adjustment**: All prices are adjusted for splits and dividends

## Limitations & Disclaimers

1. **Historical Data Only**: Past performance does not guarantee future results
2. **No Transaction Costs**: Backtests do not include commissions, slippage, or taxes
3. **Market Hours**: Data reflects only regular trading hours
4. **Survivorship Bias**: Index composition changes not accounted for
5. **No Financial Advice**: This tool is for educational and research purposes only

**Disclaimer**: This dashboard is provided "as-is" without any warranties. The authors are not responsible for any trading losses incurred from using this tool. Always consult with a qualified financial advisor before making investment decisions.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Ideas
- Add more trading strategies (mean reversion, pairs trading, etc.)
- Implement machine learning models
- Add more risk metrics (CVaR, Expected Shortfall)
- Create downloadable reports
- Add email alerts for signals
- Implement portfolio optimization

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing framework
- [yfinance](https://github.com/ranaroussi/yfinance) - For market data access
- [Statsmodels](https://www.statsmodels.org/) - For statistical modeling
- [Matplotlib](https://matplotlib.org/) - For visualization capabilities

## Resources

### Learn More About Quantitative Trading
- [Quantitative Trading Strategies](https://www.quantstart.com/)
- [Python for Finance](https://www.oreilly.com/library/view/python-for-finance/9781492024323/)
- [Algorithmic Trading](https://www.investopedia.com/terms/a/algorithmictrading.asp)

### Streamlit Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Community](https://discuss.streamlit.io/)

---
