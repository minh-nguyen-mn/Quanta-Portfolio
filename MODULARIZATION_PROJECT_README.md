# Quanta Portfolio Modularization Project

## 📋 Project Overview

This repository contains the work to **modularize and eliminate code duplication** from the Quanta Portfolio analysis codebase. The original two portfolio notebooks (`Portfolio_1_0xLong.ipynb` and `Portfolio_1_5xLong.ipynb`) contained 5000+ lines of nearly identical code, differing only in signal configurations and leverage factors.

**Goal**: Extract shared analysis logic into reusable modules and reduce code duplication from ~10,000 lines to ~3,000 lines (75% reduction).

---

## 📁 Project Structure

### Original Files (No Changes Yet)
- **Portfolio_1_0xLong.ipynb** - 1.0x leverage long portfolio (5000+ lines)
- **Portfolio_1_5xLong.ipynb** - 1.5x leverage long portfolio (5000+ lines)
- **Quanta_W7.ipynb** - Week 7 analysis (if uses similar code)

### New Modular Components
- **portfolio_config.py** - Signal configurations for all portfolio variants
- **portfolio_engine.py** - Shared analysis engine (to be populated)

### Documentation & Guides
- **MODULARIZATION_GUIDE.md** - Architecture overview and strategy
- **EXTRACTION_GUIDE.md** - Detailed step-by-step extraction instructions
- **IMPLEMENTATION_CHECKLIST.md** - Project tasks and progress tracking
- **ADD_NEW_VARIANT.md** - How to add new portfolio variants (value of modularization)
- **REFACTORED_NOTEBOOK_TEMPLATE.ipynb** - Template showing refactored notebook structure

---

## 🚀 Quick Start

### For New Team Members
1. Read **MODULARIZATION_GUIDE.md** (10 min) - Understand the problem and solution
2. Read **EXTRACTION_GUIDE.md** (15 min) - See exactly what needs to be done
3. Look at **REFACTORED_NOTEBOOK_TEMPLATE.ipynb** (5 min) - See what notebooks will look like
4. Use **IMPLEMENTATION_CHECKLIST.md** to track progress

### To Continue Implementation
1. Open **IMPLEMENTATION_CHECKLIST.md** - See what's complete and what's next
2. Currently completing: Phase 2 (Core Engine Extraction)
   - Details in EXTRACTION_GUIDE.md Section "Phase 2"
   - Focus on extracting functions from original notebooks to portfolio_engine.py
3. Next: Phase 3 (Notebook Refactoring) - Details in EXTRACTION_GUIDE.md Section "Phase 3"

### To Add New Portfolio Variant
See **ADD_NEW_VARIANT.md** - Shows how easy variant creation becomes after modularization.

---

## 📊 Current Status

| Phase | Task | Status | Key Files |
|-------|------|--------|-----------|
| 1 | Configuration Extraction | ✅ COMPLETE | `portfolio_config.py` |
| 2 | Core Engine Extraction | 🔄 IN PROGRESS | `portfolio_engine.py` |
| 3 | Notebook Refactoring | ⏳ PENDING | Portfolio notebooks |
| 4 | Validation Testing | ⏳ PENDING | - |
| 5 | Documentation | ✅ COMPLETE | All .md files |
| 6 | Deployment | ⏳ PENDING | - |

**Overall Progress**: ~35% (Configuration complete, Engine skeleton created, Documentation finished)

---

## 🔍 What's Already Done

### ✅ Configuration Module (`portfolio_config.py`)
```python
# Two signal configurations created:
SIGNAL_1_0X_LONG = {
    'name': '1.0x Long Portfolio',
    'leverage': 1.0,
    'etf_universe': [...],  # 21 ETFs
    'bond_etfs': [...]      # 54 bond ETFs
}

SIGNAL_1_5X_LONG = {
    'name': '1.5x Long Portfolio',
    'leverage': 1.5,  # Only difference!
    'etf_universe': [...],  # Same as 1.0x
    'bond_etfs': [...]      # Same as 1.0x
}

# Factory function to retrieve configs:
def get_signal_config(portfolio_variant: str) -> Dict
```

**Status**: ✅ Complete and importable

