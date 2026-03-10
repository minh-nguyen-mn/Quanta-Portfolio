# ETF Long–Short Signal Portfolio

This project implements a **systematic multi-signal long–short ETF portfolio** designed to generate **robust and diversified alpha across market regimes**.

Rather than relying on a single predictive model, the system stacks **many independently validated signals**, each implemented as its own **long–short sub-portfolio**, and aggregates them into a unified portfolio.

The core philosophy is **signal diversification**:

- every signal must work independently  
- signals must generalize across datasets  
- signals must remain stable when combined  

This avoids dependence on any single alpha source and produces a **robust systematic portfolio**.

---

# Strategy Overview

The portfolio is constructed using **cross-sectional ETF signals** applied to a broad universe of global ETFs.

Key properties:

- Multi-signal architecture  
- Cross-asset ETF universe  
- Long–short construction  
- Equal-weight signal aggregation  
- Extensive out-of-sample validation  

Each signal produces its own **long–short portfolio**, which is then aggregated into the final strategy.

---

# ETF Universe

The system operates on a **large cross-section of 232 ETFs**, spanning multiple asset classes:

- global equities  
- sector ETFs  
- fixed income  
- commodities  
- volatility proxies  
- leveraged ETFs  
- international markets  

Example ETFs include:

SPY, QQQ, EWJ, FXI, XLV, XLP, VNQ, GLD, GDX, SOXX, TLT, HYG, AGG, IWM, EEM, EWZ, ITB, VGT, XLE, XBI

A large ETF universe improves:

- cross-sectional signal power  
- diversification  
- robustness across regimes  

---

# Code Architecture

The project is structured into modular components.

```
Quanta-Portfolio/

run_portfolio.py
portfolio_engine.py
signals/
    __init__.py
    signal_*.py
data_cache/
README.md
```

## run_portfolio.py

Main entry point for the system.

Responsibilities:

- CLI interface  
- portfolio configuration  
- ETF universe construction  
- data loading  
- running portfolio backtests  
- computing performance metrics  
- printing results  

---

## portfolio_engine.py

Core backtesting engine.

Handles:

- signal evaluation  
- long/short portfolio construction  
- leverage control  
- daily PnL computation  
- Sharpe / CAGR / drawdown metrics  

---

## signals/

Contains **all signal implementations**.

Signals are registered through:

```python
_SIGNAL_REGISTRY
```

This allows the portfolio to dynamically map **signal names → signal functions**.

---

# Portfolio Configurations

Two portfolio structures are implemented.

---

## 1. Market Neutral Portfolio (1.0x)

Long leverage = **1.0**  
Short leverage = **1.0**

Configuration:

- **19 signals**
- **230 ETFs**

Goal:

Capture **pure alpha** with minimal market exposure.

---

## 2. Long-Biased Portfolio (1.5x)

Long leverage = **1.5**  
Short leverage = **1.0**

Configuration:

- **11 signals**
- **142 ETFs**

Goal:

Combine signal alpha with **equity risk premium**.

---

## 3. Combined Portfolio

The combined strategy equally weights both portfolios.

```
Combined = 0.5 × (1.0x portfolio)
         + 0.5 × (1.5x portfolio)
```

Configuration:

- **30 signals**
- **232 ETFs**

This increases diversification and improves robustness.

---

# Dataset Splits

Performance is evaluated across multiple datasets.

| Period | Range |
|------|------|
| Train | 2000-01-01 → 2015-12-31 |
| Validation | 2016-01-01 → 2021-12-31 |
| Blind | 2022-01-01 → 2025-06-30 |
| Live OOS | 2026-01-01 → present |

The **Live OOS period updates automatically** whenever the portfolio is run.

---

# Running the Portfolio

The portfolio is executed from the command line.

## Run Market Neutral Portfolio

```bash
python run_portfolio.py 1.0
```

Runs:

- 19 signals  
- 230 ETFs  
- 1.0 / 1.0 leverage  

---

## Run Long-Biased Portfolio

```bash
python run_portfolio.py 1.5
```

Runs:

- 11 signals  
- 142 ETFs  
- 1.5 / 1.0 leverage  

---

## Run Combined Portfolio

```bash
python run_portfolio.py combo
```

Runs:

1. Market neutral portfolio  
2. Long-biased portfolio  
3. Combined portfolio  

---

## Force Reload ETF Data

ETF data is cached locally.

To force a full reload:

