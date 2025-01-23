Here’s the implementation of the RSI-based trading strategy using `backtesting.py`. The code includes all the necessary components, such as imports, strategy class, entry/exit logic, risk management, and parameter optimization. It also includes Moon Dev-themed debug prints for better visualization. 🌙✨🚀

```python
# Import necessary libraries
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Clean and preprocess data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()  # Clean column names
data = data.drop(columns=[col for col in data.columns if 'unnamed' in col.lower()])  # Drop unnamed columns

# Map columns to required format
data.rename(columns={
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'close': 'Close',
    'volume': 'Volume'
}, inplace=True)

# Ensure datetime format
data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

# Define the RSI-based strategy
class RSIStrategy(Strategy):
    # Define strategy parameters
    rsi_period = 14
    overbought = 70
    oversold = 30
    risk_per_trade = 0.01  # Risk 1% of account per trade
    risk_reward_ratio = 2  # Risk-reward ratio for take profit

    def init(self):
        # Calculate RSI using TA-Lib
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        print("🌙 RSI Indicator Initialized! ✨")

    def next(self):
        # Calculate position size based on risk management
        account_balance = self.equity
        risk_amount = account_balance * self.risk_per_trade
        stop_loss_pct = 0.02  # 2% stop loss (adjust as needed)
        position_size = risk_amount / (self.data.Close[-1] * stop_loss_pct)

        # Entry logic for buy
        if crossover(self.rsi, self.oversold):
            print("🚀 Buy Signal Detected! RSI crossed above 30 🌙")
            stop_loss = self.data.Low[-1] * (1 - stop_loss_pct)  # Stop loss below recent swing low
            take_profit = self.data.Close[-1] * (1 + (stop_loss_pct * self.risk_reward_ratio))  # Take profit
            self.buy(size=position_size, sl=stop_loss, tp=take_profit)
            print(f"🌙 Entered Buy Trade | Size: {position_size:.2f} | SL: {stop_loss:.2f} | TP: {take_profit:.2f} ✨")

        # Entry logic for sell
        elif crossover(self.overbought, self.rsi):
            print("🚀 Sell Signal Detected! RSI crossed below 70 🌙")
            stop_loss = self.data.High[-1] * (1 + stop_loss_pct)  # Stop loss above recent swing high
            take_profit = self.data.Close[-1] * (1 - (stop_loss_pct * self.risk_reward_ratio))  # Take profit
            self.sell(size=position_size, sl=stop_loss, tp=take_profit)
            print(f"🌙 Entered Sell Trade | Size: {position_size:.2f} | SL: {stop_loss:.2f} | TP: {take_profit:.2f} ✨")

# Initialize backtest
bt = Backtest(data, RSIStrategy, cash=1_000_000, commission=0.002)

# Run initial backtest
print("🌙 Running Initial Backtest... ✨")
stats = bt.run()
print(stats)
print(stats._strategy)

# Show initial performance plot
bt.plot()

# Optimize parameters
print("🌙 Optimizing Parameters... ✨")
optimization_results = bt.optimize(
    rsi_period=range(10, 20, 2),
    overbought=range(65, 75, 2),
    oversold=range(25, 35, 2),
    risk_reward_ratio=range(1, 4, 1),
    maximize='Return [%]'
)
print("🌙 Optimization Results: ✨")
print(optimization_results)

# Run backtest with optimized parameters
print("🌙 Running Backtest with Optimized Parameters... ✨")
optimized_stats = bt.run(**optimization_results._params)
print(optimized_stats)
print(optimized_stats._strategy)

# Show optimized performance plot
bt.plot()
```

---

### Explanation of the Code:
1. **Data Handling**:
   - The data is cleaned and preprocessed to match the required format for `backtesting.py`.
   - Columns are renamed and formatted to ensure compatibility.

2. **Strategy Class**:
   - The `RSIStrategy` class defines the RSI-based trading logic.
   - The `init` method calculates the RSI indicator using TA-Lib.
   - The `next` method implements the entry/exit logic based on RSI thresholds and risk management.

3. **Risk Management**:
   - Position sizing is calculated based on a fixed risk percentage (1% of account balance).
   - Stop loss and take profit levels are dynamically calculated using a risk-reward ratio.

4. **Parameter Optimization**:
   - The `optimize` method is used to find the best combination of RSI period, overbought/oversold thresholds, and risk-reward ratio.
   - Optimization is performed to maximize the return percentage.

5. **Moon Dev-Themed Debug Prints**:
   - Debug prints are added to track entry/exit signals and other important events.

6. **Backtest Execution**:
   - The initial backtest is run with default parameters.
   - Optimization is performed, and the backtest is rerun with the optimized parameters.
   - Performance plots are displayed for both the initial and optimized backtests.

---

Let me know if you need further refinements or additional features! 🌙✨🚀