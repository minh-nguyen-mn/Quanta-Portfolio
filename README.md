# ETF Long–Short Signal Portfolio

This project develops a systematic **multi-signal long–short ETF portfolio** designed to produce **robust, diversified alpha** across market regimes.

Rather than relying on a single model or leverage amplification, the strategy stacks **many independently validated signals**, each implemented as its own **long–short sub-portfolio**, and then aggregates them into a unified portfolio.

The core design principle is **robust signal diversification**: each signal must be profitable on its own and remain stable across multiple validation tests before inclusion.

---

# Strategy Overview

The system builds a portfolio using **cross-sectional ETF signals** applied to a broad universe of global ETFs.

Key characteristics:

- Multi-signal architecture
- Cross-asset ETF universe
- Long–short construction
- Equal-weight signal aggregation
- Extensive robustness validation

Each signal forms an **independent long–short sub-portfolio**, which allows failures to be isolated and reduces dependence on any single alpha source.

---

# ETF Universe

The strategy operates on a large cross-section of **~230 ETFs**, spanning:

- Global equities
- Sector ETFs
- Fixed income
- Commodities
- Volatility proxies
- Leveraged ETFs
- International markets

Examples include: SPY, QQQ, EWJ, FXI, XLV, XLP, VNQ, GLD, GDX, SOXX, TLT, HYG, AGG, IWM, EEM, EWZ, ITB, VGT, XLE, XBI


This broad universe provides **diversification across asset classes and geographies**, improving signal robustness.

---

# Portfolio Construction

The portfolio is constructed in **three layers**.

## 1. Signal Construction

Each signal generates a **cross-sectional ranking of ETFs**.

Signals capture different market effects such as:

- momentum persistence
- volatility compression
- price path efficiency
- volume confirmation
- liquidity persistence
- return dispersion
- entropy of price movement
- autocorrelation structure

Each signal is implemented as an **independent long–short portfolio**.

---

## 2. Signal Validation

Signals must pass strict criteria before inclusion.

Requirements include:

- Sharpe ≥ 1.0 in both **Train** and **Validation**
- Consistent behavior across market regimes
- Low correlation with existing signals
- Robustness under transaction costs
- Stability under leave-one-out tests

Signals that fail these checks are excluded.

---

## 3. Portfolio Aggregation

Validated signals are combined using: Equal-weight averaging of signal portfolios

This avoids overfitting and keeps the portfolio construction simple and robust.

Each signal contributes equally to the final portfolio.

---

# Portfolio Variants

Two portfolio structures are maintained.

## 1. Market Neutral Portfolio (Primary)
Long leverage = 1.0, Short leverage = 1.0


This configuration produces a **balanced long–short portfolio** designed to isolate alpha rather than market exposure.

This portfolio is the **primary focus of the strategy**.

---

## 2. Long-Biased Portfolio
Long leverage = 1.5, Short leverage = 1.0


This variant introduces **net long exposure** while keeping the signal structure identical.

It allows additional upside during strong equity regimes.

---

# Performance Summary

## Market Neutral Portfolio (1.0 / 1.0)

This is the **main strategy configuration**.

| Period | Sharpe |
|------|------|
| Train | 3.99 |
| Validation | 3.99 |
| Train + Val | 3.95 |
| Blind (Out-of-Sample) | 2.74 |

Key observations:

- Performance remains **strong and consistent across splits**
- Blind period confirms **good out-of-sample generalization**
- Sharpe remains significantly higher than the benchmark

---

# Signal Architecture

The final portfolio contains **19 validated signals**, each running as an independent long–short sub-portfolio.

Examples include:

- signal_1
- signal_3
- signal_8
- signal_9
- signal_entropy
- signal_autocorr
- signal_return_conviction
- signal_vol_of_vol
- signal_run_length
- signal_liquidity_persistence
- signal_signed_volume_agreement
- signal_price_volume_phase
- signal_vol_compression_ratio
- signal_convexity_gap_adjusted
- signal_time_since_volume_spike
- signal_path_efficiency
- signal_return_iqr
- signal_record_rate
- signal_burstiness

Each signal independently satisfies the validation criteria before inclusion.

---

# Signal Robustness

## Individual Signal Performance

Each signal demonstrates **independent profitability** in both training and validation sets, with most signals achieving Sharpe values around **1.0–1.4** before aggregation.

This ensures that portfolio performance does **not rely on a single dominant signal**.

---

## Leave-One-Out Stability

A leave-one-out analysis was performed by removing each signal individually and recomputing portfolio performance.

Results show that:

- performance remains stable
- no signal removal collapses returns
- the portfolio is **not dependent on any single signal**

This confirms **true diversification of alpha sources**.

---

## Signal Correlation

Signal correlations are generally **low to moderate**, with most pairwise correlations remaining well below **0.3**.

Low correlation between signals ensures that:

- signals capture different market effects
- portfolio diversification is effective
- risk concentration is minimized

---

# Execution Assumptions

The strategy assumes **next-day execution**, meaning signals are computed using today's close and positions are executed at the next market open.

This avoids look-ahead bias and ensures realistic tradability.

Transaction costs are included in robustness testing.

---

# Key Characteristics

The strategy exhibits several desirable properties:

- diversified alpha sources
- strong out-of-sample performance
- low signal correlation
- robustness to signal removal
- large ETF universe
- consistent behavior across market regimes

Most importantly, the results indicate that performance arises from **stacking many independent long–short signals**, rather than relying on leverage or a single predictive model.

---

# Future Improvements

Potential improvements include:

- turnover reduction via signal smoothing
- volatility-based signal weighting
- correlation-aware portfolio weighting
- dynamic capital allocation across signals
- expansion of orthogonal signal families

---

# Conclusion

This project demonstrates that a **multi-signal long–short ETF portfolio** can generate strong and robust risk-adjusted returns when built with strict validation and diversification principles.

The results suggest that:

- diversified signal stacking is a powerful source of alpha
- independent signal validation improves out-of-sample reliability
- broad ETF universes enable robust cross-sectional strategies

The market-neutral configuration shows particularly strong stability and remains the primary focus of the strategy.
