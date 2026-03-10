# Validation Checklist for Modularized Notebooks

## Pre-Execution Checks

- [ ] API key configured (or environment variable set)
- [ ] Python 3.9+ with pandas, numpy, scipy, requests installed
- [ ] Internet connection for Polygon API calls
- [ ] Original notebooks (Portfolio_1_0xLong.ipynb, Portfolio_1_5xLong.ipynb) available for comparison

## Step 1: Extract Original Metrics

**Objective**: Get baseline metrics from original notebooks

```python
# Run Portfolio_1_0xLong.ipynb cells up to metrics calculation
# Extract and record these values:

ORIGINAL_1_0X_METRICS = {
    'train_sharpe': ______,      # From original output
    'val_sharpe': ______,        # From original output
    'blind_sharpe': ______,      # From original output
    'full_sharpe': ______,       # Train+Val+Blind combined
}

ORIGINAL_1_5X_METRICS = {
    'train_sharpe': ______,      # From original output
    'val_sharpe': ______,        # From original output
    'blind_sharpe': ______,      # From original output
    'full_sharpe': ______,       # Train+Val+Blind combined
}
```

- [ ] Extracted TRAIN SHARPE (1.0x)
- [ ] Extracted VAL SHARPE (1.0x)
- [ ] Extracted BLIND SHARPE (1.0x)
- [ ] Extracted TRAIN SHARPE (1.5x)
- [ ] Extracted VAL SHARPE (1.5x)
- [ ] Extracted BLIND SHARPE (1.5x)

## Step 2: Execute Refactored 1.0x Notebook

**Objective**: Generate metrics from Portfolio_1_0xLong_REFACTORED.ipynb

```python
# Run all cells in refactored notebook
# Record output from Cell 6 (metrics calculation):

REFACTORED_1_0X_METRICS = {
    'train_sharpe': ______,
    'val_sharpe': ______,
    'blind_sharpe': ______,
    'full_sharpe': ______,
}
```

- [ ] Cell 1: Markdown loads without error
- [ ] Cell 2: Imports succeed (signals + portfolio_engine)
- [ ] Cell 3: Configuration set correctly
- [ ] Cell 4: Data loading completes (check cache messages)
- [ ] Cell 5: Backtest executes without error
- [ ] Cell 6: Metrics calculated
- [ ] Cell 7: Equity curve plots
- [ ] Cell 8: Performance tables generate

## Step 3: Compare 1.0x Metrics

**Tolerance**: ±0.0001 on Sharpe ratios

| Metric | Original | Refactored | ±0.0001? | Pass? |
|--------|----------|-----------|----------|-------|
| TRAIN SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |
| VAL SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |
| BLIND SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |
| FULL SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |

- [ ] All train metrics within ±0.0001
- [ ] All validation metrics within ±0.0001
- [ ] All blind metrics within ±0.0001
- [ ] All portfolio metrics within ±0.0001

