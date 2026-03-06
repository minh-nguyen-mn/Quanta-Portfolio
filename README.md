# Portfolio Optimization Framework

This repository contains a quantitative research framework for developing and validating systematic ETF trading strategies. The framework focuses on building robust alpha signals through a structured pipeline emphasizing cross-asset testing, independent signal validation, and conservative portfolio construction.

The core philosophy is to **build many diversified long-short alpha signals first, validate them individually, and only then combine them into a portfolio**, rather than optimizing directly at the portfolio level.

---

# Research Philosophy

The strategy is designed around several key principles:

- **Signal-first research** rather than portfolio-first optimization
- **Cross-asset robustness testing** to avoid asset-specific overfitting
- **Independent signal validation** before aggregation
- **Neutral long–short construction** to isolate alpha from market beta
- **Low signal correlation** to maximize diversification
- **Minimal reliance on leverage**

This structure improves generalization and ensures that each signal contributes meaningful standalone alpha.

---

# 1. Data Loading and Configuration

## API Access

`POLYGON_API_KEY` is required to fetch historical ETF data from Polygon.io.

The key should be securely stored before running the notebook.

---

## ETF Universe

`ETF_UNIVERSE` defines the set of ETFs used for signal discovery and portfolio construction.

Signals are tested **across the full ETF universe first**, rather than tuned for individual assets. This prevents asset-specific overfitting and ensures signals capture broader structural effects.

---

## Backtesting Periods

The backtest is segmented into three periods:

- **Train:** Signal development and preliminary filtering  
- **Validation:** Robustness confirmation and model selection  
- **Blind (Out-of-Sample):** Final performance evaluation

```
TRAIN_START / TRAIN_END
VAL_START / VAL_END
BLIND_START / BLIND_END
```

---

## Data Sources

`fetch_etf()` retrieves daily ETF data including:

- Open
- High
- Low
- Close
- Volume
- Returns

`fetch_vix()` retrieves VIX data for market regime analysis.

`SPY` is loaded separately to serve as a **market benchmark and regime reference**.

---

# 2. Core Signal Operators

Signals are built using reusable time-series operators.

## Time-Series Functions

| Function | Description |
|--------|-------------|
| `ts_rank(x, window)` | Rank of the most recent value within a rolling window |
| `ts_argmin(x, window)` | Index of minimum value within a rolling window |
| `ts_mad(x, window)` | Mean absolute deviation |
| `ts_percentile(x, window, p)` | Rolling percentile |
| `volatility(x, window)` | Rolling standard deviation |
| `ts_mscore(x, window)` | Momentum-style score |

---

## Signal Transformations

| Function | Purpose |
|--------|---------|
| `scale_signal(x, cap)` | Caps signal leverage |
| `apply_decay(signal, decay_days, mode)` | Applies time decay to signals |

These transformations ensure signals remain **stable, interpretable, and point-in-time safe**.

---

# 3. Signal Development Framework

Signals are defined using a modular registration system:

```python
@register_signal
def signal_name(df):
```

Each signal is automatically added to `_SIGNAL_REGISTRY`, allowing the research framework to test signals systematically.

Signals typically output:

```
-1  -> Short
0   -> Neutral
+1  -> Long
```

---

# 4. Cross-ETF Signal Evaluation

Unlike traditional workflows that tune signals per asset, this framework evaluates signals **across the entire ETF universe first**.

### Process

1. Generate the signal across all ETFs.
2. Evaluate aggregate signal behavior.
3. Apply robustness checks across Train and Validation periods.

Signals that fail robustness tests are discarded before portfolio construction.

This approach significantly reduces the risk of **data-mining individual assets**.

---

# 5. ETF Compatibility Filtering

Once a signal passes aggregate validation, the ETF universe is filtered to identify **instruments that are structurally compatible with that signal**.

### Filtering Process

1. Evaluate profitability per ETF.
2. Retain only ETFs with **positive risk-adjusted performance**.
3. Iteratively remove weak instruments until the remaining set demonstrates consistent profitability.

This produces a **signal-specific ETF universe**, ensuring the signal is only applied where it behaves reliably.

---

# 6. Signal Portfolio Construction

Each signal is constructed as its own **long–short ETF portfolio**.

### Portfolio Structure

- Long exposure: selected ETFs with positive signal
- Short exposure: selected ETFs with negative signal
- Market-neutral orientation
- Controlled leverage

Each signal portfolio is required to independently demonstrate stable performance across both Train and Validation periods before inclusion.

This design ensures that **every signal component contributes real alpha**.

---

# 7. Robustness Testing Pipeline

Every signal portfolio undergoes a comprehensive validation process.

## Leave-One-Out (LOO)

Signals are removed one at a time to ensure the portfolio does not rely excessively on any single component.

---

## Signal Correlation Analysis

Signal portfolio returns are analyzed for correlation.

Low to moderate correlations indicate effective diversification across signals.

---

## Transaction Cost Sensitivity

Performance is tested under multiple transaction cost assumptions to ensure profitability remains realistic.

---

## Next-Day Execution Testing

Signals are evaluated using next-day open execution to simulate realistic trading conditions and eliminate lookahead bias.

---

## Market Regime Testing

Performance is evaluated across different market regimes:

- Bull markets
- Bear markets
- Sideways markets
- High volatility environments
- Low volatility environments

Robust signals should remain stable across regimes rather than depending on a single market condition.

---

# 8. Portfolio Construction

Once signals pass validation, they are combined into a single strategy.

Current aggregation uses **equal-weighted averaging of signal portfolios**.

This approach avoids introducing unnecessary parameter tuning and reduces overfitting risk.

The design emphasizes:

- signal independence
- diversification
- robustness

Future weighting methods may incorporate:

- volatility scaling
- Sharpe-based weighting
- correlation-aware allocation

---

# 9. Leverage Philosophy

The strategy prioritizes **portable alpha rather than leverage-driven returns**.

Long-short signals are designed to generate returns independently of market beta. Portfolio construction therefore focuses on stacking diversified alpha sources instead of increasing leverage.

This improves stability and reduces sensitivity to market regimes.

---

# 10. Performance Evaluation

The framework tracks several core metrics:

- Sharpe Ratio
- CAGR
- Maximum Drawdown
- Turnover
- Margin usage

Performance is evaluated separately across:

- Train
- Validation
- Blind (Out-of-Sample)

Strong strategies should demonstrate **consistent behavior across all splits**.

---

# 11. Equity Curve Visualization

The framework generates cumulative return plots for:

- individual signal portfolios
- the combined strategy
- benchmark comparisons

These visualizations help assess stability and drawdown behavior over time.

---

# 12. Strategy Architecture Summary

The research pipeline follows this structure:

```
Signal Research
      ↓
Cross-ETF Testing
      ↓
Robustness Validation
      ↓
ETF Compatibility Filtering
      ↓
Signal-Level Portfolio Construction
      ↓
Signal Robustness Testing
      ↓
Equal-Weight Signal Aggregation
      ↓
Final Portfolio
```

This layered validation process ensures that:

- each signal works independently
- the portfolio is diversified
- overfitting is minimized
- out-of-sample reliability is improved

---

# Conclusion

This framework provides a structured environment for developing robust ETF trading strategies.

Key design principles include:

- cross-asset signal discovery
- signal-level portfolio construction
- rigorous robustness validation
- diversified alpha stacking
- minimal reliance on leverage

By validating each component independently before aggregation, the strategy aims to achieve **stable and generalizable performance across market conditions**.
