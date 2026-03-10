#!/usr/bin/env python3
"""
Portfolio Backtest Runner
=========================
Execute 1.0x or 1.5x leverage portfolio backtest.
Uses exact signal maps and ETF universe from original notebooks.

Usage:
    python run_portfolio_updated.py 1.0   # Run 1.0x leverage portfolio
    python run_portfolio_updated.py 1.5   # Run 1.5x leverage portfolio
"""

import sys
import pandas as pd
import numpy as np
from signals import (
    signal_1, signal_3, signal_8, signal_9,
    signal_autocorr, signal_entropy, signal_convexity_gap_adjusted,
    signal_run_length, signal_record_rate, signal_time_since_volume_spike,
    signal_return_iqr, signal_burstiness, signal_signed_volume_agreement,
    signal_path_efficiency, signal_vol_of_vol, signal_return_conviction,
    signal_price_volume_phase, signal_vol_compression_ratio,
    signal_liquidity_persistence, signal_vol_drift_imbalance
)
from portfolio_engine import load_price_data, run_period, sharpe, cagr, max_drawdown


# Configuration
POLYGON_API_KEY = 'REMOVED_API_KEY'

TRAIN_START = '2000-01-01'
TRAIN_END = '2015-12-31'
VAL_START = '2016-01-01'
VAL_END = '2021-12-31'
BLIND_START = '2022-01-01'
BLIND_END = '2024-06-30'

# Complete ETF universe (436 ETFs)
ETF_UNIVERSE = [
    "AAXJ", "ACWI", "ACWX", "AGG", "AGQ", "AIA", "AOA", "AOM", "AOR", "BAB",
    "BIL", "BIV", "BLV", "BND", "BSV", "BWX", "CGW", "CMF", "CQQQ", "CWB",
    "CWI", "DBC", "DEM", "DES", "DGS", "DHS", "DIA", "DLN", "DLS", "DON",
    "DSI", "DTD", "DVY", "DXJ", "EDV", "EEM", "EFA", "EFG", "EFV", "EMB",
    "EPI", "EPP", "EPS", "EWA", "EWC", "EWG", "EWJ", "EWL", "EWP", "EWS",
    "EWT", "EWU", "EWW", "EWY", "EWZ", "EXI", "EZU", "FAS", "FBT", "FDL",
    "FDN", "FEX", "FEZ", "FGD", "FIW", "FNX", "FPX", "FTA", "FTC", "FTCS",
    "FVD", "FXH", "FXI", "FXL", "FXO", "FXR", "FXU", "FYX", "GDX", "GDXJ",
    "GLD", "GRID", "GSG", "GSY", "GVI", "HEDJ", "HYD", "HYG", "IAI", "IAU",
    "IBB", "ICF", "ICLN", "IDU", "IDV", "IEF", "IEI", "IEV", "IGF", "IGM",
    "IGOV", "IGV", "IHI", "IJH", "IJJ", "IJK", "IJR", "IJS", "IJT", "ILF",
    "IOO", "ITA", "ITB", "ITM", "ITOT", "IUSG", "IUSV", "IVE", "IVV", "IVW",
    "IWB", "IWC", "IWD", "IWF", "IWL", "IWM", "IWN", "IWO", "IWP", "IWR",
    "IWS", "IWV", "IWX", "IWY", "IXC", "IXJ", "IXN", "IYC", "IYE", "IYF",
    "IYG", "IYH", "IYJ", "IYK", "IYR", "IYW", "IYY", "JNK", "KBE", "KRE",
    "LQD", "MBB", "MDY", "MDYG", "MDYV", "MGC", "MGK", "MGV", "MINT", "MUB",
    "MUNI", "NLR", "NYF", "OEF", "ONEQ", "PCY", "PDP", "PEY", "PFF", "PGX",
    "PHO", "PID", "PKW", "PPA", "PRF", "PRFZ", "PWB", "PWV", "PWZ", "PXF",
    "PXH", "PZA", "QLD", "QQEW", "QQQ", "QQXT", "QTEC", "ROM", "RPG", "RPV",
    "RSP", "RWJ", "RWK", "RWL", "RWO", "RWR", "SCHA", "SCHB", "SCHF", "SCHG",
    "SCHV", "SCHX", "SCZ", "SDY", "SGOL", "SH", "SHM", "SHV", "SHY", "SIVR",
    "SLV", "SLYG", "SLYV", "SMH", "SOXX", "SPAB", "SPHQ", "SPMD", "SPXL", "SPY",
    "SPYG", "SPYV", "SSO", "SUB", "TECL", "TFI", "TIP", "TLH", "TLT", "TMF",
    "TNA", "UPRO", "USD", "USO", "UYG", "VAW", "VB", "VBK", "VBR", "VCIT",
    "VCLT", "VCR", "VCSH", "VDC", "VDE", "VEA", "VEU", "VFH", "VGIT", "VGK",
    "VGLT", "VGSH", "VGT", "VHT", "VIG", "VIS", "VMBS", "VNQ", "VO", "VOE",
    "VOT", "VOX", "VPL", "VPU", "VSS", "VT", "VTI", "VTV", "VUG", "VV",
    "VWO", "VXF", "VYM", "YINN", "ZROZ"
]

