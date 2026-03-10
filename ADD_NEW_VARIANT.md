# Adding New Portfolio Variants - Quick Guide

## Overview

Once the modularization is complete, adding new portfolio variants (e.g., 2.0x Long, 3.0x Long, Short variants, etc.) becomes trivial - **you only need to edit `portfolio_config.py`**, no other code changes required!

## Before Modularization
Adding a new portfolio variant required:
1. Copy entire 5000+ line notebook code
2. Modify ETF universe list
3. Modify leverage factor
4. Modify any variant-specific calculations
5. Test and debug both old and new notebooks
6. **Total effort: 4-6 hours per new variant**

## After Modularization
Adding a new portfolio variant requires:
1. Edit `portfolio_config.py` (5 minutes)
2. Copy refactored notebook template (1 minute)
3. Change one line in the notebook (1 minute)
4. Run and verify (10 minutes)
5. **Total effort: 20 minutes per new variant**

---

## Example 1: Add 2.0x Long Portfolio

### Step 1: Add Configuration to `portfolio_config.py`

Open `portfolio_config.py` and add this new configuration:

```python
SIGNAL_2_0X_LONG = {
    'name': '2.0x Long Portfolio',
    'leverage': 2.0,
    'etf_universe': [
        # Your ETF selections for 2.0x variant
        # Can be same as 1.0x/1.5x or different
        'ROM', 'QQQ', 'XLU', 'VTI', 'VEA',
        # ... rest of ETF list
    ],
    'bond_etfs': BOND_ETFS,  # Reference shared bond list
}
```

### Step 2: Update `get_signal_config()` function

In the same file, update the factory function:

```python
def get_signal_config(portfolio_variant: str) -> Dict:
    """
    Get signal configuration for portfolio variant.
    
    Args:
        portfolio_variant: '1.0x_long', '1.5x_long', '2.0x_long', etc.
    
    Returns:
        Dictionary with signal configuration
    """
    variants = {
        '1.0x_long': SIGNAL_1_0X_LONG,
        '1.5x_long': SIGNAL_1_5X_LONG,
        '2.0x_long': SIGNAL_2_0X_LONG,  # NEW LINE
    }
    
    if portfolio_variant not in variants:
        raise ValueError(f"Unknown variant: {portfolio_variant}")
    
    return variants[portfolio_variant]
```

### Step 3: Create New Notebook

Copy one of the refactored notebooks and modify:

1. Copy `Portfolio_1_0xLong.ipynb` → `Portfolio_2_0xLong.ipynb`
2. In Cell 1 (Markdown), update title:
   ```markdown
   # Portfolio Analysis - 2.0x Long
   ```

3. In Cell 3 (Configuration), change one line:
   ```python
   config = get_signal_config('2.0x_long')  # Changed
   ```

That's it! All other code is unchanged.

### Step 4: Run & Verify

1. Open `Portfolio_2_0xLong.ipynb`
2. Run all cells
3. Verify results look reasonable:
   - Equity curve should be similar shape to 1.5x but with 2x volatility
   - Sharpe ratio might be lower (higher leverage = higher risk)
   - Returns should be roughly 2x the 1.0x portfolio

---

## Example 2: Add Short Portfolio Variant

### Step 1: Add to `portfolio_config.py`

```python
SIGNAL_1_0X_SHORT = {
    'name': '1.0x Short Portfolio',
    'leverage': -1.0,  # Negative leverage for short positions
    'etf_universe': [
        # Same or different ETFs
        # Negative leverage will short these
        'ROM', 'QQQ', 'XLU', 'VTI', 'VEA',
        # ...
    ],
    'bond_etfs': BOND_ETFS,
}
```

### Step 2: Update factory function

```python
def get_signal_config(portfolio_variant: str) -> Dict:
    variants = {
        '1.0x_long': SIGNAL_1_0X_LONG,
        '1.5x_long': SIGNAL_1_5X_LONG,
        '2.0x_long': SIGNAL_2_0X_LONG,
        '1.0x_short': SIGNAL_1_0X_SHORT,  # NEW
    }
    # ... rest unchanged
```

