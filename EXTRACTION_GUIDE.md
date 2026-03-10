# Step-by-Step Code Extraction Guide

## Overview
This guide shows how to extract code from the original notebooks and refactor it into the modular structure.

## Phase 1: Extract Configuration ✅ DONE

### What was done:
Created `portfolio_config.py` with:
- Signal configurations for different variants (1.0x, 1.5x)
- ETF universes specific to each variant
- Bond ETF lists (same for all variants)
- `get_signal_config()` function to retrieve configs

## Phase 2: Extract Core Engine Logic (IN PROGRESS)

### What to extract:
The large code cell (lines 5-5227) from the original notebooks should be refactored into `portfolio_engine.py`.

### How to do it:

#### Step 2.1: Get the original code
1. Open `Portfolio_1_0xLong.ipynb` in a text editor
2. Find the first non-markdown code cell (around line 5-5227)
3. Copy the entire cell content

#### Step 2.2: Identify sections in the code
The code likely contains these sections (in this order):

**Section A: Imports & Constants**
```python
# import statements
import pandas as pd
import numpy as np
import requests
# ... more imports

POLYGON_API_KEY = "..."  # Keep this
```

**Section B: Data Loading**
```python
def fetch_data_from_polygon(symbols, start_date, end_date):
    # API calls to get OHLCV data
    # Returns DataFrame

def preprocess_data(df):
    # Clean, align, handle missing data
    # Returns cleaned DataFrame
```

**Section C: Signal Generation**
```python
def calculate_momentum(prices):
    # Calculate momentum signals
    pass

def calculate_mean_reversion(prices):
    # Calculate mean reversion signals
    pass

def combine_signals(momentum, mean_reversion):
    # Combine multiple signals
    pass
```

**Section D: Portfolio Construction & Backtesting**
```python
def calculate_positions(signals, leverage=1.0):
    # Position sizing based on signals
    # Apply leverage here
    pass

def calculate_pnl(prices, positions):
    # Calculate P&L from positions
    pass

def backtest_strategy(data, signals):
    # Full backtest simulation
    pass
```

**Section E: Analysis & Metrics**
```python
def calculate_sharpe_ratio(returns):
    pass

def calculate_sortino_ratio(returns):
    pass

def generate_metrics(returns):
    # All performance calculations
    pass
```

**Section F: Visualization Preparation**
```python
def prepare_equity_curve(returns):
    pass

def prepare_drawdown_chart(returns):
    pass
```

#### Step 2.3: Refactor each section