# Signal -> ETF mapping (mode 3: signal-centric portfolio using exact original maps)
SIGNAL_MAP = {
    signal_1: ['ROM', 'XLU', 'QQQ', 'SH', 'FDN', 'PCY', 'TNA', 'IYK', 'GRID', 'ITA', 'IDU', 'XOP', 'IGOV', 'BSV', 'CMF', 'HEDJ', 'IGV', 'PXH', 'IWD', 'MUNI', 'VMBS', 'SCZ', 'MDYV', 'DLS', 'BWX', 'PWV', 'RWL', 'SPHQ', 'FTCS', 'BIL'],
    signal_entropy: ['TMF', 'DHS', 'XLV', 'IWC', 'XLK', 'IAI', 'VNQ', 'GDXJ', 'PCY', 'SIVR', 'VPL', 'PFF', 'BWX', 'KRE', 'FTCS', 'VOX', 'PID', 'SGOL', 'XLP', 'CQQQ', 'SPHQ', 'MUB', 'MBB', 'GSY', 'AOM', 'EWP', 'CWB', 'HYD', 'VSS', 'GRID', 'SUB', 'NYF', 'VGSH', 'ITOT', 'VCLT', 'MUNI', 'MINT', 'BIL', 'SHY'],
    signal_8: ['SHM', 'XSD', 'IEF', 'FXU', 'NYF', 'AGG', 'XLV', 'PWZ', 'FXI', 'IXJ', 'VGIT', 'IJH', 'SPYG', 'VMBS', 'MBB', 'BSV'],
    signal_time_since_volume_spike: ['EEM', 'BIV', 'IJS', 'TLT', 'VBR', 'XBI', 'TECL', 'VDC', 'RWL', 'SH', 'VGLT', 'RWO', 'SDY', 'UPRO', 'FXO', 'VSS', 'EWU', 'FGD', 'IEI', 'SLYG', 'TIP', 'VXF', 'SCHX', 'SCHB', 'RWK', 'SCHG', 'CWB', 'VIS', 'QQQ', 'IUSG', 'IUSV', 'IEF', 'HEDJ', 'PWB', 'PHO', 'SCHV', 'PFF', 'SPY', 'AGG', 'FBT', 'VGSH', 'SHV', 'BIL'],
    signal_autocorr: ['IGV', 'XBI', 'SH', 'IJK', 'ITA', 'HYG', 'IYH', 'CQQQ', 'VCR', 'GSY', 'FPX', 'IYC', 'IWX', 'MINT', 'XLY', 'EPS', 'RWL', 'VGIT'],
    signal_path_efficiency: ['FXU', 'ICLN', 'IDU', 'XBI', 'SH', 'FXH', 'GDXJ', 'AAXJ', 'PCY', 'MUB', 'QQXT', 'XLP', 'XLG', 'TFI', 'IWY', 'XLK', 'IYK', 'CQQQ', 'SDY', 'VDC', 'BIL', 'VGSH', 'MGK', 'IEI'],
    signal_burstiness: ['IGV', 'EDV', 'EPP', 'VPU', 'FDN', 'FVD', 'DHS', 'RWL', 'XSD', 'FPX', 'VUG', 'SH', 'DVY', 'PGX', 'RWK', 'VCLT', 'EWL', 'SHM', 'VGT', 'BWX', 'GLD', 'SLYV', 'FNX', 'IGOV', 'IWY', 'XLP', 'IVW', 'FIW', 'IYC', 'HEDJ', 'BIV', 'BIL'],
    signal_signed_volume_agreement: ['VBK', 'FTA', 'FXL', 'GSG', 'IGV', 'MDY', 'SPMD', 'PID', 'RWL', 'UPRO', 'XLP', 'VCR', 'XOP', 'XSD', 'GDXJ', 'VDE', 'TIP', 'PDP', 'CMF', 'SHM', 'IGM', 'TECL', 'BLV', 'BND', 'FTCS', 'EMB', 'VCIT', 'MUB', 'SCHB', 'ITA', 'ITM', 'GVI', 'TFI', 'PWZ', 'BSV', 'VCSH', 'NYF', 'PZA', 'SPHQ', 'SHV', 'AOR'],
    signal_9: ['GDX', 'EWL', 'XBI', 'XLP', 'FNX', 'PZA', 'EWJ', 'VDC', 'FXL', 'VCIT', 'IYK', 'GSY', 'HYD', 'MUB', 'IDU', 'MINT'],
    signal_run_length: ['XLU', 'EWY', 'VAW', 'GLD', 'ITM', 'CMF', 'BIV', 'VPU', 'VYM', 'AOM', 'VDC', 'DXJ', 'XLE', 'SLYV', 'ITA', 'DBC', 'PPA', 'VGLT', 'CWB', 'IWB', 'VHT', 'EMB', 'IHI', 'FVD', 'SPHQ', 'FEX', 'QQXT', 'IGOV', 'VGIT', 'KBE', 'VOT', 'BWX', 'VCLT', 'HYD', 'VMBS', 'PWZ', 'ITOT', 'VCIT', 'FTC', 'XOP', 'SHV', 'VCSH', 'MBB', 'SGOL', 'BIL'],
    signal_record_rate: ['BAB', 'ITB', 'SH', 'RWL', 'SPMD', 'EWY', 'SCZ', 'DBC', 'VSS', 'TLT', 'EPI', 'AIA', 'CQQQ', 'VOX', 'DGS', 'PFF', 'FXU', 'IGOV', 'GLD', 'EDV', 'TIP', 'SHM', 'PWZ', 'DLS', 'NYF', 'MUNI', 'VMBS', 'SUB'],
    signal_return_iqr: ['DEM', 'SH', 'IGOV', 'IDU', 'SMH', 'IXJ', 'SCHF', 'TFI', 'FDL', 'MUB', 'FGD', 'PHO', 'BWX', 'DGS', 'XLY', 'DTD'],
    signal_convexity_gap_adjusted: ['GDX', 'USD', 'TECL', 'EWT', 'FNX', 'VPU', 'DBC', 'VYM', 'CWB', 'MDYV', 'GRID', 'UPRO', 'BWX', 'VMBS', 'SUB', 'EWS', 'SHY', 'VCR', 'SPHQ', 'IUSG', 'SCHG', 'DVY', 'SHV', 'PCY', 'VCSH', 'BIL', 'FVD', 'IWY'],
    signal_3: ['FXU', 'SPAB', 'PZA', 'PGX', 'IAU', 'EWW', 'EWS', 'IXJ', 'IYC', 'ICF', 'XOP', 'HYG', 'IYH', 'SPXL', 'EWZ', 'AAXJ', 'HEDJ', 'CQQQ', 'MBB', 'VMBS', 'TIP', 'MUB', 'DGS', 'PFF', 'AGG', 'GSY', 'FXH', 'FXI', 'IYF', 'IVV', 'FXO', 'BLV', 'VIG', 'ITM', 'GVI', 'IYG', 'IAI', 'FTCS', 'SPY', 'IGV', 'SCHX', 'SCHB', 'DVY', 'VGT', 'FDL', 'IWO', 'IWL', 'FVD', 'VV', 'XLY', 'IWD', 'IEV', 'IVE', 'SDY', 'VHT'],
    signal_vol_of_vol: ['FBT', 'RWJ', 'PGX', 'FTA', 'SH', 'DBC', 'PWB', 'FXL', 'GLD', 'IVW', 'TIP', 'IEI', 'BWX', 'VT', 'VCLT', 'XLV', 'MINT', 'BIL'],
    signal_return_conviction: ['SIVR', 'EWJ', 'GRID', 'SH', 'JNK', 'ACWX', 'IYC', 'IXJ', 'SHM', 'FXU', 'CQQQ', 'TLH', 'VCSH', 'PGX', 'MUNI', 'SUB', 'XLG', 'TFI', 'SHY', 'VMBS', 'VGSH', 'SHV', 'MINT'],
    signal_price_volume_phase: ['SPAB', 'UPRO', 'PWV', 'TNA', 'SLV', 'AGQ', 'IWR', 'VB', 'EWW', 'FIW', 'IJJ', 'BIV', 'AAXJ', 'FAS', 'GLD', 'RPG', 'TLT', 'QTEC', 'PZA', 'CQQQ', 'HYD', 'PDP', 'EWZ', 'VDC', 'RWL', 'KRE', 'SCHX', 'XLG', 'FDN', 'AOR', 'VAW', 'QQQ', 'TECL', 'SMH', 'DES', 'QLD', 'XSD', 'MGC', 'IYH', 'IYC', 'EPI', 'IWC', 'IYK', 'RWJ', 'SOXX', 'BND', 'FBT', 'XLU', 'GSY', 'MUB', 'SHM', 'EFV', 'JNK', 'IJS', 'EFG', 'OEF', 'MUNI', 'SIVR', 'VDE', 'QQXT', 'CMF', 'MINT', 'RSP', 'VFH'],
    signal_vol_compression_ratio: ['FBT', 'PPA', 'XLG', 'SH', 'EWS', 'DXJ', 'XME', 'IYG', 'BIV', 'GLD', 'XLP', 'PWZ', 'TMF', 'BWX', 'SHM', 'VGK', 'SCZ', 'AAXJ', 'HYG', 'SGOL', 'NYF', 'IEV', 'GSY', 'MINT', 'SHV', 'BIL', 'VGIT', 'SUB', 'TLH', 'VMBS'],
    signal_liquidity_persistence: ['RWR', 'FTC', 'EPI', 'RWK', 'RWJ', 'EPS', 'IWN', 'RPV', 'EDV', 'DVY', 'EZU', 'SH', 'FXH', 'BAB', 'SOXX', 'DTD', 'GDXJ', 'UYG', 'SLYG', 'XLP', 'TLH', 'SPMD', 'LQD', 'OEF', 'CMF', 'VT', 'SHM', 'EWP', 'SPYG', 'QQXT', 'VCIT', 'NYF', 'VCLT', 'FEX', 'IGOV', 'MGV', 'IEF', 'VGLT', 'SHV', 'USO'],
    signal_vol_drift_imbalance: ['XBI', 'DGS', 'ICLN', 'EWG', 'DBC', 'DEM', 'IGF', 'VPU', 'MDYV', 'SCZ', 'RWK', 'EMB', 'VOT'],
}


