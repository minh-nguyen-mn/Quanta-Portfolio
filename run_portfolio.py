#!/usr/bin/env python3
"""
Portfolio Backtest Runner
=========================
Execute 1.0x or 1.5x leverage portfolio backtest with portfolio-specific configurations.

Usage:
    python run_portfolio.py 1.0   # Run 1.0x leverage portfolio (19 signals, 230 ETFs)
    python run_portfolio.py 1.5   # Run 1.5x leverage portfolio (11 signals, 142 ETFs)
"""

import sys
import pandas as pd
import numpy as np
from signals import _SIGNAL_REGISTRY
from portfolio_engine import load_price_data, run_period, sharpe, cagr, max_drawdown


# Configuration
POLYGON_API_KEY = 'REMOVED_API_KEY'

TRAIN_START = '2000-01-01'
TRAIN_END = '2015-12-31'
VAL_START = '2016-01-01'
VAL_END = '2021-12-31'
BLIND_START = '2022-01-01'
BLIND_END = '2025-06-30'

# Portfolio 1.0x Long: 19 signals, 230 ETFs
SIGNAL_MAP_1_0X_STRINGS = {
    'signal_1': ['ROM', 'XLU', 'QQQ', 'SH', 'FDN', 'PCY', 'TNA', 'IYK', 'GRID', 'ITA', 'IDU', 'XOP', 'IGOV', 'BSV', 'CMF', 'HEDJ', 'IGV', 'PXH', 'IWD', 'MUNI', 'VMBS', 'SCZ', 'MDYV', 'DLS', 'BWX', 'PWV', 'RWL', 'SPHQ', 'FTCS', 'BIL'],
    'signal_3': ['FXU', 'SPAB', 'PZA', 'PGX', 'IAU', 'EWW', 'EWS', 'IXJ', 'IYC', 'ICF', 'XOP', 'HYG', 'IYH', 'SPXL', 'EWZ', 'AAXJ', 'HEDJ', 'CQQQ', 'MBB', 'VMBS', 'TIP', 'MUB', 'DGS', 'PFF', 'AGG', 'GSY', 'FXH', 'FXI', 'IYF', 'IVV', 'FXO', 'BLV', 'VIG', 'ITM', 'GVI', 'IYG', 'IAI', 'FTCS', 'SPY', 'IGV', 'SCHX', 'SCHB', 'DVY', 'VGT', 'FDL', 'IWO', 'IWL', 'FVD', 'VV', 'XLY', 'IWD', 'IEV', 'IVE', 'SDY', 'VHT'],
    'signal_8': ['SHM', 'XSD', 'IEF', 'FXU', 'NYF', 'AGG', 'XLV', 'PWZ', 'FXI', 'IXJ', 'VGIT', 'IJH', 'SPYG', 'VMBS', 'MBB', 'BSV'],
    'signal_9': ['GDX', 'EWL', 'XBI', 'XLP', 'FNX', 'PZA', 'EWJ', 'VDC', 'FXL', 'VCIT', 'IYK', 'GSY', 'HYD', 'MUB', 'IDU', 'MINT'],
    'signal_entropy': ['TMF', 'DHS', 'XLV', 'IWC', 'XLK', 'IAI', 'VNQ', 'GDXJ', 'PCY', 'SIVR', 'VPL', 'PFF', 'BWX', 'KRE', 'FTCS', 'VOX', 'PID', 'SGOL', 'XLP', 'CQQQ', 'SPHQ', 'MUB', 'MBB', 'GSY', 'AOM', 'EWP', 'CWB', 'HYD', 'VSS', 'GRID', 'SUB', 'NYF', 'VGSH', 'ITOT', 'VCLT', 'MUNI', 'MINT', 'BIL', 'SHY'],
    'signal_autocorr': ['IGV', 'XBI', 'SH', 'IJK', 'ITA', 'HYG', 'IYH', 'CQQQ', 'VCR', 'GSY', 'FPX', 'IYC', 'IWX', 'MINT', 'XLY', 'EPS', 'RWL', 'VGIT'],
    'signal_path_efficiency': ['FXU', 'ICLN', 'IDU', 'XBI', 'SH', 'FXH', 'GDXJ', 'AAXJ', 'PCY', 'MUB', 'QQXT', 'XLP', 'XLG', 'TFI', 'IWY', 'XLK', 'IYK', 'CQQQ', 'SDY', 'VDC', 'BIL', 'VGSH', 'MGK', 'IEI'],
    'signal_burstiness': ['IGV', 'EDV', 'EPP', 'VPU', 'FDN', 'FVD', 'DHS', 'RWL', 'XSD', 'FPX', 'VUG', 'SH', 'DVY', 'PGX', 'RWK', 'VCLT', 'EWL', 'SHM', 'VGT', 'BWX', 'GLD', 'SLYV', 'FNX', 'IGOV', 'IWY', 'XLP', 'IVW', 'FIW', 'IYC', 'HEDJ', 'BIV', 'BIL'],
    'signal_signed_volume_agreement': ['VBK', 'FTA', 'FXL', 'GSG', 'IGV', 'MDY', 'SPMD', 'PID', 'RWL', 'UPRO', 'XLP', 'VCR', 'XOP', 'XSD', 'GDXJ', 'VDE', 'TIP', 'PDP', 'CMF', 'SHM', 'IGM', 'TECL', 'BLV', 'BND', 'FTCS', 'EMB', 'VCIT', 'MUB', 'SCHB', 'ITA', 'ITM', 'GVI', 'TFI', 'PWZ', 'BSV', 'VCSH', 'NYF', 'PZA', 'SPHQ', 'SHV', 'AOR'],
    'signal_time_since_volume_spike': ['EEM', 'BIV', 'IJS', 'TLT', 'VBR', 'XBI', 'TECL', 'VDC', 'RWL', 'SH', 'VGLT', 'RWO', 'SDY', 'UPRO', 'FXO', 'VSS', 'EWU', 'FGD', 'IEI', 'SLYG', 'TIP', 'VXF', 'SCHX', 'SCHB', 'RWK', 'SCHG', 'CWB', 'VIS', 'QQQ', 'IUSG', 'IUSV', 'IEF', 'HEDJ', 'PWB', 'PHO', 'SCHV', 'PFF', 'SPY', 'AGG', 'FBT', 'VGSH', 'SHV', 'BIL'],
    'signal_run_length': ['XLU', 'EWY', 'VAW', 'GLD', 'ITM', 'CMF', 'BIV', 'VPU', 'VYM', 'AOM', 'VDC', 'DXJ', 'XLE', 'SLYV', 'ITA', 'DBC', 'PPA', 'VGLT', 'CWB', 'IWB', 'VHT', 'EMB', 'IHI', 'FVD', 'SPHQ', 'FEX', 'QQXT', 'IGOV', 'VGIT', 'KBE', 'VOT', 'BWX', 'VCLT', 'HYD', 'VMBS', 'PWZ', 'ITOT', 'VCIT', 'FTC', 'XOP', 'SHV', 'VCSH', 'MBB', 'SGOL', 'BIL'],
    'signal_record_rate': ['BAB', 'ITB', 'SH', 'RWL', 'SPMD', 'EWY', 'SCZ', 'DBC', 'VSS', 'TLT', 'EPI', 'AIA', 'CQQQ', 'VOX', 'DGS', 'PFF', 'FXU', 'IGOV', 'GLD', 'EDV', 'TIP', 'SHM', 'PWZ', 'DLS', 'NYF', 'MUNI', 'VMBS', 'SUB'],
    'signal_return_iqr': ['DEM', 'SH', 'IGOV', 'IDU', 'SMH', 'IXJ', 'SCHF', 'TFI', 'FDL', 'MUB', 'FGD', 'PHO', 'BWX', 'DGS', 'XLY', 'DTD'],
    'signal_convexity_gap_adjusted': ['GDX', 'USD', 'TECL', 'EWT', 'FNX', 'VPU', 'DBC', 'VYM', 'CWB', 'MDYV', 'GRID', 'UPRO', 'BWX', 'VMBS', 'SUB', 'EWS', 'SHY', 'VCR', 'SPHQ', 'IUSG', 'SCHG', 'DVY', 'SHV', 'PCY', 'VCSH', 'BIL', 'FVD', 'IWY'],
    'signal_vol_of_vol': ['FBT', 'RWJ', 'PGX', 'FTA', 'SH', 'DBC', 'PWB', 'FXL', 'GLD', 'IVW', 'TIP', 'IEI', 'BWX', 'VT', 'VCLT', 'XLV', 'MINT', 'BIL'],
    'signal_return_conviction': ['SIVR', 'EWJ', 'GRID', 'SH', 'JNK', 'ACWX', 'IYC', 'IXJ', 'SHM', 'FXU', 'CQQQ', 'TLH', 'VCSH', 'PGX', 'MUNI', 'SUB', 'XLG', 'TFI', 'SHY', 'VMBS', 'VGSH', 'SHV', 'MINT'],
    'signal_price_volume_phase': ['SPAB', 'UPRO', 'PWV', 'TNA', 'SLV', 'AGQ', 'IWR', 'VB', 'EWW', 'FIW', 'IJJ', 'BIV', 'AAXJ', 'FAS', 'GLD', 'RPG', 'TLT', 'QTEC', 'PZA', 'CQQQ', 'HYD', 'PDP', 'EWZ', 'VDC', 'RWL', 'KRE', 'SCHX', 'XLG', 'FDN', 'AOR', 'VAW', 'QQQ', 'TECL', 'SMH', 'DES', 'QLD', 'XSD', 'MGC', 'IYH', 'IYC', 'EPI', 'IWC', 'IYK', 'RWJ', 'SOXX', 'BND', 'FBT', 'XLU', 'GSY', 'MUB', 'SHM', 'EFV', 'JNK', 'IJS', 'EFG', 'OEF', 'MUNI', 'SIVR', 'VDE', 'QQXT', 'CMF', 'MINT', 'RSP', 'VFH'],
    'signal_vol_compression_ratio': ['FBT', 'PPA', 'XLG', 'SH', 'EWS', 'DXJ', 'XME', 'IYG', 'BIV', 'GLD', 'XLP', 'PWZ', 'TMF', 'BWX', 'SHM', 'VGK', 'SCZ', 'AAXJ', 'HYG', 'SGOL', 'NYF', 'IEV', 'GSY', 'MINT', 'SHV', 'BIL', 'VGIT', 'SUB', 'TLH', 'VMBS'],
    'signal_liquidity_persistence': ['RWR', 'FTC', 'EPI', 'RWK', 'RWJ', 'EPS', 'IWN', 'RPV', 'EDV', 'DVY', 'EZU', 'SH', 'FXH', 'BAB', 'SOXX', 'DTD', 'GDXJ', 'UYG', 'SLYG', 'XLP', 'TLH', 'SPMD', 'LQD', 'OEF', 'CMF', 'VT', 'SHM', 'EWP', 'SPYG', 'QQXT', 'VCIT', 'NYF', 'VCLT', 'FEX', 'IGOV', 'MGV', 'IEF', 'VGLT', 'SHV', 'USO'],
}

