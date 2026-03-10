# Modularization Implementation Checklist

## Project: Modularize Portfolio Analysis Code
**Goal**: Eliminate 5000+ lines of code duplication between `Portfolio_1_0xLong.ipynb` and `Portfolio_1_5xLong.ipynb`

**Status**: In Progress ✍️
- ✅ Phase 1 (Configuration): COMPLETE
- 🔄 Phase 2 (Core Engine): IN PROGRESS  
- ⏳ Phase 3 (Notebook Refactoring): PENDING
- ⏳ Phase 4 (Verification & Testing): PENDING

---

## PHASE 1: Configuration Extraction ✅ COMPLETE

- [x] Create `portfolio_config.py` with signal definitions
- [x] Define `SIGNAL_1_0X_LONG` configuration
- [x] Define `SIGNAL_1_5X_LONG` configuration  
- [x] Include `ETF_UNIVERSE_FULL` reference list
- [x] Include bond ETF lists
- [x] Create `get_signal_config()` factory function
- [x] Test imports work correctly

**Status**: All configuration files created and ready to use.

**Files Created**:
- `portfolio_config.py` (120 lines)

---

## PHASE 2: Core Engine Extraction 🔄 IN PROGRESS

### PHASE 2a: Analyze Original Code Structure

- [ ] Open `Portfolio_1_0xLong.ipynb` in text editor
- [ ] Locate main code cell (lines ~5-5227)
- [ ] Copy full cell content to working document
- [ ] Mark section boundaries:
  - [ ] Imports & Constants (lines ~5-50)
  - [ ] Data Loading Functions (lines ~50-500)
  - [ ] Signal Generation Functions (lines ~500-2000)
  - [ ] Backtesting Logic (lines ~2000-3500)
  - [ ] Metrics Calculation (lines ~3500-4500)
  - [ ] Visualization Prep (lines ~4500-5227)

**Estimated effort**: 1-2 hours
**Dependencies**: None (read-only)

### PHASE 2b: Extract Data Loading Functions

- [ ] Copy data loading code from original notebook
- [ ] Create `PortfolioAnalysisEngine.load_data()` method
- [ ] Replace `ETF_UNIVERSE` with `self.etf_universe`
- [ ] Replace hardcoded date ranges with parameters
- [ ] Add docstring explaining parameters and return values
- [ ] Test extraction:
  - [ ] Method loads data successfully
  - [ ] Returns DataFrame with expected structure
  - [ ] Data shape matches original

**Estimated effort**: 2-3 hours
**Success Criteria**: `engine.load_data()` returns identical DataFrame structure to original

### PHASE 2c: Extract Signal Generation Functions

- [ ] Copy signal generation code from original notebook
- [ ] Create helper functions in `portfolio_engine.py`:
  - [ ] `calculate_momentum()`
  - [ ] `calculate_mean_reversion()`
  - [ ] `calculate_combined_signals()`
- [ ] Create `PortfolioAnalysisEngine.generate_signals()` method
- [ ] Replace all global variable references with instance variables
- [ ] Add docstrings
- [ ] Test extraction:
  - [ ] Signals generated for all ETFs
  - [ ] Signal values match original ranges (-1 to 1)
  - [ ] No missing values unexpectedly

**Estimated effort**: 2-3 hours
**Success Criteria**: Generated signals match original in distribution and range

### PHASE 2d: Extract Backtesting Logic

- [ ] Copy backtesting code from original notebook
- [ ] Create `PortfolioAnalysisEngine.run_backtest()` method
- [ ] Ensure leverage is applied correctly:
  - [ ] Use `self.leverage` (1.0 for first variant, 1.5 for second)
  - [ ] Position sizing reflects leverage
- [ ] Extract P&L calculation logic
- [ ] Create `PortfolioAnalysisEngine.calculate_positions()` helper
- [ ] Test extraction:
  - [ ] Positions calculated correctly
  - [ ] P&L matches original
  - [ ] Leverage properly applied (1.5x variant has 50% more exposure)

**Estimated effort**: 2-3 hours
**Success Criteria**: Backtest results match original row-by-row (within floating point tolerance)

### PHASE 2e: Extract Metrics Calculation

- [ ] Copy metrics calculation code from original notebook
- [ ] Create `PortfolioAnalysisEngine.calculate_metrics()` method
- [ ] Extract individual metric functions:
  - [ ] `_calculate_sharpe_ratio()`
  - [ ] `_calculate_sortino_ratio()`
  - [ ] `_calculate_max_drawdown()`
  - [ ] `_calculate_win_rate()`
  - [ ] Others as present in original
