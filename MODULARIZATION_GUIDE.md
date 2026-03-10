# Portfolio Code Modularization Guide

## Overview

The two portfolio notebooks (`Portfolio_1_0xLong.ipynb` and `Portfolio_1_5xLong.ipynb`) contain nearly identical code logic with only differences in their **signal maps** (different ETF universes and parameters).

This guide shows how to modularize the code to eliminate duplication and improve maintainability.

## Structure

### Files

1. **portfolio_config.py** - Signal map configurations for each portfolio variant
   - Defines ETF universes and parameters for each strategy
   - Easily add new variants without code duplication

2. **portfolio_engine.py** (to be created) - Core portfolio logic
   - Extract all common functions and classes
   - Main analysis, backtesting, signal generation code
   - Use configuration objects instead of hardcoded values

3. **Portfolio_1_0xLong.ipynb** (refactored) - 1.0x Long variant notebook
   - Import signal config and engine
   - Pass config to analysis functions
   - Much shorter and focused on results

4. **Portfolio_1_5xLong.ipynb** (refactored) - 1.5x Long variant notebook
   - Import signal config and engine
   - Pass config to analysis functions
   - Same analysis, different signal map

## Refactoring Steps

### Step 1: Extract Configuration (DONE)
✅ Move ETF_UNIVERSE assignments to `portfolio_config.py`
- Create signal map dictionaries for each portfolio variant
- Include leverage factors, bond lists, and other parameters

### Step 2: Extract Core Logic
Extract the main code cell (lines 5-5227 in notebook) into `portfolio_engine.py`:
- Data loading and preprocessing functions
- Signal generation functions
- Backtesting and analysis functions
- Performance calculation functions

Key principle: Functions should accept `signal_config` as a parameter rather than using global variables.

### Step 3: Refactor Notebooks
Minimize each notebook to:
```python
# Import configuration and engine
from portfolio_config import get_signal_config
from portfolio_engine import run_portfolio_analysis

# Load this variant's signal map
config = get_signal_config('1.0x_long')  # or '1.5x_long'

# Run analysis with the config
results = run_portfolio_analysis(config)

# Display results and visualizations
display_results(results)
```

## Benefits

1. **DRY (Don't Repeat Yourself)**
   - Core logic written once, used by both portfolios
   - Easier to maintain and update

2. **Easy to Add New Variants**
   - Just add a new signal config to `portfolio_config.py`
   - No need to duplicate entire notebooks

3. **Better Testing**
   - Core functions can be tested independently
   - Easier to verify changes don't break existing logic

4. **Clearer Intent**
   - Notebooks focus on the specific variant and results
   - Shared logic isolated in the engine module

5. **Collaboration**
   - Team members can work on configs vs. logic separately
   - Easier code review and version control

## Implementation Example

### Original Notebook Pattern
```python
# Cell 1: Config - DUPLICATED in both notebooks
POLYGON_API_KEY = "..."
ETF_UNIVERSE = ['ROM', 'QQQ', ...]  # Different per notebook
BOND = [...]  # Same in both

# Cell 2-100: Large code cell with all logic - DUPLICATED
def calculate_signals():
    ...
    
def run_backtest():
    ...

# Execute
results = run_backtest()  # Uses global ETF_UNIVERSE
```

### Refactored Pattern
```python
# Cell 1: Import and configure
from portfolio_config import get_signal_config
from portfolio_engine import run_portfolio_analysis

config = get_signal_config('1.0x_long')

# Cell 2: Run analysis
results = run_portfolio_analysis(config)

# Cell 3+: Visualizations and results display
display_results(results)
```

## Migration Checklist

- [ ] Extract configuration to `portfolio_config.py`
- [ ] Create `portfolio_engine.py` with core functions
  - [ ] Move data loading functions
  - [ ] Move signal generation functions
  - [ ] Move backtesting functions
  - [ ] Update functions to use config parameter
- [ ] Refactor `Portfolio_1_0xLong.ipynb`
  - [ ] Remove config definitions
  - [ ] Remove core logic cells
  - [ ] Add import statements
  - [ ] Update to use `run_portfolio_analysis(config)`
- [ ] Refactor `Portfolio_1_5xLong.ipynb`
  - [ ] Same changes as 1.0x variant
  - [ ] Test that results match original
- [ ] Update `Quanta_W7.ipynb` if it has duplicated code
- [ ] Test both notebooks work correctly
- [ ] Update documentation/README

## Next Steps

1. **Extract portfolio_engine.py**: 
   - Copy the large code cell from the original notebooks
   - Segment into logical functions
   - Add `signal_config` parameter to all Functions
   - Remove hardcoded variable references

2. **Update Notebooks**:
   - Keep all visualization and results cells
   - Remove all duplicated setup and logic cells
   - Add clear imports and configuration loading

3. **Add New Variants**:
   - To add a new portfolio variant:
     - Add config to `portfolio_config.py`
     - Create new notebook with imports and results
     - Done! (no code duplication needed)

## Example New Variant

To add a 2.0x leverage variant:

```python
# In portfolio_config.py - Add this:
SIGNAL_2_0X_LONG = {
    'name': '2.0x Long Portfolio',
    'leverage': 2.0,
    'etf_universe': [...],  # Your ETF selections
    'bond_etfs': [...]  # Bond universe
}
```

Then in notebook:
```python
config = get_signal_config('2.0x_long')
results = run_portfolio_analysis(config)
```

Done! No code duplication needed.
