import yfinance as yf
import pandas as pd

# ── CONFIG ────────────────────────────────────────────────
TICKER      = "AAPL"       # Stock to backtest (Apple)
START_DATE  = "2020-01-01"
END_DATE    = "2024-01-01"
SHORT_WINDOW = 20          # Short moving average: 20 days
LONG_WINDOW  = 50          # Long moving average:  50 days
INITIAL_CASH = 10000       # Start with $10,000 (paper money)
# ──────────────────────────────────────────────────────────

def fetch_data(ticker, start, end):
    """Download historical closing prices from Yahoo Finance."""
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    df = df[["Close"]].copy()
    df.columns = ["close"]
    return df

def compute_signals(df, short_window, long_window):
    """
    Calculate moving averages and generate buy/sell signals.
    Signal = 1 means 'hold stock', 0 means 'hold cash'.
    """
    df["ma_short"] = df["close"].rolling(window=short_window).mean()
    df["ma_long"]  = df["close"].rolling(window=long_window).mean()

    # When short MA > long MA → uptrend → signal = 1 (buy/hold)
    # When short MA < long MA → downtrend → signal = 0 (sell/hold cash)
    df["signal"] = 0
    df.loc[df["ma_short"] > df["ma_long"], "signal"] = 1

    # 'position' tells us when the signal CHANGES (actual trade days)
    # +1 = buy event,  -1 = sell event,  0 = no change
    df["position"] = df["signal"].diff()

    return df

def run_backtest(df, initial_cash):
    """
    Simulate trading: start with cash, buy/sell on signals, track portfolio value.
    """
    cash        = initial_cash
    shares_held = 0
    portfolio_values = []

    for date, row in df.iterrows():
        price = row["close"]

        if pd.isna(price) or pd.isna(row["position"]):
            portfolio_values.append(cash)
            continue

        # BUY: spend all cash on shares
        if row["position"] == 1 and cash > 0:
            shares_held = cash / price
            cash = 0
            print(f"  BUY  on {date.date()} @ ${price:.2f}  →  {shares_held:.2f} shares")

        # SELL: convert all shares back to cash
        elif row["position"] == -1 and shares_held > 0:
            cash = shares_held * price
            shares_held = 0
            print(f"  SELL on {date.date()} @ ${price:.2f}  →  ${cash:.2f} cash")

        # Portfolio value = cash in hand + value of shares held
        total_value = cash + (shares_held * price)
        portfolio_values.append(total_value)

    df["portfolio_value"] = portfolio_values
    return df

def print_results(df, initial_cash):
    """Print a clean summary of backtest performance."""
    final_value   = df["portfolio_value"].iloc[-1]
    total_return  = ((final_value - initial_cash) / initial_cash) * 100

    # Compare against simply buying and holding the whole time (benchmark)
    buy_hold_return = ((df["close"].iloc[-1] - df["close"].iloc[0])
                       / df["close"].iloc[0]) * 100

    num_trades = int(df["position"].abs().sum())

    print("\n" + "="*45)
    print("         BACKTEST RESULTS SUMMARY")
    print("="*45)
    print(f"  Ticker         : {TICKER}")
    print(f"  Period         : {START_DATE} → {END_DATE}")
    print(f"  Strategy       : MA Crossover ({SHORT_WINDOW}/{LONG_WINDOW})")
    print(f"  Initial Cash   : ${initial_cash:,.2f}")
    print(f"  Final Value    : ${final_value:,.2f}")
    print(f"  Strategy Return: {total_return:.2f}%")
    print(f"  Buy & Hold     : {buy_hold_return:.2f}%")
    print(f"  Total Trades   : {num_trades}")
    print("="*45)

# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching {TICKER} data from {START_DATE} to {END_DATE}...")
    df = fetch_data(TICKER, START_DATE, END_DATE)

    print("Computing moving average signals...")
    df = compute_signals(df, SHORT_WINDOW, LONG_WINDOW)

    print("\nSimulating trades:")
    df = run_backtest(df, INITIAL_CASH)

    print_results(df, INITIAL_CASH)