**If any metric fails**: Check [Troubleshooting](#troubleshooting) section

## Step 4: Validate Equity Curves (1.0x)

**Objective**: Verify continuous cumulative returns match

```python
# In refactored notebook after Cell 5:
from scipy.stats import pearsonr

# Extract equity curves
orig_equity = original_pnl.cumsum()
refac_equity = refactored_pnl.cumsum()

# Calculate correlation
corr, pval = pearsonr(orig_equity.fillna(method='ffill'), 
                      refac_equity.fillna(method='ffill'))
print(f"Equity curve correlation: {corr:.6f}")

# Visual comparison
plt.figure(figsize=(12, 6))
plt.plot(orig_equity, label='Original', alpha=0.7)
plt.plot(refac_equity, label='Refactored', alpha=0.7)
plt.legend()
plt.title('Equity Curve Comparison (1.0x)')
plt.show()
```

- [ ] Equity curve correlation > 0.999
- [ ] Visual inspection shows curves overlap closely
- [ ] No unexplained divergences
- [ ] Drawdown patterns match

## Step 5: Execute Refactored 1.5x Notebook

**Objective**: Generate metrics from Portfolio_1_5xLong_REFACTORED.ipynb

```python
REFACTORED_1_5X_METRICS = {
    'train_sharpe': ______,
    'val_sharpe': ______,
    'blind_sharpe': ______,
    'full_sharpe': ______,
}
```

- [ ] Cell 1: Markdown loads without error
- [ ] Cell 2: Imports succeed
- [ ] Cell 3: LONG_LEVERAGE = 1.5 confirmed
- [ ] Cell 4: Data loading completes
- [ ] Cell 5: Backtest executes
- [ ] Cell 6: Metrics calculated
- [ ] Cell 7: Equity curve plots
- [ ] Cell 8: Performance tables generate

## Step 6: Compare 1.5x Metrics

**Tolerance**: ±0.0001 on Sharpe ratios

| Metric | Original | Refactored | ±0.0001? | Pass? |
|--------|----------|-----------|----------|-------|
| TRAIN SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |
| VAL SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |
| BLIND SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |
| FULL SHARPE | ___ | ___ | ✓/✗ | ✓/✗ |

- [ ] All train metrics within ±0.0001
- [ ] All validation metrics within ±0.0001
- [ ] All blind metrics within ±0.0001

## Step 7: Validate Equity Curves (1.5x)

- [ ] Equity curve correlation > 0.999
- [ ] Visual inspection shows curves overlap
- [ ] Leverage effect visible (steeper slopes than 1.0x)
- [ ] Drawdown patterns match original

## Step 8: Per-ETF Statistics Validation

**Sample Check**: Verify 3 random ETFs match

```python
# Cell 8 generates per-ETF statistics
# Compare original vs refactored for 3 random tickers:

SAMPLE_TICKERS = ['QQQ', 'SPY', 'GRID']

for ticker in SAMPLE_TICKERS:
    orig_stats = original_perf_stats.loc[ticker]
    refac_stats = refactored_perf_stats.loc[ticker]
    
    print(f"\n{ticker}:")
    print(f"  Sharpe: {orig_stats['sharpe']:.6f} vs {refac_stats['sharpe']:.6f}")
    print(f"  CAGR: {orig_stats['cagr']:.6f} vs {refac_stats['cagr']:.6f}")
    print(f"  Turnover: {orig_stats['turnover']:.6f} vs {refac_stats['turnover']:.6f}")
```

- [ ] QQQ metrics match (±0.0001)
- [ ] SPY metrics match (±0.0001)
- [ ] GRID metrics match (±0.0001)
- [ ] All other ETFs spot-checked

## Final Summary

| Category | Status | Evidence |
|----------|--------|----------|
| **1.0x Metrics** | ✓/✗ | All within ±0.0001 |
| **1.0x Equity Curve** | ✓/✗ | Correlation > 0.999 |
| **1.5x Metrics** | ✓/✗ | All within ±0.0001 |
| **1.5x Equity Curve** | ✓/✗ | Correlation > 0.999 |
| **Per-ETF Stats** | ✓/✗ | Sample tickers match |
| **Overall** | ✓/✗ | Ready for production |

---

## Troubleshooting

### Issue: Sharpe ratios differ by >0.0001

**Possible Causes**:
1. Missing NaN handling in return calculations
2. Different period slicing (inclusive vs exclusive dates)
3. Different rolling window parameters
4. Integer vs float precision

**Solutions**:
- Check sharpe() function in portfolio_engine.py for robustness checks
- Verify date slicing in run_period() matches original
- Compare signal window parameters between signals.py and original
- Use `.astype('float64')` for explicit precision

### Issue: Equity curves diverge significantly

**Possible Causes**:
1. Position sizing differs (equal vs rank vs zscore mode)
2. Leverage not applied correctly
3. Cost assumptions (slippage, commissions)
4. Signal generation differs

**Solutions**:
- Check build_long_short_portfolio() portfolio_mode parameter
- Add debug prints for position sizes: print(pos_full.head())
- Verify long_leverage/short_leverage applied in run_period()
- Compare signal values: signal_original vs signal_refactored

### Issue: Data loading fails with API error

**Possible Causes**:
1. API key invalid or rate-limited
2. Network connectivity issue
3. Polygon API down or ticker not found

**Solutions**:
- Verify POLYGON_API_KEY is correct
- Test single ticker: fetch_etf('QQQ', api_key, '2000-01-01')
- Check Polygon API status: https://status.polygon.io/
- Fall back to CSV cache if available

### Issue: Memory error on large universes

**Possible Causes**:
1. Too many ETFs (loading 300+ tickers)
2. Insufficient RAM (< 8GB)
3. Data not cached properly

**Solutions**:
- Reduce ETF_UNIVERSE to top 50 tickers for testing
- Close other applications to free memory
- Force clear cache: del _ETF_CACHE; gc.collect()
- Process in batches: split universe into 50-ticker chunks

---

## Sign-Off

**Validation Date**: ________________

**Validator**: ________________

**Status**: ✓ PASS / ✗ FAIL

**Notes**:
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

**Approval for Production**: ✓ YES / ✗ NO