def main():
    """Main entry point for portfolio backtest."""
    
    # Parse command-line argument
    if len(sys.argv) < 2:
        print("Usage: python run_portfolio_updated.py <leverage>")
        print("  <leverage>: 1.0 or 1.5")
        print("\nExample:")
        print("  python run_portfolio_updated.py 1.0   # Run 1.0x leverage")
        print("  python run_portfolio_updated.py 1.5   # Run 1.5x leverage")
        sys.exit(1)
    
    leverage_str = sys.argv[1]
    
    # Validate leverage argument
    try:
        leverage = float(leverage_str)
    except ValueError:
        print(f"Error: Leverage must be a number, got '{leverage_str}'")
        sys.exit(1)
    
    if leverage not in [1.0, 1.5]:
        print(f"Error: Leverage must be 1.0 or 1.5, got {leverage}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"Portfolio Backtest: {leverage:.1f}x Leverage")
    print(f"{'='*70}\n")
    
    print(f"Loading price data for {len(ETF_UNIVERSE)} ETFs...")
    price_data = load_price_data(ETF_UNIVERSE, POLYGON_API_KEY)
    print(f"Data loaded successfully.\n")
    
    print(f"Running backtest with {len(SIGNAL_MAP)} signals...")
    print(f"Signal -> ETF mapping (Mode 3: Signal-centric)")
    print(f"Leverage: {leverage:.1f}x long, 1.0x short\n")
    
    # Run backtest with signal_map (mode 3)
    pnl_full, pos_full, ret_full, ind_pnl_full = run_period(
        TRAIN_START,
        BLIND_END,
        price_data,
        list(SIGNAL_MAP.keys()),  # Signal functions
        signal_map=SIGNAL_MAP,    # Signal -> ETF mapping (mode 3)
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
    print(f"  Total Return:         {total_return:>12.4f} (${total_return:,.0f})")
    print(f"  Final Drawdown:       {final_dd:>12.4f}")
    print(f"  Signals Used:         {len(SIGNAL_MAP):>12}")
    print(f"  ETF Universe:         {len(ETF_UNIVERSE):>12}")
    print(f"  Backtesting Period:   {TRAIN_START} to {BLIND_END}")
    print(f"{'='*70}\n")
    
    # Return success
    return 0


if __name__ == '__main__':
    sys.exit(main())