- [ ] Add validation for metric ranges
- [ ] Test extraction:
  - [ ] Sharpe ratio matches original
  - [ ] Sortino ratio matches original
  - [ ] All metrics within expected ranges
  - [ ] No NaN or inf values

**Estimated effort**: 1.5-2 hours
**Success Criteria**: All metrics match original to 4 decimal places

### PHASE 2f: Create Main Pipeline Method

- [ ] Create `PortfolioAnalysisEngine.run_full_analysis()` method
- [ ] Method sequence:
  1. Load data
  2. Generate signals
  3. Run backtest
  4. Calculate metrics
  5. Package results dictionary
- [ ] Return structure:
  ```python
  {
      'config': self.config,
      'data': self.data,
      'signals': self.signals,
      'backtest': {
          'positions': pos_df,
          'returns': ret_series,
          'equity_curve': eq_series
      },
      'metrics': {
          'sharpe_ratio': ...,
          'sortino_ratio': ...,
          # ... all metrics
      }
  }
  ```
- [ ] Test pipeline:
  - [ ] Full pipeline runs without errors
  - [ ] Return structure is complete
  - [ ] All data present and valid

**Estimated effort**: 1 hour
**Success Criteria**: Full pipeline runs successfully

### PHASE 2f: Complete Engine Implementation

- [ ] Review `portfolio_engine.py` for completeness
- [ ] Ensure all helper functions present
- [ ] Add comprehensive docstrings to all methods
- [ ] Create type hints for all parameters
- [ ] Add error handling for edge cases
- [ ] Test imports in interactive Python:
  ```python
  from portfolio_config import get_signal_config
  from portfolio_engine import PortfolioAnalysisEngine
  
  config = get_signal_config('1.0x_long')
  engine = PortfolioAnalysisEngine(config)
  results = engine.run_full_analysis()
  ```

**Estimated effort**: 1-2 hours
**Success Criteria**: Engine initializes and runs full analysis

### PHASE 2g: Validate Against Original

- [ ] Compare metrics from engine vs original notebook:
  - [ ] Sharpe ratio: Match to 4 decimals
  - [ ] Sortino ratio: Match to 4 decimals
  - [ ] Max drawdown: Match to 4 decimals
  - [ ] Total return: Match to 4 decimals
  - [ ] Win rate: Exact match
- [ ] Compare equity curves: Plot overlay
  - [ ] 1.0x variant equity curve matches
  - [ ] Visual comparison shows identical curves
- [ ] Compare daily returns distribution
  - [ ] Return statistics match (mean, std, skew, kurtosis)
- [ ] Document any small differences and root causes

**Estimated effort**: 1 hour
**Success Criteria**: All metrics match within acceptable tolerance (<0.0001)

---

## PHASE 3: Notebook Refactoring 🔄 PENDING

### PHASE 3a: Refactor Portfolio_1_0xLong.ipynb

- [ ] Backup original notebook (save as `Portfolio_1_0xLong_ORIGINAL.ipynb`)
- [ ] Step 1: Replace large code cell with imports
  - [ ] Delete lines 5-5227 (the massive code cell)
  - [ ] Create new Cell 2 with imports:
    ```python
    from portfolio_config import get_signal_config
    from portfolio_engine import PortfolioAnalysisEngine
    ```
- [ ] Step 2: Add configuration cell
  - [ ] Create Cell 3:
    ```python
    config = get_signal_config('1.0x_long')
    engine = PortfolioAnalysisEngine(config)
    results = engine.run_full_analysis()
    ```
- [ ] Step 3: Keep all visualization cells (Cells 4+)
  - [ ] Update variable references if needed (e.g., `equity_curve = results['backtest']['equity_curve']`)
- [ ] Verify notebook structure:
  - [ ] Cell 1: Markdown (title/description)
  - [ ] Cell 2: Imports
  - [ ] Cell 3: Configuration & Analysis
  - [ ] Cells 4+: Visualizations
- [ ] Test refactored notebook:
  - [ ] Notebook runs without errors
  - [ ] All cells execute successfully
  - [ ] Results match original

**Estimated effort**: 1-2 hours
**Success Criteria**: Refactored notebook produces identical results with 1/5 the code

### PHASE 3b: Refactor Portfolio_1_5xLong.ipynb

- [ ] Backup original notebook (save as `Portfolio_1_5xLong_ORIGINAL.ipynb`)
- [ ] Repeat steps from Phase 3a with one change:
  - [ ] Use `get_signal_config('1.5x_long')` instead of `'1.0x_long'`
