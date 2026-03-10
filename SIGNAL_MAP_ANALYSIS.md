# SIGNAL_MAP ANALYSIS FOR QUANTA PORTFOLIO

## Portfolio_1_0xLong.ipynb

**Unique Signal Functions:** 19
**Unique ETFs:** 230

### Active Signals:
1. signal_1
2. signal_3
3. signal_8
4. signal_9
5. signal_entropy
6. signal_autocorr
7. signal_path_efficiency
8. signal_burstiness
9. signal_signed_volume_agreement
10. signal_time_since_volume_spike
11. signal_run_length
12. signal_record_rate
13. signal_return_iqr
14. signal_convexity_gap_adjusted
15. signal_vol_of_vol
16. signal_return_conviction
17. signal_price_volume_phase
18. signal_vol_compression_ratio
19. signal_liquidity_persistence

### SIGNAL_MAP Dictionary:

```python
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
}
```

---

## Portfolio_1_5xLong.ipynb

**Unique Signal Functions:** 11
**Unique ETFs:** 142

### Active Signals:
1. signal_entropy
2. signal_8
3. signal_9
4. signal_burstiness
5. signal_record_rate
6. signal_return_iqr
7. signal_convexity_gap_adjusted
8. signal_vol_of_vol
9. signal_return_conviction
10. signal_vol_compression_ratio
11. signal_vol_drift_imbalance

### SIGNAL_MAP Dictionary:

```python
SIGNAL_MAP = {
    signal_entropy: ['TMF', 'DHS', 'XLV', 'IWC', 'XLK', 'IAI', 'VNQ', 'GDXJ', 'PCY', 'SIVR', 'VPL', 'PFF', 'BWX', 'KRE', 'FTCS', 'VOX', 'PID', 'SGOL', 'XLP', 'CQQQ', 'SPHQ', 'MUB', 'MBB', 'GSY', 'AOM', 'EWP', 'CWB', 'HYD', 'VSS', 'GRID', 'SUB', 'NYF', 'VGSH', 'ITOT', 'VCLT', 'MUNI', 'MINT', 'BIL', 'SHY'],
    signal_8: ['SHM', 'XSD', 'IEF', 'FXU', 'NYF', 'AGG', 'XLV', 'PWZ', 'FXI', 'IXJ', 'VGIT', 'IJH', 'SPYG', 'VMBS', 'MBB', 'BSV'],
    signal_burstiness: ['IGV', 'EDV', 'EPP', 'VPU', 'FDN', 'FVD', 'DHS', 'RWL', 'XSD', 'FPX', 'VUG', 'SH', 'DVY', 'PGX', 'RWK', 'VCLT', 'EWL', 'SHM', 'VGT', 'BWX', 'GLD', 'SLYV', 'FNX', 'IGOV', 'IWY', 'XLP', 'IVW', 'FIW', 'IYC', 'HEDJ', 'BIV', 'BIL'],
    signal_9: ['GDX', 'EWL', 'XBI', 'XLP', 'FNX', 'PZA', 'EWJ', 'VDC', 'FXL', 'VCIT', 'IYK', 'GSY', 'HYD', 'MUB', 'IDU', 'MINT'],
    signal_record_rate: ['BAB', 'ITB', 'SH', 'RWL', 'SPMD', 'EWY', 'SCZ', 'DBC', 'VSS', 'TLT', 'EPI', 'AIA', 'CQQQ', 'VOX', 'DGS', 'PFF', 'FXU', 'IGOV', 'GLD', 'EDV', 'TIP', 'SHM', 'PWZ', 'DLS', 'NYF', 'MUNI', 'VMBS', 'SUB'],
    signal_return_iqr: ['DEM', 'SH', 'IGOV', 'IDU', 'SMH', 'IXJ', 'SCHF', 'TFI', 'FDL', 'MUB', 'FGD', 'PHO', 'BWX', 'DGS', 'XLY', 'DTD'],
    signal_convexity_gap_adjusted: ['GDX', 'USD', 'TECL', 'EWT', 'FNX', 'VPU', 'DBC', 'VYM', 'CWB', 'MDYV', 'GRID', 'UPRO', 'BWX', 'VMBS', 'SUB', 'EWS', 'SHY', 'VCR', 'SPHQ', 'IUSG', 'SCHG', 'DVY', 'SHV', 'PCY', 'VCSH', 'BIL', 'FVD', 'IWY'],
    signal_vol_of_vol: ['FBT', 'RWJ', 'PGX', 'FTA', 'SH', 'DBC', 'PWB', 'FXL', 'GLD', 'IVW', 'TIP', 'IEI', 'BWX', 'VT', 'VCLT', 'XLV', 'MINT', 'BIL'],
    signal_return_conviction: ['SIVR', 'EWJ', 'GRID', 'SH', 'JNK', 'ACWX', 'IYC', 'IXJ', 'SHM', 'FXU', 'CQQQ', 'TLH', 'VCSH', 'PGX', 'MUNI', 'SUB', 'XLG', 'TFI', 'SHY', 'VMBS', 'VGSH', 'SHV', 'MINT'],
    signal_vol_compression_ratio: ['FBT', 'PPA', 'XLG', 'SH', 'EWS', 'DXJ', 'XME', 'IYG', 'BIV', 'GLD', 'XLP', 'PWZ', 'TMF', 'BWX', 'SHM', 'VGK', 'SCZ', 'AAXJ', 'HYG', 'SGOL', 'NYF', 'IEV', 'GSY', 'MINT', 'SHV', 'BIL', 'VGIT', 'SUB', 'TLH', 'VMBS'],
    signal_vol_drift_imbalance: ['XBI', 'DGS', 'ICLN', 'EWG', 'DBC', 'DEM', 'IGF', 'VPU', 'MDYV', 'SCZ', 'RWK', 'EMB', 'VOT'],
}
```