### ✅ Engine Skeleton (`portfolio_engine.py`)
```python
class PortfolioAnalysisEngine:
    def __init__(self, signal_config: Dict):
        # Takes configuration as parameter
    
    def load_data(self) -> pd.DataFrame:
        # [To be extracted]
    
    def generate_signals(self) -> pd.DataFrame:
        # [To be extracted]
    
    def run_backtest(self) -> Dict:
        # [To be extracted]
    
    def calculate_metrics(self) -> Dict[str, float]:
        # [To be extracted]
    
    def run_full_analysis(self) -> Dict:
        # Full pipeline - data → signals → backtest → metrics
```

**Status**: ✅ Structure designed, waiting for code extraction

### ✅ Documentation
- **MODULARIZATION_GUIDE.md** (180 lines) - Complete architecture overview
- **EXTRACTION_GUIDE.md** (400+ lines) - Detailed extraction instructions with code examples
- **IMPLEMENTATION_CHECKLIST.md** (300+ lines) - Task tracking and progress
- **ADD_NEW_VARIANT.md** (300+ lines) - Examples of adding 2.0x, Short, Sector variants
- **REFACTORED_NOTEBOOK_TEMPLATE.ipynb** - Sample notebook showing refactored structure

**Status**: ✅ Complete and comprehensive

---

## 🔧 What Needs to Be Done

### Phase 2: Core Engine Extraction (IN PROGRESS)
**Effort**: ~15-18 hours

1. **Extract code from original notebooks**
   - Copy lines 5-5227 from `Portfolio_1_0xLong.ipynb`
   - Break into logical sections (data loading, signals, backtest, metrics)
   - Follow EXTRACTION_GUIDE.md for detailed steps

2. **Populate portfolio_engine.py methods**
   - Implement `load_data()` - fetch and preprocess data
   - Implement `generate_signals()` - calculate all signals
   - Implement `run_backtest()` - simulate portfolio
   - Implement `calculate_metrics()` - compute performance stats
   - Implement `run_full_analysis()` - orchestrate pipeline

3. **Test extraction**
   - Verify extracted code produces identical results to original
   - Compare metrics: Sharpe ratio, Sortino, drawdown, returns
   - Validate on both 1.0x and 1.5x configurations

### Phase 3: Notebook Refactoring (PENDING)
**Effort**: ~2-3 hours

1. **Refactor Portfolio_1_0xLong.ipynb**
   - Remove 5000+ line code cell
   - Add imports and configuration loading
   - Keep visualization cells intact
   - Test against original

2. **Refactor Portfolio_1_5xLong.ipynb**
   - Identical changes, but with `'1.5x_long'` config
   - Only 2 lines different from 1.0x notebook

### Phase 4: Validation Testing (PENDING)
**Effort**: ~1-2 hours

- Run both refactored notebooks
- Compare results to originals (metrics must match exactly)
- Check visualization consistency
- Verify equity curves overlay perfectly

### Phase 5: Documentation Updates (PENDING)
**Effort**: ~1 hour

- Update main README.md with new structure
- Document how to run modularized notebooks
- Add examples for adding new variants

### Phase 6: Cleanup & Deployment (PENDING)
**Effort**: ~1-2 hours

- Archive original notebooks
- Organize repository
- Final verification from clean environment

---

## 📖 How to Use the Guides

### MODULARIZATION_GUIDE.md
**What**: High-level overview of the problem and solution
**When to read**: First - get strategic understanding
**Time**: 10-15 minutes
**Contains**:
- Problem statement (code duplication)
- Solution approach (modular architecture)
- File structure description
- Benefits enumeration
- Implementation examples
- Migration checklist

### EXTRACTION_GUIDE.md
**What**: Detailed, step-by-step extraction instructions
**When to read**: Before starting Phase 2
**Time**: 20-30 minutes
**Contains**:
- Section-by-section analysis template
- Code refactoring patterns (before/after)
- Global variable replacement guide
- Testing approach
- File size reduction metrics
- Troubleshooting section