- [ ] Verify all cells are identical to 1.0x except for this one parameter
- [ ] Test refactored notebook:
  - [ ] Notebook runs without errors
  - [ ] Results match original 1.5x notebook
  - [ ] Equity curve shows ~1.5x the volatility/return vs 1.0x

**Estimated effort**: 30 minutes
**Success Criteria**: Only config string differs between the two notebooks

### PHASE 3c: Refactor Quanta_W7.ipynb (if needed)

- [ ] Check if Quanta_W7.ipynb contains duplicated analysis code
- [ ] If yes, repeat refactoring process:
  - [ ] Backup original
  - [ ] Extract into portfolio_engine.py if unique logic
  - [ ] Refactor to use modular components
- [ ] If no, skip this step

**Estimated effort**: Depends on content (0-3 hours)
**Success Criteria**: All portfolio notebooks use modular architecture

---

## PHASE 4: Verification & Testing ⏳ PENDING

### PHASE 4a: Component Testing

- [ ] Test `portfolio_config.py`:
  - [ ] `get_signal_config('1.0x_long')` returns correct dict
  - [ ] `get_signal_config('1.5x_long')` returns correct dict
  - [ ] `get_signal_config('invalid')` raises error
- [ ] Test `portfolio_engine.py`:
  - [ ] `PortfolioAnalysisEngine` initializes without error
  - [ ] Each method returns expected data types
  - [ ] Full pipeline completes successfully

**Estimated effort**: 30 minutes
**Success Criteria**: All components pass unit tests

### PHASE 4b: Integration Testing

- [ ] Run refactored 1.0x notebook:
  - [ ] All cells execute successfully
  - [ ] Final metrics match original
  - [ ] Visualizations display correctly
- [ ] Run refactored 1.5x notebook:
  - [ ] All cells execute successfully
  - [ ] Final metrics match original 1.5x
  - [ ] Results show expected 1.5x leverage effect
- [ ] Compare results side-by-side:
  - [ ] Create comparison table of metrics
  - [ ] Verify 1.5x leverage reflected in volatility and returns

**Estimated effort**: 1 hour
**Success Criteria**: Both refactored notebooks match originals

### PHASE 4c: Performance Testing

- [ ] Benchmark execution time:
  - [ ] Original notebook execution time
  - [ ] Refactored notebook execution time
  - [ ] Document any differences
- [ ] Memory usage analysis:
  - [ ] Compare memory footprint of refactored vs original
  - [ ] Note any improvements or regressions

**Estimated effort**: 30 minutes
**Success Criteria**: Refactored code performs comparably or better

### PHASE 4d: Code Review

- [ ] Review `portfolio_engine.py`:
  - [ ] [ ] All functions have docstrings
  - [ ] [ ] Type hints are present
  - [ ] [ ] Error handling is robust
  - [ ] [ ] Code is readable and well-commented
- [ ] Review refactored notebooks:
  - [ ] Code is minimal and focused on analysis setup
  - [ ] Markdown cells explain purpose clearly
  - [ ] Visualization cells are clean and well-commented

**Estimated effort**: 1 hour
**Success Criteria**: Code meets quality standards

---

## PHASE 5: Documentation & Knowledge Transfer ✓ COMPLETE

- [x] Create `MODULARIZATION_GUIDE.md` - Architecture and strategy overview
- [x] Create `EXTRACTION_GUIDE.md` - Detailed step-by-step extraction instructions
- [x] Create `REFACTORED_NOTEBOOK_TEMPLATE.ipynb` - Template showing refactored structure
- [x] Create this checklist - Project tracking and task organization

**Additional deliverables**:
- [ ] Create `ADD_NEW_VARIANT.md` - Instructions for adding new portfolio variants
- [ ] Create unit test file: `test_portfolio_engine.py`

---

## PHASE 6: Deployment & Cleanup 📋 PENDING

- [ ] Update README.md:
  - [ ] Document new modular structure
  - [ ] Add instructions for running refactored notebooks
  - [ ] Example of adding new variants
- [ ] Organize repository:
  - [ ] Move old original notebooks to `_archive/` folder
  - [ ] Keep backups: `Portfolio_1_0xLong_ORIGINAL.ipynb`, etc.
  - [ ] Document what changed
- [ ] Final cleanup:
  - [ ] Remove any temporary working files
  - [ ] Verify all imports work correctly
  - [ ] Test from a clean environment

**Estimated effort**: 1-2 hours
**Success Criteria**: Repository is clean and well-organized

---