**For Section A (Imports):**
- Keep all imports at the top of `portfolio_engine.py`
- Move API key to a config or environment variable (don't hardcode)

**For Section B (Data Loading):**
```python
# IN portfolio_engine.py

def load_data(self) -> pd.DataFrame:
    """Load OHLCV data for all ETFs in self.etf_universe"""
    # PASTE the data loading code here
    # Change: ETF_UNIVERSE → self.etf_universe
    # Change: hardcoded dates → function parameters
    
    # Example conversion:
    # BEFORE:  for symbol in ETF_UNIVERSE:
    # AFTER:   for symbol in self.etf_universe:
    
    data = {}
    for symbol in self.etf_universe:
        df = fetch_data_from_polygon(
            symbol,
            start_date="2020-01-01",
            end_date="2024-01-01"
        )
        data[symbol] = df
    
    return combine_dataframes(data)
```

**For Section C (Signals):**
```python
def generate_signals(self) -> pd.DataFrame:
    """Generate signals for all ETFs in portfolio"""
    # PASTE signal generation code here
    # Change: global ETF_UNIVERSE → self.etf_universe
    # Change: global BOND → self.bond_etfs
    
    signals = {}
    for symbol in self.etf_universe:
        momentum = calculate_momentum(self.data[symbol])
        mean_rev = calculate_mean_reversion(self.data[symbol])
        signals[symbol] = combine_signals(momentum, mean_rev)
    
    return pd.DataFrame(signals)
```

**For Section D (Backtesting):**
```python
def run_backtest(self, data: pd.DataFrame, signals: pd.DataFrame) -> Dict:
    """Run backtest with leverage applied"""
    # PASTE backtesting code here
    # Change: leverage hardcoded as 1.0 → self.leverage
    
    positions = calculate_positions(signals, leverage=self.leverage)
    returns = calculate_pnl(data, positions)
    
    return {
        'positions': positions,
        'returns': returns,
        'equity_curve': (1 + returns).cumprod()
    }
```

**For Section E (Metrics):**
```python
def calculate_metrics(self, returns: pd.Series) -> Dict[str, float]:
    """Calculate all performance metrics"""
    # PASTE metric calculation code here
    
    sharpe = calculate_sharpe_ratio(returns)
    sortino = calculate_sortino_ratio(returns)
    max_dd = calculate_max_drawdown(returns)
    
    return {
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'max_drawdown': max_dd,
        # ... other metrics
    }
```

**For Section F (Visualizations):**
- These can stay in the notebook for now
- OR extract to `portfolio_engine.py` and import in notebook
- Recommended: Extract to notebook cell that calls `prepare_*` functions

#### Step 2.4: Handle global variables

**Find & Replace Pattern:**
```
BEFORE:              AFTER:
ETF_UNIVERSE    →    self.etf_universe
BOND            →    self.bond_etfs
LEVERAGE_FACTOR →    self.leverage
```

**Common conversions:**
```python
# BEFORE (in notebook):
for etf in ETF_UNIVERSE:
    process(etf)

# AFTER (in engine):
def some_function(self):
    for etf in self.etf_universe:
        process(etf)
```

#### Step 2.5: Extract visualization code

All plot/visualization code should be separated:

**Option A: Keep in notebook**
```python
# Notebook Cell
from portfolio_engine import run_portfolio_analysis
import matplotlib.pyplot as plt

config = get_signal_config('1.0x_long')
results = run_portfolio_analysis(config)

# Visualizations (from original notebook, unchanged)
equity = results['backtest']['equity_curve']
plt.plot(equity)
plt.title(f"{config['name']} Equity Curve")
plt.show()
```

**Option B: Extract visualization helpers**
```python
# In portfolio_engine.py
def plot_equity_curve(results):
    equity = results['backtest']['equity_curve']
    plt.plot(equity)
    plt.title(f"{results['config']['name']} Equity Curve")
    return plt

# In notebook
from portfolio_engine import run_portfolio_analysis, plot_equity_curve
results = run_portfolio_analysis(config)
plot_equity_curve(results)
```

#### Step 2.6: Test the extracted code

Test that results match original:
```python
# In test script or notebook:
from portfolio_config import get_signal_config
from portfolio_engine import run_portfolio_analysis

# Load 1.0x config
config = get_signal_config('1.0x_long')
results = run_portfolio_analysis(config)

# Verify metrics match original notebook output
original_sharpe = 1.148404  # From original notebook
new_sharpe = results['metrics']['sharpe_ratio']

assert abs(original_sharpe - new_sharpe) < 0.0001, "Metrics don't match!"
print("✓ Results match original!")

# Repeat for 1.5x variant
config = get_signal_config('1.5x_long')
results = run_portfolio_analysis(config)
# ... verify metrics ...
```

## Phase 3: Refactor Notebooks

### Create minimal notebook structure:

**Cell 1: Setup & Imports**
```python
# Portfolio 1.0x Long
from portfolio_config import get_signal_config
from portfolio_engine import run_portfolio_analysis
import matplotlib.pyplot as plt
import pandas as pd

# Configuration
config = get_signal_config('1.0x_long')
print(f"Analyzing: {config['name']}")
print(f"ETFs: {len(config['etf_universe'])}")
```

**Cell 2: Run Analysis**
```python
# Run full analysis
results = run_portfolio_analysis(config)

# Extract results
metrics = results['metrics']
backtest = results['backtest']
equity_curve = backtest['equity_curve']

print(f"\nSharpe Ratio: {metrics['sharpe_ratio']:.4f}")
print(f"Sortino Ratio: {metrics['sortino_ratio']:.4f}")
print(f"Max Drawdown: {metrics['max_drawdown']:.4f}")
```

**Cell 3+: Visualizations**
```python
# All the plotting code from the original notebook
# These visualization cells can be copied as-is from original

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Equity curve
axes[0, 0].plot(equity_curve.index, equity_curve)
axes[0, 0].set_title("Equity Curve")

# Other plots...
```

### Create 1.5x variant notebook:
Simply change line 1 in Cell 1:
```python
config = get_signal_config('1.5x_long')  # Changed from 1.0x_long
```

All other cells are identical!

## File Size Reduction

### Before Modularization:
- Portfolio_1_0xLong.ipynb: ~5000 lines
- Portfolio_1_5xLong.ipynb: ~5000 lines  
- Quanta_W7.ipynb: ~5000 lines (if duplicated)
- **Total: ~15,000 lines of duplicated code**

### After Modularization:
- portfolio_config.py: ~100 lines
- portfolio_engine.py: ~500-1000 lines (extracted from notebooks)
- Portfolio_1_0xLong.ipynb: ~1000 lines (visualization only)
- Portfolio_1_5xLong.ipynb: ~1000 lines (visualization only, mostly identical)
- Quanta_W7.ipynb: Reuses the above modules
- **Total: ~3000-4000 lines (75% reduction!)**

## Checkbox for Completion

- [ ] **Phase 1**: Configuration extracted (✅ DONE)
- [ ] **Phase 2a**: Extract data loading to `portfolio_engine.py`
- [ ] **Phase 2b**: Extract signal generation to `portfolio_engine.py`
- [ ] **Phase 2c**: Extract backtesting to `portfolio_engine.py`
- [ ] **Phase 2d**: Extract metrics calculation to `portfolio_engine.py`
- [ ] **Phase 2e**: Test extracted code matches original results
- [ ] **Phase 3a**: Refactor `Portfolio_1_0xLong.ipynb`
- [ ] **Phase 3b**: Refactor `Portfolio_1_5xLong.ipynb`
- [ ] **Phase 3c**: Test both notebooks produce same results as originals
- [ ] **Phase 4**: Add new signal variants by editing only `portfolio_config.py`

## Troubleshooting

**Issue**: "Results don't match original"
- **Solution**: Check that you haven't changed the actual calculation logic
- Search for any hardcoded values that should use `self.leverage` or `self.etf_universe`

**Issue**: "Missing data for some ETFs"
- **Solution**: Verify that the API key is correct and rate limits aren't being hit
- The extracted code should use the same data source and date ranges as original

**Issue**: "Import errors in notebook"
- **Solution**: Make sure `portfolio_config.py` and `portfolio_engine.py` are in the same directory as the notebooks
- Or update the import path: `from .portfolio_config import ...`