### IMPLEMENTATION_CHECKLIST.md
**What**: Task-by-task breakdown with effort estimates
**When to use**: Throughout implementation to track progress
**Time**: Reference document
**Contains**:
- 50+ checkbox items organized by phase
- Time estimates for each task
- Success criteria for completion
- Progress summary table
- Key milestones
- Phase dependencies

### ADD_NEW_VARIANT.md
**What**: Demonstrates the value of modularization
**When to read**: After modularization to understand benefits
**Time**: 15-20 minutes
**Contains**:
- Examples: 2.0x, Short, Sector portfolios
- Before/after effort comparison (6 hours → 20 minutes!)
- Detailed configuration patterns
- Best practices
- Testing approach

### REFACTORED_NOTEBOOK_TEMPLATE.ipynb
**What**: Working notebook template showing refactored structure
**When to use**: As template while refactoring actual notebooks
**Time**: Reference/copy as needed
**Contains**:
- Cell-by-cell structure for refactored notebook
- Import patterns
- Configuration loading
- Analysis execution
- Visualization examples
- Documentation cells

---

## 🎯 Key Design Principles

### 1. Configuration as Data
Signal maps are stored as data dictionaries, not hardcoded in calculation logic.

```python
# ✅ Good - Configuration is separate
config = get_signal_config('1.0x_long')
engine = PortfolioAnalysisEngine(config)

# ❌ Bad - Configuration mixed in logic
if PORTFOLIO_TYPE == '1.0x_long':
    ETF_UNIVERSE = [...]  # Hardcoded
```

### 2. Single Responsibility
Each module has one clear purpose:
- `portfolio_config.py` - Signal configurations
- `portfolio_engine.py` - Analysis logic
- Notebooks - Results visualization and reporting

### 3. Factory Pattern
Use factory function to manage multiple variants:
```python
get_signal_config('1.0x_long')   # Returns config dict
get_signal_config('1.5x_long')   # Returns config dict
get_signal_config('2.0x_long')   # Easy to add new!
```

### 4. Leverage as Parameter
Leverage is not hardcoded; it comes from configuration:
```python
position_size = signal_strength * config['leverage']
```

This automatically handles 1.0x, 1.5x, 2.0x, shorts (-1.0x), etc.

### 5. Shared Components
Common resources (bond ETF lists) are shared references:
```python
BOND_ETFS = [...]  # Single source of truth

SIGNAL_1_0X_LONG = {..., 'bond_etfs': BOND_ETFS}
SIGNAL_1_5X_LONG = {..., 'bond_etfs': BOND_ETFS}
SIGNAL_2_0X_LONG = {..., 'bond_etfs': BOND_ETFS}
# Update once, applies to all variants
```

---

## 🧪 Testing Strategy

### Validation Approach
1. **Unit Testing**: Test each extracted function independently
2. **Integration Testing**: Test full pipeline
3. **Regression Testing**: Compare results to original notebooks
4. **Validation Criteria**: Metrics match to 4 decimal places

### How to Validate
```python
# In a notebook or script:
from portfolio_config import get_signal_config
from portfolio_engine import PortfolioAnalysisEngine

# Test 1.0x variant
config_1_0x = get_signal_config('1.0x_long')
engine_1_0x = PortfolioAnalysisEngine(config_1_0x)
results_1_0x = engine_1_0x.run_full_analysis()

# Compare to original notebook output:
original_sharpe = 1.148404  # From original notebook
new_sharpe = results_1_0x['metrics']['sharpe_ratio']
assert abs(original_sharpe - new_sharpe) < 0.0001

print("✓ Results match original!")
```

---

## 📚 Dependencies

### Required Python Packages
- pandas
- numpy
- matplotlib
- scipy (for statistics)
- polygon-io (for market data API)

### External Resources
- Polygon.io API (for OHLCV data)
- API Key required: `POLYGON_API_KEY`

---

## 🚨 Important Notes

### Backup Your Work
The original notebooks are being modified. Before starting:
1. Create backups: `Portfolio_1_0xLong_ORIGINAL.ipynb`, etc.
2. Commit to version control before making changes
3. Keep git history clean with descriptive messages

### Data Integrity
Ensure refactored code produces **exactly identical** results:
- Metrics match to 4 decimal places
- Equity curves overlay perfectly
- No data loss or corruption
- Handle edge cases correctly