### Step 3: Create Notebook

Copy template, change:
- Title to "1.0x Short"
- Config to `'1.0x_short'`

The engine will automatically handle negative leverage!

---

## Example 3: Add Sector-Specific Portfolio

### Step 1: Create Variant Configuration

```python
SIGNAL_1_0X_TECH = {
    'name': '1.0x Tech-Focused Portfolio',
    'leverage': 1.0,
    'etf_universe': [
        # Only tech sector ETFs
        'QQQ',    # NASDAQ-100
        'XLK',    # Technology sector
        'QQQS',   # Quality ETFs
        'ARKK',   # Tech innovation
        # ... more tech ETFs
    ],
    'bond_etfs': BOND_ETFS,
}
```

### Step 2: Add to Factory

```python
variants = {
    # ... existing variants
    '1.0x_tech': SIGNAL_1_0X_TECH,  # NEW
}
```

### Step 3: Create Notebook

Copy template, change configuration to `'1.0x_tech'`

---

## Summary: Files to Edit for New Variants

| Variant Type | Files to Edit | Lines to Change | Time |
|--------------|---------------|-----------------|------|
| New Leverage (1x, 2x, 3x) | `portfolio_config.py` + 1 notebook | 10 lines total | 20 min |
| New ETF Universe | `portfolio_config.py` + 1 notebook | 20 lines total | 30 min |
| New Direction (Long/Short) | `portfolio_config.py` + 1 notebook | 10 lines total | 20 min |
| Sector-Specific | `portfolio_config.py` + 1 notebook | 25 lines total | 30 min |

**Contrast with original**: Would require copying 5000+ line cell and modifying calculations!

---

## Modifying Existing Variants

### To adjust ETF universe for 1.0x:
Edit `SIGNAL_1_0X_LONG['etf_universe']` list in `portfolio_config.py`
- All notebooks using this config get the change
- Only 1 place to update

### To change leverage for 1.5x:
Edit `SIGNAL_1_5X_LONG['leverage']` in `portfolio_config.py`
- Change applies to all notebooks automatically

### To add bond universe adjustments:
Edit `BOND_ETFS` list in `portfolio_config.py`
- Applies to all variants that use `BOND_ETFS`
- Single source of truth

---

## Best Practices for New Variants

### DO:
✅ **Do use shared bond list**
```python
'bond_etfs': BOND_ETFS,  # Good - shares updates
```

✅ **Do follow naming convention**
```python
SIGNAL_[LEVERAGE]_[DIRECTION]  # e.g., SIGNAL_2_0X_LONG
'[leverage]x_[direction]'       # e.g., '2.0x_long'
```

✅ **Do verify leverage is being applied correctly**
- Positive leverage: long positions
- Negative leverage: short positions
- Magnitude affects position size

✅ **Do test results make intuitive sense**
- Higher leverage = higher returns AND higher risk
- Short portfolios should be inverse of long
- Equity curves should correlate appropriately

### DON'T:
❌ **Don't duplicate ETF lists**
```python
# Bad - duplicated data
SIGNAL_NEW = {
    'bond_etfs': ['TLT', 'BND', 'AGG', ...]  # Same list as others
}

# Good - reference shared data
SIGNAL_NEW = {
    'bond_etfs': BOND_ETFS  # Shared
}
```

❌ **Don't hardcode calculations in new variant**
```python
# Bad - variant-specific calculation
if variant == '2.0x_long':
    position_size = something_special

# Good - leverage already applied in generic engine
position_size = signal * self.leverage  # Works for all variants
```

❌ **Don't create new notebook from scratch**
```python
# Bad - copy entire old notebook code
# Copy -> modify ETF list -> redo everything

# Good - copy refactored template
# Copy template -> change 1 line config -> done
```

---

## Testing New Variants