# Portfolio 1.5x Long: 11 signals, 142 ETFs
SIGNAL_MAP_1_5X_STRINGS = {
    'signal_entropy': ['TMF', 'DHS', 'XLV', 'IWC', 'XLK', 'IAI', 'VNQ', 'GDXJ', 'PCY', 'SIVR', 'VPL', 'PFF', 'BWX', 'KRE', 'FTCS', 'VOX', 'PID', 'SGOL', 'XLP', 'CQQQ', 'SPHQ', 'MUB', 'MBB', 'GSY', 'AOM', 'EWP', 'CWB', 'HYD', 'VSS', 'GRID', 'SUB', 'NYF', 'VGSH', 'ITOT', 'VCLT', 'MUNI', 'MINT', 'BIL', 'SHY'],
    'signal_8': ['SHM', 'XSD', 'IEF', 'FXU', 'NYF', 'AGG', 'XLV', 'PWZ', 'FXI', 'IXJ', 'VGIT', 'IJH', 'SPYG', 'VMBS', 'MBB', 'BSV'],
    'signal_9': ['GDX', 'EWL', 'XBI', 'XLP', 'FNX', 'PZA', 'EWJ', 'VDC', 'FXL', 'VCIT', 'IYK', 'GSY', 'HYD', 'MUB', 'IDU', 'MINT'],
    'signal_burstiness': ['IGV', 'EDV', 'EPP', 'VPU', 'FDN', 'FVD', 'DHS', 'RWL', 'XSD', 'FPX', 'VUG', 'SH', 'DVY', 'PGX', 'RWK', 'VCLT', 'EWL', 'SHM', 'VGT', 'BWX', 'GLD', 'SLYV', 'FNX', 'IGOV', 'IWY', 'XLP', 'IVW', 'FIW', 'IYC', 'HEDJ', 'BIV', 'BIL'],
    'signal_record_rate': ['BAB', 'ITB', 'SH', 'RWL', 'SPMD', 'EWY', 'SCZ', 'DBC', 'VSS', 'TLT', 'EPI', 'AIA', 'CQQQ', 'VOX', 'DGS', 'PFF', 'FXU', 'IGOV', 'GLD', 'EDV', 'TIP', 'SHM', 'PWZ', 'DLS', 'NYF', 'MUNI', 'VMBS', 'SUB'],
    'signal_return_iqr': ['DEM', 'SH', 'IGOV', 'IDU', 'SMH', 'IXJ', 'SCHF', 'TFI', 'FDL', 'MUB', 'FGD', 'PHO', 'BWX', 'DGS', 'XLY', 'DTD'],
    'signal_convexity_gap_adjusted': ['GDX', 'USD', 'TECL', 'EWT', 'FNX', 'VPU', 'DBC', 'VYM', 'CWB', 'MDYV', 'GRID', 'UPRO', 'BWX', 'VMBS', 'SUB', 'EWS', 'SHY', 'VCR', 'SPHQ', 'IUSG', 'SCHG', 'DVY', 'SHV', 'PCY', 'VCSH', 'BIL', 'FVD', 'IWY'],
    'signal_vol_of_vol': ['FBT', 'RWJ', 'PGX', 'FTA', 'SH', 'DBC', 'PWB', 'FXL', 'GLD', 'IVW', 'TIP', 'IEI', 'BWX', 'VT', 'VCLT', 'XLV', 'MINT', 'BIL'],
    'signal_return_conviction': ['SIVR', 'EWJ', 'GRID', 'SH', 'JNK', 'ACWX', 'IYC', 'IXJ', 'SHM', 'FXU', 'CQQQ', 'TLH', 'VCSH', 'PGX', 'MUNI', 'SUB', 'XLG', 'TFI', 'SHY', 'VMBS', 'VGSH', 'SHV', 'MINT'],
    'signal_vol_compression_ratio': ['FBT', 'PPA', 'XLG', 'SH', 'EWS', 'DXJ', 'XME', 'IYG', 'BIV', 'GLD', 'XLP', 'PWZ', 'TMF', 'BWX', 'SHM', 'VGK', 'SCZ', 'AAXJ', 'HYG', 'SGOL', 'NYF', 'IEV', 'GSY', 'MINT', 'SHV', 'BIL', 'VGIT', 'SUB', 'TLH', 'VMBS'],
    'signal_vol_drift_imbalance': ['XBI', 'DGS', 'ICLN', 'EWG', 'DBC', 'DEM', 'IGF', 'VPU', 'MDYV', 'SCZ', 'RWK', 'EMB', 'VOT'],
}


