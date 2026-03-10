"""
Signal map configurations for different portfolio variants.
Each configuration defines the ETF universe and parameters for a specific portfolio strategy.
"""

# =========================
# SIGNAL MAPS BY PORTFOLIO
# =========================

# Portfolio 1.0x Long Signal Map
SIGNAL_1_0X_LONG = {
    'name': '1.0x Long Portfolio',
    'leverage': 1.0,
    'etf_universe': [
        'ROM', 'QQQ', 'XLU', 'GRID', 'EWT', 'BWX', 'IDU', 'PXH', 'CMF', 'IYK', 
        'IGOV', 'SPYG', 'SCZ', 'ACWI', 'RPV', 'HEDJ', 'BSV', 'EPS', 'MUNI', 'IVW', 'ITA'
    ],
    'bond_etfs': [
        'AGG', 'BAB', 'BIL', 'BIV', 'BLV', 'BND', 'BSV', 'BWX', 'CMF', 'CWB', 'EDV', 'EMB',
        'GOVI', 'GSY', 'GVI', 'HYD', 'HYG', 'IEF', 'IEI', 'IGIB', 'IGLB', 'IGOV', 'IGSB',
        'ITM', 'JNK', 'LQD', 'MBB', 'MINT', 'MUB', 'MUNI', 'NYF', 'PCY', 'PWZ', 'PZA', 'SHM',
        'SHV', 'SHY', 'SPAB', 'SPIB', 'SPIP', 'SPLB', 'SPMB', 'SPSB', 'SPTI', 'SPTL', 'SUB',
        'TFI', 'TIP', 'TLH', 'TLT', 'TMF', 'USIG', 'VCIT', 'VCLT', 'VCSH', 'VGIT', 'VGLT',
        'VGSH', 'VMBS', 'ZROZ'
    ]
}

# Portfolio 1.5x Long Signal Map
SIGNAL_1_5X_LONG = {
    'name': '1.5x Long Portfolio',
    'leverage': 1.5,
    'etf_universe': [
        'ROM', 'QQQ', 'XLU', 'GRID', 'EWT', 'BWX', 'IDU', 'PXH', 'CMF', 'IYK',
        'IGOV', 'SPYG', 'SCZ', 'ACWI', 'RPV', 'HEDJ', 'BSV', 'EPS', 'MUNI', 'IVW', 'ITA'
    ],
    'bond_etfs': [
        'AGG', 'BAB', 'BIL', 'BIV', 'BLV', 'BND', 'BSV', 'BWX', 'CMF', 'CWB', 'EDV', 'EMB',
        'GOVI', 'GSY', 'GVI', 'HYD', 'HYG', 'IEF', 'IEI', 'IGIB', 'IGLB', 'IGOV', 'IGSB',
        'ITM', 'JNK', 'LQD', 'MBB', 'MINT', 'MUB', 'MUNI', 'NYF', 'PCY', 'PWZ', 'PZA', 'SHM',
        'SHV', 'SHY', 'SPAB', 'SPIB', 'SPIP', 'SPLB', 'SPMB', 'SPSB', 'SPTI', 'SPTL', 'SUB',
        'TFI', 'TIP', 'TLH', 'TLT', 'TMF', 'USIG', 'VCIT', 'VCLT', 'VCSH', 'VGIT', 'VGLT',
        'VGSH', 'VMBS', 'ZROZ'
    ]
}

