# Market Strategy Backtester

A Python backtesting engine implementing a **Moving Average Crossover** strategy on real OHLC data.

## What it does
- Fetches real daily OHLC data via `yfinance` (no API key needed)
- Computes 20-day and 50-day simple moving averages
- Generates buy/sell signals on MA crossover events
- Reports final PnL and compares against buy-and-hold benchmark

## How to run
```bash
pip install yfinance pandas
python backtester.py
```

## Sample output
```
  BUY  on 2020-04-30 @ $70.92  →  141.00 shares
  SELL on 2020-10-02 @ $109.63  →  $15,456.82 cash
  ...
  Strategy Return: 69.08%
  Buy & Hold     : 163.19%
  Total Trades   : 21
```

## Concepts implemented
- **OHLC data**: Open, High, Low, Close daily price data
- **Moving Average**: rolling mean of closing prices over N days
- **Crossover signal**: short MA crossing above long MA = buy; below = sell
- **PnL tracking**: full portfolio simulation with cash and share positions