```bash
python run_portfolio.py combo --reload
```

---

# ETF Data Caching

ETF price data is cached locally to avoid repeated downloads.

Example console output:

```
Loading ETF universe (232 ETFs) ...

Loading ETF data...

✓ Cache hits   (232): ['AAXJ', 'ACWX', 'AGG', 'AGQ', 'AIA']...
```

This means all ETF price data was loaded from cache instead of downloading again.

---

# Example Console Output

```
PS D:\Quanta-Portfolio> python run_portfolio.py combo
```

```
======================================================================
Cache reload: NO
======================================================================

Loading ETF universe (232 ETFs) ...

Loading ETF data...

✓ Cache hits   (232): ['AAXJ', 'ACWX', 'AGG', 'AGQ', 'AIA']...

Running combined portfolio (1.0x + 1.5x equal weight)
```

---

# Example Results (Early Live Period Illustration)

The live out-of-sample period begins in **2026**.

The results shown below are **only an early illustration using the first ~2 months of live data** and should **not be interpreted as long-term live performance**.

As time progresses, the live statistics will automatically update when the portfolio is re-run.

Example evaluation window:

```
2026-01-01 → 2026-03-01
```

Because this sample period is short, live Sharpe ratios and returns may fluctuate significantly.

---

# Market Neutral Portfolio (1.0x)

Configuration:

- 19 signals  
- 230 ETFs  

| Period | Sharpe |
|------|------|
| Train | 3.99 |
| Validation | 4.00 |
| Blind | 2.74 |
| Live (early sample) | 1.99 |
| Full | 3.69 |

Example early live performance:

```
Absolute Return: 0.63%
Final Equity:    1.0063
```

---

# Long-Biased Portfolio (1.5x)

Configuration:

- 11 signals  
- 142 ETFs  

| Period | Sharpe |
|------|------|
| Train | 3.19 |
| Validation | 2.98 |
| Blind | 2.05 |
| Live (early sample) | 4.08 |
| Full | 2.94 |

Example early live performance:

```
Absolute Return: 5.21%
Final Equity:    1.0521
```

---

# Combined Portfolio

Configuration:

- 30 signals  
- 232 ETFs  

| Period | Sharpe |
|------|------|
| Train | 3.89 |
| Validation | 3.84 |
| Blind | 2.54 |
| Live (early sample) | 3.97 |
| Full | 3.61 |

Example early live performance:

```
Absolute Return: 2.90%
Final Equity:    1.0290
```

---

# Important Note

The **live out-of-sample period started in 2026**, so current results only reflect **a very short observation window**.

These numbers are included purely as an **example of how the system reports live performance**, and will evolve as additional data accumulates.

Longer live evaluation periods are necessary before drawing meaningful conclusions about real-world performance.

---

# Signal Architecture

Signals capture diverse market effects including:

- entropy of price movement  
- volatility compression  
- autocorrelation structure  
- liquidity persistence  
- price-volume interaction  
- record rates  
- burstiness  
- path efficiency  

Example signals:

```
signal_entropy
signal_autocorr
signal_burstiness
signal_record_rate
signal_vol_compression_ratio
signal_return_conviction
signal_price_volume_phase
signal_liquidity_persistence
signal_run_length
signal_signed_volume_agreement
```

Each signal is validated individually before inclusion.

---

# Signal Validation

Signals must pass strict criteria:

- Sharpe ≥ **1.0** in Train and Validation  
- consistent performance across regimes  
- low correlation with existing signals  
- stability under leave-one-out testing  
- robustness under transaction costs  

Signals failing these tests are excluded.

---

# Execution Assumptions

Signals use **next-day execution**.

Process:

1. Signals computed using today's close  
2. Positions entered at next market open  

This avoids **look-ahead bias** and reflects realistic trading.

---

# Key Characteristics

The strategy exhibits:

- diversified alpha sources  
- strong out-of-sample performance  
- low signal correlation  
- large ETF cross-section  
- stability across market regimes  

Performance arises from **stacking many independent signals**, not from leverage or a single predictive model.

---

# Conclusion

This project demonstrates that **multi-signal long–short ETF portfolios** can generate strong and robust risk-adjusted returns when constructed with:

- strict signal validation  
- large ETF universes  
- diversified alpha sources  
- disciplined out-of-sample testing  

The **combined portfolio** shows particularly strong stability, delivering high Sharpe ratios historically and providing a framework for ongoing **live out-of-sample evaluation**.