### Quick Smoke Test:
```python
from portfolio_config import get_signal_config
from portfolio_engine import PortfolioAnalysisEngine

# Load new variant
config = get_signal_config('2.0x_long')
engine = PortfolioAnalysisEngine(config)

# Test it works
try:
    results = engine.run_full_analysis()
    print(f"✓ {config['name']} works!")
    print(f"  Sharpe: {results['metrics']['sharpe_ratio']:.4f}")
except Exception as e:
    print(f"✗ Error: {e}")
```

### Full Test:
1. Run refactored notebook
2. Check metrics are reasonable
3. Compare equity curve to 1.0x/1.5x variants
4. Verify leverage is properly reflected in volatility

---

## Comparison: Before vs After

### BEFORE: Adding 2.0x Long Portfolio

1. Open `Portfolio_1_0xLong.ipynb`
2. Save As: `Portfolio_2_0xLong.ipynb`
3. Find and copy lines 5-5227 (5000+ lines)
4. Modify in new notebook:
   - Change leverage: 1.0 → 2.0
   - Change ETF universe (if different)
   - Test everything
5. Debug differences
6. **Result**: 5000+ lines of duplicated code

### AFTER: Adding 2.0x Long Portfolio

1. Edit `portfolio_config.py`:
   ```python
   SIGNAL_2_0X_LONG = {...}  # Add 10 lines
   variants = {..., '2.0x_long': SIGNAL_2_0X_LONG}  # Change 1 line
   ```
2. Copy `Portfolio_1_0xLong.ipynb` → `Portfolio_2_0xLong.ipynb`
3. Change 1 line: `get_signal_config('2.0x_long')`
4. Run notebook
5. **Result**: ~100 lines of configuration + reusable notebook template

---

## Future-Proofing

### Good Configuration Structure:
```python
SIGNAL_VARIANT = {
    'name': 'Human-readable name',
    'leverage': 1.0,  # Easy to adjust
    'etf_universe': [...],  # Easy to modify
    'bond_etfs': BOND_ETFS,  # Shared reference
    # Optional: strategy-specific params
    'momentum_period': 20,
    'mean_reversion_threshold': 1.5,
}
```

### Avoid:
```python
# Hard-coded in calculation functions - bad!
MOMENTUM_PERIOD = 20
MEAN_REVERSION_THRESHOLD = 1.5

# Should be in config instead
```

---

## Questions Before Adding New Variant?

**Q: Should I modify existing 1.0x config?**
A: Only if you want to change the strategy. Otherwise create new variant.

**Q: Can I have multiple leverage levels for same ETF universe?**
A: Yes! 1.0x_long, 1.5x_long, 2.0x_long all use same ETFs, different leverage.

**Q: Can I share parts of config between variants?**
A: Yes, like `BOND_ETFS` is shared. Create helper lists for common ETF groups.

**Q: What if I want dynamic ETF selection based on date?**
A: Create function in config.py that returns appropriate list based on parameters.

**Q: Should metrics calculations change between variants?**
A: No, leverage is handled in engine. Same metrics formula for all variants.

---

## Git/Version Control Notes

When adding new variants:
1. Commit `portfolio_config.py` changes separately
2. Commit new notebook in same commit (or separate feature branch)
3. Example: `git commit -m "Add 2.0x Long portfolio variant"`

This makes it easy to:
- Review what configurations changed
- Track when new variants were added
- Revert specific variants if needed

---

## Summary

**With modularization, adding new portfolio variants is now:**
- ✅ Quick (20-30 minutes per variant)
- ✅ Simple (edit config + copy notebook)
- ✅ Safe (reuses tested engine code)
- ✅ Maintainable (changes in one place apply to all)
- ✅ Extensible (easy to add more variants later)

**Without modularization, adding variants is:**
- ❌ Slow (4-6 hours per variant)
- ❌ Complex (copy+modify 5000 lines)
- ❌ Risky (potential to introduce bugs)
- ❌ Hard to maintain (changes needed in many places)
- ❌ Difficult to extend (discourages experimentation)