## Summary by Phase

| Phase | Task | Status | Estimated Hours | Actual Hours |
|-------|------|--------|-----------------|--------------|
| 1 | Configuration Extraction | ✅ COMPLETE | 1 | 1 |
| 2a | Analyze Code Structure | ⏳ TODO | 2 | - |
| 2b | Extract Data Loading | ⏳ TODO | 2.5 | - |
| 2c | Extract Signal Generation | ⏳ TODO | 2.5 | - |
| 2d | Extract Backtesting | ⏳ TODO | 2.5 | - |
| 2e | Extract Metrics | ⏳ TODO | 2 | - |
| 2f | Create Pipeline | ⏳ TODO | 1 | - |
| 2g | Engine Completion | ⏳ TODO | 1.5 | - |
| 2h | Validation Testing | ⏳ TODO | 1 | - |
| 3a | Refactor 1.0x Notebook | ⏳ TODO | 1.5 | - |
| 3b | Refactor 1.5x Notebook | ⏳ TODO | 0.5 | - |
| 3c | Refactor Other Notebooks | ⏳ TODO | 2 | - |
| 4a | Component Testing | ⏳ TODO | 0.5 | - |
| 4b | Integration Testing | ⏳ TODO | 1 | - |
| 4c | Performance Testing | ⏳ TODO | 0.5 | - |
| 4d | Code Review | ⏳ TODO | 1 | - |
| 5 | Documentation | ✅ COMPLETE | 2 | 2 |
| 6 | Deployment & Cleanup | ⏳ TODO | 1.5 | - |
| **TOTAL** | **All Tasks** | **~35% Complete** | **~30 hours** | **- hours** |

---

## Key Milestones

1. ✅ **Milestone 1**: Configuration files created and importable
   - Date: [COMPLETED]
   - Status: Ready for Integration

2. 🔄 **Milestone 2**: Core engine complete and validated against original
   - Target Date: [SET WHEN STARTING]
   - Status: Next priority

3. ⏳ **Milestone 3**: Notebooks refactored and producing identical results
   - Target Date: [SET WHEN COMPLETING 2]
   - Status: Blocked on Milestone 2

4. ⏳ **Milestone 4**: Full test suite passing, documentation complete
   - Target Date: [SET WHEN COMPLETING 3]
   - Status: Blocked on Milestone 3

---

## Quick Start - Next Steps

To continue the refactoring:

1. **Read the guides** (you're here!):
   - `MODULARIZATION_GUIDE.md` - Understand the overall architecture
   - `EXTRACTION_GUIDE.md` - Detailed extraction instructions
   - `REFACTORED_NOTEBOOK_TEMPLATE.ipynb` - See what the refactored notebooks should look like

2. **Extract the engine** (Phases 2a-2h):
   - Open original `Portfolio_1_0xLong.ipynb`
   - Copy the large code cell (lines ~5-5227)
   - Follow `EXTRACTION_GUIDE.md` to break it into methods
   - Test against original results

3. **Refactor the notebooks** (Phase 3):
   - Create new Cell 2 with imports
   - Create new Cell 3 with engine initialization
   - Keep visualization cells (update variable references)
   - Test both notebooks

4. **Validate everything** (Phase 4):
   - Run refactored notebooks
   - Compare metrics to originals
   - Ensure results match

5. **Document and deploy** (Phases 5-6):
   - Update README
   - Organize files
   - Final cleanup

---

## Notes & Considerations

- **Backward Compatibility**: Original notebooks should be preserved as backups in case rollback is needed
- **API Keys**: Ensure `POLYGON_API_KEY` is handled securely (environment variable, not hardcoded)
- **Date Ranges**: Make date ranges configurable rather than hardcoded for flexibility
- **Error Handling**: Add try-except blocks for API calls and data validation
- **Dependencies**: Document all required packages (pandas, numpy, polygon-io, etc.)
- **Performance**: Monitor that refactored code doesn't introduce performance regressions
- **Extensibility**: Design to easily support new portfolio variants without code changes

---

## Questions to Ask During Implementation

- What is the exact leverage application method? (Applied at position level? Portfolio level?)
- Are there any hardcoded parameters that should be configurable?
- What date range is being analyzed? Should this be configurable?
- Are there any environment-specific configurations (API keys, data paths)?
- Should the bond allocation be dynamic or fixed?
- How frequently does the signal map need to change?
- Who will be maintaining this code going forward?

---

**Last Updated**: [Today]
**By**: [GitHub Copilot]
**Status**: Ready for Phase 2 Extraction Work
