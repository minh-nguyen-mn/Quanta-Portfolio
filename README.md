# Portfolio Optimization Framework

This repository contains a quantitative trading research framework for developing and evaluating ETF-based systematic strategies. The framework focuses on signal generation, dynamic portfolio construction, ETF universe selection, and rigorous robustness testing.

---

# 1. Data Loading and Configuration

## API Access

`POLYGON_API_KEY` is required to fetch historical ETF data from Polygon.io.  
The key should be securely stored and accessible before running the notebook.

## ETF Universe

`ETF_UNIVERSE` defines the set of ETFs used in the strategy.  
The chosen universe significantly impacts performance metrics and portfolio behavior.

## Backtesting Periods

The backtest is segmented into three periods:

- **Train:** Model development and parameter tuning  
- **Validation:** Strategy evaluation and filtering  
- **Blind (Out-of-Sample):** Final performance test  

```
TRAIN_START / TRAIN_END
VAL_START / VAL_END
BLIND_START / BLIND_END
```

## Data Sources

`fetch_etf()` retrieves daily ETF data including:

- Open
- High
- Low
- Close
- Volume
- Returns

`fetch_vix()` retrieves VIX data from FRED for regime analysis.

`SPY` is loaded separately to serve as:

- Market benchmark
- Market regime filter

---

# 2. Core Signal Operators

Several custom time-series operators are used as building blocks for signals.

## Time-Series Functions

| Function | Description |
|--------|-------------|
| `ts_rank(x, window)` | Rank of the most recent value within a rolling window |
| `ts_argmin(x, window)` | Index of minimum value in a rolling window |
| `ts_mad(x, window)` | Mean Absolute Deviation |
| `ts_percentile(x, window, p)` | Rolling percentile |
| `volatility(x, window)` | Rolling standard deviation |
| `ts_mscore(x, window)` | Momentum-style score |

## Signal Transformations

| Function | Purpose |
|--------|---------|
| `scale_signal(x, cap)` | Caps signal leverage (e.g., ±1.5) |
| `apply_decay(signal, decay_days, mode)` | Applies linear or exponential decay to signals |

These operators ensure signals remain **stable, interpretable, and point-in-time safe**.

---

# 3. Signal Generation

Signals attempt to predict future ETF returns.

## Signal Registration

Signals are defined using a decorator:

```python
@register_signal
def signal_name(df):
```

This automatically registers signals in `_SIGNAL_REGISTRY`, allowing the backtest to dynamically apply all active signals.

## Example Signal Output

Signals typically output:

```
-1  -> Short
0   -> Neutral
+1  -> Long
```

## Signal Development Workflow

1. **Develop a single signal**
2. **Test it individually**
3. Evaluate performance across:
   - Train
   - Validation
   - Blind
4. **Iteratively refine parameters**

This workflow helps reduce **overfitting risk**.

---

# 4. Signal Combination

Multiple signals can be combined using `combine_signals()`.

Supported combination modes include:

| Mode | Description |
|-----|-------------|
| `equal` | Average of raw signals |
| `rank` | Rank-based aggregation |
| `zscore` | Standardized signal averaging |
| `vol_scaled` | Inverse-volatility weighting |
| `ic_weighted` | Weighted by rolling Information Coefficient |

A more advanced setup allows mapping specific signals to specific ETFs for tailored strategies.

---

# 5. Dynamic Position Sizing

Portfolio construction is handled by:

```
build_long_short_portfolio()
```

This function allocates capital across ETFs based on combined signals.

## Exposure Constraints

- `long_leverage` controls long exposure (e.g., 1.5)
- `short_leverage` controls short exposure (e.g., 1.0)

Positions are clipped to remain within these leverage limits.

## Portfolio Weighting Modes

Weights across ETFs can be assigned using:

| Mode | Description |
|-----|-------------|
| `equal` | Equal weights |
| `rank` | Signal rank weighting |
| `zscore` | Standardized signals |
| `vol_scaled` | Volatility-adjusted weights |
| `ic_weighted` | Information coefficient weighting |

---

# 6. ETF Filtering and Universe Selection

The ETF universe strongly affects strategy results.

## Performance Table

After backtesting, a table is generated containing:

- Sharpe Ratio
- CAGR
- Max Drawdown
- Turnover
- Margin usage

Metrics are calculated across:

- Train
- Validation
- Blind

## ETF Filtering

A filtered set of ETFs is selected using criteria such as:

```
Sharpe_Train > 0
Sharpe_Val > 0
AlphaSharpe_Train > 0
AlphaSharpe_Val > 0
```

Only ETFs that satisfy these conditions form the filtered list:

```
passed_etfs
```

Researchers may replace the original ETF universe with this filtered set and rerun the backtest.

---

# 7. Impact of ETF Universe Selection

Changing the ETF universe affects performance metrics for several reasons.

## Portfolio Context

Different ETFs contribute differently to portfolio PnL.

## Cross-Sectional Ranking

Signals using ranking behave differently depending on universe size.

## Benchmark Changes

The equally-weighted buy-and-hold benchmark changes when the ETF universe changes.

As a result, the following may change dynamically:

- Sharpe ratios
- Alpha Sharpe
- Signal rankings
- Portfolio allocations

---

# 8. Robustness Testing

The framework includes several tests to validate strategy stability.

## Train / Validation / Blind Testing

A standard approach used to prevent overfitting.

## Leave-One-Out (LOO) Analysis

Removes one signal at a time to measure its contribution to portfolio performance.

## Signal Correlation Analysis

Measures correlation between signal PnLs.

This helps detect:

- redundant signals
- diversification benefits

## Transaction Cost Analysis

Validation Sharpe is tested under different transaction cost assumptions:

- 1 bps
- 5 bps
- 10 bps
- 20 bps

This provides a more realistic profitability estimate.

## Next-Day Open Execution

Performance is evaluated using next-day open prices to simulate realistic trade execution and avoid lookahead bias.

## Market Regime Testing

Strategy performance is tested under different market regimes:

- Bull markets
- Bear markets
- Sideways markets
- High VIX environments
- Low VIX environments

## Leverage Stress Test

Sensitivity to leverage caps is tested, such as:

```
1.0x
1.5x
```

---

# 9. Performance Metrics

Key metrics tracked include:

- Sharpe Ratio
- Alpha Sharpe
- CAGR
- Max Drawdown
- Turnover
- Margin Usage

These metrics provide insight into both performance and risk.

---

# 10. Equity Curve Visualization

The framework generates cumulative return plots for:

- Strategy equity curve
- Equally-weighted ETF benchmark

This helps visualize long-term performance behavior.

---

# 11. Optional PnL Simulation

An optional module converts returns into dollar PnL using a specified book size.

Example:

```
BOOK_SIZE = $20M
```

This produces a cumulative dollar profit curve.

---

# Conclusion

This framework provides a comprehensive environment for developing and evaluating quantitative ETF strategies.

Key features include:

- Modular signal generation
- Dynamic portfolio construction
- ETF universe optimization
- Robust out-of-sample testing
- Extensive robustness diagnostics

By systematically combining these components, researchers can develop and validate robust systematic trading strategies.