---

## Key Differences

### Signals Used in 1.0x Portfolio (19):
- signal_1, signal_3, signal_8, signal_9, signal_entropy, signal_autocorr, signal_path_efficiency, signal_burstiness, signal_signed_volume_agreement, signal_time_since_volume_spike, signal_run_length, signal_record_rate, signal_return_iqr, signal_convexity_gap_adjusted, signal_vol_of_vol, signal_return_conviction, signal_price_volume_phase, signal_vol_compression_ratio, signal_liquidity_persistence

### Signals Used in 1.5x Portfolio (11):
- signal_entropy, signal_8, signal_9, signal_burstiness, signal_record_rate, signal_return_iqr, signal_convexity_gap_adjusted, signal_vol_of_vol, signal_return_conviction, signal_vol_compression_ratio, signal_vol_drift_imbalance

### Signals Only in 1.0x (9):
- signal_1, signal_3, signal_autocorr, signal_liquidity_persistence, signal_path_efficiency, signal_price_volume_phase, signal_run_length, signal_signed_volume_agreement, signal_time_since_volume_spike

### Signals Only in 1.5x (1):
- signal_vol_drift_imbalance

### Signals in Both (10):
- signal_8, signal_9, signal_burstiness, signal_convexity_gap_adjusted, signal_entropy, signal_record_rate, signal_return_conviction, signal_return_iqr, signal_vol_compression_ratio, signal_vol_of_vol

---

## Summary

| Metric | Portfolio 1.0x | Portfolio 1.5x |
|--------|---|---|
| **Unique Signals** | 19 | 11 |
| **Unique ETFs** | 230 | 142 |
| **Shared Signals** | 10 | 10 |
| **Unique to Portfolio** | 9 | 1 |

**Note:** The 1.5x portfolio is more conservative with fewer signals and a smaller ETF universe, while the 1.0x (market-neutral) portfolio uses a broader set of signals and more ETFs for greater diversification.