def convert_signal_map_strings_to_functions(signal_map_strings):
    """Convert signal map with string keys to signal map with function keys."""
    signal_map = {}
    for signal_name, etf_list in signal_map_strings.items():
        if signal_name in _SIGNAL_REGISTRY:
            signal_fn = _SIGNAL_REGISTRY[signal_name]
            signal_map[signal_fn] = etf_list
        else:
            print(f"Warning: Signal '{signal_name}' not found in registry")
    return signal_map


def main():
    """Main entry point for portfolio backtest."""
    
    # Parse command-line argument
    if len(sys.argv) < 2:
        print("Usage: python run_portfolio.py <leverage>  [--reload]")
        print("  <leverage>: 1.0 or 1.5")
        print("  --reload : force reload all ETF data (ignore cache)")
        print("\nExample:")
        print("  python run_portfolio.py 1.0   # Run 1.0x leverage (19 signals, 230 ETFs)")
        print("  python run_portfolio.py 1.5   # Run 1.5x leverage (11 signals, 142 ETFs)")
        sys.exit(1)
    
    leverage_str = sys.argv[1]
    force_reload = "--reload" in sys.argv
    
    # Validate leverage argument
    try:
        leverage = float(leverage_str)
    except ValueError:
        print(f"Error: Leverage must be a number, got '{leverage_str}'")
        sys.exit(1)
    
    if leverage not in [1.0, 1.5]:
        print(f"Error: Leverage must be 1.0 or 1.5, got {leverage}")
        sys.exit(1)
    
    # Select portfolio-specific configuration
    if leverage == 1.0:
        signal_map_strings = SIGNAL_MAP_1_0X_STRINGS
        num_signals = 19
        num_etfs = 230
    else:  # leverage == 1.5
        signal_map_strings = SIGNAL_MAP_1_5X_STRINGS
        num_signals = 11
        num_etfs = 142
    
    print(f"\n{'='*70}")
    print(f"Portfolio Backtest: {leverage:.1f}x Long, 1.0x Short Leverage")
    print(f"{'='*70}")
    print(f"Configuration: {num_signals} signals, {num_etfs} ETFs")
    print(f"{'='*70}\n")

    print(f"Cache reload: {'YES' if force_reload else 'NO'}\n")

    # Convert signal map strings to functions
    print(f"Loading signal registry...")
    signal_map = convert_signal_map_strings_to_functions(signal_map_strings)
    print(f"Loaded {len(signal_map)} signal functions.\n")
    
    # Build ETF universe from signal map
    etf_universe = sorted({etf for etf_list in signal_map_strings.values() for etf in etf_list})
    print(f"ETF Universe: {len(etf_universe)} ETFs\n")
    
    print(f"Loading price data for {len(etf_universe)} ETFs...")
    price_data = load_price_data(
        etf_universe,
        POLYGON_API_KEY,
        force_reload=force_reload
    )
    print(f"Data loaded successfully.\n")
    
    print(f"Running backtest...")
    print(f"  Period: {TRAIN_START} to {BLIND_END}")
    print(f"  Long Leverage: {leverage:.1f}x")
    print(f"  Short Leverage: 1.0x\n")
    
    # Run backtest with portfolio-specific signal map
    pnl_full, pos_full, ret_full, ind_pnl_full = run_period(
        TRAIN_START,
        BLIND_END,
        price_data,
        list(signal_map.keys()),  # Signal functions list (not used in Mode 3)
        signal_map=signal_map,    # Signal-to-ETF mapping (Mode 3)
        etf_universe=etf_universe,
        long_leverage=leverage,
        short_leverage=1.0
    )
    
    print("Backtest completed. Calculating metrics...\n")
    
    # Extract periods
    pnl_train = pnl_full.loc[TRAIN_START:TRAIN_END]
    pnl_val = pnl_full.loc[VAL_START:VAL_END]
    pnl_blind = pnl_full.loc[BLIND_START:BLIND_END]
    pnl_trainval = pnl_full.loc[TRAIN_START:VAL_END]
    
    # Calculate metrics
    train_sharpe = sharpe(pnl_train)
    val_sharpe = sharpe(pnl_val)
    blind_sharpe = sharpe(pnl_blind)
    trainval_sharpe = sharpe(pnl_trainval)
    full_sharpe = sharpe(pnl_full)
    
    train_cagr = cagr(pnl_train)
    val_cagr = cagr(pnl_val)
    blind_cagr = cagr(pnl_blind)
    
    train_mdd = max_drawdown(pnl_train)
    val_mdd = max_drawdown(pnl_val)
    blind_mdd = max_drawdown(pnl_blind)
    
    # Display results
    print(f"{'='*70}")
    print(f"RESULTS — {leverage:.1f}x Leverage Portfolio")
    print(f"{'='*70}\n")
    
    print(f"{'TRAIN PERIOD':30} ({TRAIN_START} to {TRAIN_END})")
    print(f"  Sharpe Ratio:   {train_sharpe:>12.4f}")
    print(f"  CAGR:           {train_cagr:>12.4f}")
    print(f"  Max Drawdown:   {train_mdd:>12.4f}\n")
    
    print(f"{'VALIDATION PERIOD':30} ({VAL_START} to {VAL_END})")
    print(f"  Sharpe Ratio:   {val_sharpe:>12.4f}")
    print(f"  CAGR:           {val_cagr:>12.4f}")
    print(f"  Max Drawdown:   {val_mdd:>12.4f}\n")
    
    print(f"{'BLIND PERIOD':30} ({BLIND_START} to {BLIND_END})")
    print(f"  Sharpe Ratio:   {blind_sharpe:>12.4f}")
    print(f"  CAGR:           {blind_cagr:>12.4f}")
    print(f"  Max Drawdown:   {blind_mdd:>12.4f}\n")
    
    print(f"{'TRAIN + VALIDATION':30}")
    print(f"  Sharpe Ratio:   {trainval_sharpe:>12.4f}\n")
    
    print(f"{'FULL PERIOD':30}")
    print(f"  Sharpe Ratio:   {full_sharpe:>12.4f}\n")
    
    # Summary stats
    total_return = pnl_full.iloc[-1]
    equity_high = pnl_full.cummax().iloc[-1]
    if equity_high > 0:
        final_dd = (pnl_full.iloc[-1] - equity_high) / equity_high
    else:
        final_dd = 0
    
    print(f"{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"  Signals Used:         {len(signal_map):>12} (portfolio-specific)")
    print(f"  ETFs Used:            {len(etf_universe):>12} (portfolio-specific)")
    print(f"  Total Return:         {total_return:>12.4f} (${total_return:,.0f})")
    print(f"  Final Drawdown:       {final_dd:>12.4f}")
    print(f"  Backtesting Period:   {TRAIN_START} to {BLIND_END}")
    print(f"{'='*70}\n")
    
    # Return success
    return 0


if __name__ == '__main__':
    sys.exit(main())