# Full ETF Universe (for reference/testing)
ETF_UNIVERSE_FULL = [
    'AAXJ', 'ACWI', 'ACWX', 'AGG', 'AGQ', 'AIA', 'AOA', 'AOM', 'AOR', 'BAB',
    'BIL', 'BIV', 'BLV', 'BND', 'BSV', 'BWX', 'CGW', 'CMF', 'CQQQ', 'CWB',
    'CWI', 'DBC', 'DEM', 'DES', 'DGS', 'DHS', 'DIA', 'DLN', 'DLS', 'DON',
    'DSI', 'DTD', 'DVY', 'DXJ', 'EDV', 'EEM', 'EFA', 'EFG', 'EFV', 'EMB',
    'EPI', 'EPP', 'EPS', 'EWA', 'EWC', 'EWG', 'EWJ', 'EWL', 'EWP', 'EWS',
    'EWT', 'EWU', 'EWW', 'EWY', 'EWZ', 'EXI', 'EZU', 'FAS', 'FBT', 'FDL',
    'FDN', 'FEX', 'FEZ', 'FGD', 'FIW', 'FNX', 'FPX', 'FTA', 'FTC', 'FTCS',
    'FVD', 'FXH', 'FXI', 'FXL', 'FXO', 'FXR', 'FXU', 'FYX', 'GDX', 'GDXJ',
    'GLD', 'GRID', 'GSG', 'GSY', 'GVI', 'HEDJ', 'HYD', 'HYG', 'IAI', 'IAU',
    'IBB', 'ICF', 'ICLN', 'IDU', 'IDV', 'IEF', 'IEI', 'IEV', 'IGF', 'IGM',
    'IGOV', 'IGV', 'IHI', 'IJH', 'IJJ', 'IJK', 'IJR', 'IJS', 'IJT', 'ILF',
    'IOO', 'ITA', 'ITB', 'ITM', 'ITOT', 'IUSG', 'IUSV', 'IVE', 'IVV', 'IVW',
    'IWB', 'IWC', 'IWD', 'IWF', 'IWL', 'IWM', 'IWN', 'IWO', 'IWP', 'IWR',
    'IWS', 'IWV', 'IWX', 'IWY', 'IXC', 'IXJ', 'IXN', 'IYC', 'IYE', 'IYF',
    'IYG', 'IYH', 'IYJ', 'IYK', 'IYR', 'IYW', 'IYY', 'JNK', 'KBE', 'KRE',
    'LQD', 'MBB', 'MDY', 'MDYG', 'MDYV', 'MGC', 'MGK', 'MGV', 'MINT', 'MUB',
    'MUNI', 'NLR', 'NYF', 'OEF', 'ONEQ', 'PCY', 'PDP', 'PEY', 'PFF', 'PGX',
    'PHO', 'PID', 'PKW', 'PPA', 'PRF', 'PRFZ', 'PWB', 'PWV', 'PWZ', 'PXF',
    'PXH', 'PZA', 'QLD', 'QQEW', 'QQQ', 'QQXT', 'QTEC', 'ROM', 'RPG', 'RPV',
    'RSP', 'RWJ', 'RWK', 'RWL', 'RWO', 'RWR', 'SCHA', 'SCHB', 'SCHF', 'SCHG',
    'SCHV', 'SCHX', 'SCZ', 'SDY', 'SGOL', 'SH', 'SHM', 'SHV', 'SHY', 'SIVR',
    'SLV', 'SLYG', 'SLYV', 'SMH', 'SOXX', 'SPAB', 'SPHQ', 'SPMD', 'SPXL', 'SPY',
    'SPYG', 'SPYV', 'SSO', 'SUB', 'TECL', 'TFI', 'TIP', 'TLH', 'TLT', 'TMF',
    'TNA', 'UPRO', 'USD', 'USO', 'UYG', 'VAW', 'VB', 'VBK', 'VBR', 'VCIT',
    'VCLT', 'VCR', 'VCSH', 'VDC', 'VDE', 'VEA', 'VEU', 'VFH', 'VGIT', 'VGK',
    'VGLT', 'VGSH', 'VGT', 'VHT', 'VIG', 'VIS', 'VMBS', 'VNQ', 'VO', 'VOE',
    'VOT', 'VOX', 'VPL', 'VPU', 'VSS', 'VT', 'VTI', 'VTV', 'VUG', 'VV',
    'VWO', 'VXF', 'VYM', 'XBI', 'XHB', 'XLB', 'XLE', 'XLF', 'XLG', 'XLI',
    'XLK', 'XLP', 'XLU', 'XLV', 'XLY', 'XME', 'XOP', 'XSD', 'YINN', 'ZROZ'
]


def get_signal_config(portfolio_variant: str) -> dict:
    """
    Retrieve the signal configuration for a given portfolio variant.
    
    Args:
        portfolio_variant: String identifier for the portfolio variant
                          ('1.0x_long', '1.5x_long', etc.)
    
    Returns:
        Dictionary containing 'name', 'leverage', 'etf_universe', and 'bond_etfs'
    
    Raises:
        ValueError: If the portfolio variant is not recognized
    """
    variants = {
        '1.0x_long': SIGNAL_1_0X_LONG,
        '1.5x_long': SIGNAL_1_5X_LONG,
    }
    
    if portfolio_variant not in variants:
        raise ValueError(
            f"Unknown portfolio variant: {portfolio_variant}. "
            f"Available options: {list(variants.keys())}"
        )
    
    return variants[portfolio_variant]
