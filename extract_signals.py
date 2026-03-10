import json

def extract_signal_map(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'SIGNAL_MAP = {' in source:
                # Find the dictionary definition
                start = source.find('SIGNAL_MAP = {')
                # Find the matching closing brace
                brace_count = 0
                in_dict = False
                end = start
                for i in range(start, len(source)):
                    if source[i] == '{':
                        brace_count += 1
                        in_dict = True
                    elif source[i] == '}':
                        brace_count -= 1
                        if in_dict and brace_count == 0:
                            end = i + 1
                            break
                
                signal_map_code = source[start:end]
                
                # Extract just the active signals
                lines = signal_map_code.split('\n')
                active_signals = []
                signal_etf_dict = {}
                
                for line in lines:
                    line_stripped = line.strip()
                    if line_stripped and not line_stripped.startswith('#') and ':' in line_stripped:
                        # Extract signal name and ETF list
                        parts = line_stripped.split(':', 1)
                        signal_name = parts[0].strip()
                        active_signals.append(signal_name)
                        
                        # Extract ETF list
                        if len(parts) > 1:
                            etf_str = parts[1].strip()
                            if etf_str.startswith('[') and etf_str.endswith('],'):
                                etf_list = etf_str[1:-2]  # Remove [ and ],
                                etfs = [e.strip().strip("'\"") for e in etf_list.split(',')]
                                signal_etf_dict[signal_name] = [e for e in etfs if e]
                
                return signal_map_code, active_signals, signal_etf_dict
    
    return None, None, {}

# Process both notebooks
print("=" * 80)
print("PORTFOLIO_1_0XLONG.IPYNB")
print("=" * 80)
code_1, signals_1, etf_dict_1 = extract_signal_map('Portfolio_1_0xLong.ipynb')
print(f"\nActive Signals ({len(signals_1)}):")
for sig in signals_1:
    print(f"  - {sig}")

print("\n" + "=" * 80)
print("PORTFOLIO_1_5XLONG.IPYNB")
print("=" * 80)
code_15, signals_15, etf_dict_15 = extract_signal_map('Portfolio_1_5xLong.ipynb')
print(f"\nActive Signals ({len(signals_15)}):")
for sig in signals_15:
    print(f"  - {sig}")

print("\n" + "=" * 80)
print("ETF COUNT ANALYSIS")
print("=" * 80)

# Count unique ETFs in each portfolio
all_etfs_1 = set()
for etf_list in etf_dict_1.values():
    all_etfs_1.update(etf_list)

all_etfs_15 = set()
for etf_list in etf_dict_15.values():
    all_etfs_15.update(etf_list)

print(f"\nPortfolio 1.0x: {len(all_etfs_1)} unique ETFs")
print(f"Portfolio 1.5x: {len(all_etfs_15)} unique ETFs")

# Find differences
only_in_1 = set(signals_1) - set(signals_15)
only_in_15 = set(signals_15) - set(signals_1)
in_both = set(signals_1) & set(signals_15)

print(f"\n" + "=" * 80)
print("SIGNAL DIFFERENCES")
print("=" * 80)
print(f"\nSignals only in 1.0x ({len(only_in_1)}): {sorted(only_in_1)}")
print(f"Signals only in 1.5x ({len(only_in_15)}): {sorted(only_in_15)}")
print(f"Signals in both ({len(in_both)}): {sorted(in_both)}")
