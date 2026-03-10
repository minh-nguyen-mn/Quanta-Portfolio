# Quanta Portfolio

Systematic ETF portfolio backtesting framework with modular signals, ETF universe management, and cached data loading.

The system supports running multiple portfolios individually or in combination while sharing the same data pipeline and cache.

---

# Features

- Modular signal architecture
- ETF universe abstraction
- Local data caching (avoids repeated downloads)
- Train / Validation / Blind / Live evaluation splits
- Portfolio-level and combined portfolio backtests
- PnL correlation matrices
- Configurable leverage
- Reproducible CLI execution

---

# Portfolio Structure

The framework currently supports three portfolio modes:

| Mode | Description |
|-----|-------------|
| `1.0` | Base portfolio |
| `1.5` | Higher leverage portfolio |
| `combo` | Equal-weight combination of 1.0 and 1.5 portfolios |

Each portfolio has its own:

- signal set
- ETF universe
- leverage configuration

---

# Data Periods

The backtest uses the following dataset splits:

| Period | Date Range | Purpose |
|------|-------------|--------|
| Train | 2000-01-01 → 2015-12-31 | Model development |
| Validation | 2016-01-01 → 2021-12-31 | Out-of-sample testing |
| Blind | 2022-01-01 → 2025-06-30 | Unseen historical data |
| Live | 2026-01-01 → present | Real forward period |

**Important**

The live period shown in examples currently uses **only the first two months of 2026**.

```
LIVE OUT-OF-SAMPLE
2026-01-01 → 2026-03-01
```

This window will automatically extend as new data becomes available.

---

# Installation

Clone the repository:

```
git clone https://github.com/minh-nguyen-mn/Quanta-Portfolio.git
cd Quanta-Portfolio
```

---

# Running the Backtest

## Run 1.0 Portfolio

```
python run_portfolio.py 1.0
```

## Run 1.5 Portfolio

```
python run_portfolio.py 1.5
```

## Run Combined Portfolio

```
python run_portfolio.py combo
```

This runs:

- Portfolio 1.0
- Portfolio 1.5
- Equal-weight combination

---

# Data Cache

ETF price data is cached locally to avoid repeated downloads.

Cached files are stored in:

```
data_cache/
```

When the program runs:

```
✓ Cache hits   (232)
↓ Fetched new (...)
```

### Force Reload Cache

```
python run_portfolio.py combo --clear-cache
```

This deletes cached files and downloads fresh data.

---

# Performance Metrics

The framework reports:

| Metric | Meaning |
|------|--------|
| Sharpe Ratio | Risk-adjusted return |
| CAGR | Compound annual growth rate |
| Max Drawdown | Largest peak-to-trough loss |
| Absolute Return | Return during live period |
| Final Equity | Ending equity multiple |

Example:

```
Absolute Return: 0.0521
Final Equity:    1.0521
```

Meaning:

- Portfolio gained **5.21%**
- $1 → **$1.0521**

---

# Example Output

Example command:

```
python run_portfolio.py combo
```

Example output:

```
======================================================================
Cache reload: NO
======================================================================

Loading ETF universe (232 ETFs) ...

Loading ETF data...

✓ Cache hits   (232): ['AAXJ', 'ACWX', 'AGG', 'AGQ', 'AIA']...

Running combined portfolio (1.0x + 1.5x equal weight)


======================================================================
PORTFOLIO 1.0x
======================================================================
Configuration: 19 signals, 230 ETFs
======================================================================

RESULTS

TRAIN PERIOD                   (2000-01-01 to 2015-12-31)
  Sharpe Ratio:         3.9893
  CAGR:                 0.1536
  Max Drawdown:        -0.0178

VALIDATION PERIOD              (2016-01-01 to 2021-12-31)
  Sharpe Ratio:         3.9960
  CAGR:                 0.1062
  Max Drawdown:        -0.0119

BLIND PERIOD                   (2022-01-01 to 2025-06-30)
  Sharpe Ratio:         2.7426
  CAGR:                 0.0631
  Max Drawdown:        -0.0147

LIVE OUT-OF-SAMPLE             (2026-01-01 to 2026-03-01)
  Sharpe Ratio:         1.9878
  CAGR:                 0.0412
  Max Drawdown:        -0.0047

TRAIN + VALIDATION
  Sharpe Ratio:         3.9420

FULL PERIOD
  Sharpe Ratio:         3.6935

LIVE RETURN
  Absolute Return:       0.0063
  Final Equity:          1.0063

SUMMARY
  Signals Used:    19
  ETFs Used:       230
  Total Return:         12.1673
  Final Drawdown:       -0.0133


======================================================================
PORTFOLIO 1.5x
======================================================================
Configuration: 11 signals, 142 ETFs
======================================================================

RESULTS

TRAIN PERIOD                   (2000-01-01 to 2015-12-31)
  Sharpe Ratio:         3.1921
  CAGR:                 0.2283
  Max Drawdown:        -0.0608

VALIDATION PERIOD              (2016-01-01 to 2021-12-31)
  Sharpe Ratio:         2.9778
  CAGR:                 0.1805
  Max Drawdown:        -0.0782

BLIND PERIOD                   (2022-01-01 to 2025-06-30)
  Sharpe Ratio:         2.0495
  CAGR:                 0.1272
  Max Drawdown:        -0.0769

LIVE OUT-OF-SAMPLE             (2026-01-01 to 2026-03-01)
  Sharpe Ratio:         4.0842
  CAGR:                 0.3886
  Max Drawdown:        -0.0222

TRAIN + VALIDATION
  Sharpe Ratio:         3.1214

FULL PERIOD
  Sharpe Ratio:         2.9360

LIVE RETURN
  Absolute Return:       0.0521
  Final Equity:          1.0521

SUMMARY
  Signals Used:    11
  ETFs Used:       142
  Total Return:         55.0097
  Final Drawdown:        0.0000


======================================================================
COMBINED PORTFOLIO (1.0x + 1.5x)
======================================================================
Configuration: 30 signals, 232 ETFs
======================================================================

RESULTS

TRAIN PERIOD                   (2000-01-01 to 2015-12-31)
  Sharpe Ratio:         3.8851
  CAGR:                 0.1908
  Max Drawdown:        -0.0271

VALIDATION PERIOD              (2016-01-01 to 2021-12-31)
  Sharpe Ratio:         3.8417
  CAGR:                 0.1431
  Max Drawdown:        -0.0352

BLIND PERIOD                   (2022-01-01 to 2025-06-30)
  Sharpe Ratio:         2.5383
  CAGR:                 0.0951
  Max Drawdown:        -0.0437

LIVE OUT-OF-SAMPLE             (2026-01-01 to 2026-03-01)
  Sharpe Ratio:         3.9650
  CAGR:                 0.2032
  Max Drawdown:        -0.0120

TRAIN + VALIDATION
  Sharpe Ratio:         3.8466

FULL PERIOD
  Sharpe Ratio:         3.6083

LIVE RETURN
  Absolute Return:       0.0290
  Final Equity:          1.0290

SUMMARY
  Signals Used:    30
  ETFs Used:       232
  Total Return:         26.3733
  Final Drawdown:       -0.0001
```

---

# Notes

- PnL values represent **daily portfolio returns**.
- Total return is the **equity multiple minus 1** over the full backtest period.
- Live performance will evolve as more real data becomes available.

---

# License

MIT License