### API Limits
Polygon.io has rate limits. During testing:
- Cache data locally if running many tests
- Space out API calls
- Monitor rate limit headers

### Code Review
Before deployment:
1. Have another team member review changes
2. Run full notebook end-to-end
3. Compare visualizations side-by-side
4. Verify no performance regressions

---

## 📞 Troubleshooting

### Import Errors
```
ModuleNotFoundError: No module named 'portfolio_config'
```
**Solution**: Ensure `portfolio_config.py` and `portfolio_engine.py` are in same directory as notebook.

### Metrics Don't Match
```
AssertionError: Sharpe ratio 1.1234 != 1.1484
```
**Solution**: 
- Check for hardcoded calculations that should use `self.leverage`
- Verify data loading hasn't changed
- Review signal generation logic carefully
- Check for floating point accumulation errors

### API Key Issues
```
ValueError: Missing API key
```
**Solution**: Set environment variable or load from config file:
```python
import os
api_key = os.environ['POLYGON_API_KEY']
```

### Missing Data
```
KeyError: 'ROM' not in data
```
**Solution**: Verify ETF symbols are correct and trading during analysis period.

---

## 🔗 Related Files

For detailed information, see:
- **MODULARIZATION_GUIDE.md** - Architecture and strategy
- **EXTRACTION_GUIDE.md** - Implementation walkthrough
- **IMPLEMENTATION_CHECKLIST.md** - Task tracking
- **ADD_NEW_VARIANT.md** - Extensibility demonstration
- **REFACTORED_NOTEBOOK_TEMPLATE.ipynb** - Notebook template

---

## 📋 Quick Reference - What Goes Where

| Code Element | Original Location | New Location | Status |
|---|---|---|---|
| Signal definitions | Notebooks (hardcoded) | portfolio_config.py | ✅ Done |
| Data loading logic | Notebook cell 2 | portfolio_engine.load_data() | 🔄 To extract |
| Signal generation | Notebook cell 2 | portfolio_engine.generate_signals() | 🔄 To extract |
| Backtesting logic | Notebook cell 2 | portfolio_engine.run_backtest() | 🔄 To extract |
| Metrics calculation | Notebook cell 2 | portfolio_engine.calculate_metrics() | 🔄 To extract |
| Visualization | Notebook cells 3+ | Keep in notebooks | ✅ No change |
| Configuration | Hardcoded in notebook | Passed as parameter | ✅ Done |

---

## 🎓 Learning Outcomes

After completing this modularization project, you'll understand:
1. ✅ How to identify and eliminate code duplication
2. ✅ Configuration management with data structures
3. ✅ Designing reusable analysis engines
4. ✅ Factory patterns for variant management
5. ✅ Code extraction and refactoring strategies
6. ✅ Testing and validation of refactored code

---

## 👥 Contributing

When working on this project:
1. Work through phases in order (don't skip ahead)
2. Use IMPLEMENTATION_CHECKLIST.md to track progress
3. Verify results match originals at each step
4. Commit changes with clear messages
5. Update documentation as you go

---

## 📝 Version History

| Date | Phase | Status |
|------|-------|--------|
| 2024-01-XX | 1 - Configuration | ✅ Complete |
| TBD | 2 - Engine Extraction | 🔄 In Progress |
| TBD | 3 - Notebook Refactoring | ⏳ Pending |
| TBD | 4 - Validation | ⏳ Pending |
| TBD | 5 - Documentation | ✅ Complete |
| TBD | 6 - Deployment | ⏳ Pending |

---

## 📞 Questions?

Refer to appropriate guide:
- **"How do I start?"** → Read MODULARIZATION_GUIDE.md
- **"What exactly needs to be done?"** → Use IMPLEMENTATION_CHECKLIST.md
- **"How do I extract code?"** → Read EXTRACTION_GUIDE.md
- **"Why is this valuable?"** → Read ADD_NEW_VARIANT.md
- **"What should refactored notebook look like?"** → See REFACTORED_NOTEBOOK_TEMPLATE.ipynb

---

**Last Updated**: [Today]  
**Project Status**: Phase 2 in progress  
**Next Milestone**: Complete Core Engine Extraction
