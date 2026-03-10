import json

def count_etfs(notebook_path):
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
                
                # Extract all ETFs
                all_etfs = set()
                lines = signal_map_code.split('\n')
                
                for line in lines:
                    line_stripped = line.strip()
                    if ':' in line_stripped and not line_stripped.startswith('#'):
                        # Extract ETF list
                        if '[' in line_stripped and ']' in line_stripped:
                            # Find the list part
                            start_bracket = line_stripped.find('[')
                            end_bracket = line_stripped.rfind(']')
                            if start_bracket != -1 and end_bracket != -1:
                                etf_str = line_stripped[start_bracket+1:end_bracket]
                                # Split by comma and clean up
                                etfs = [e.strip().strip("'\"") for e in etf_str.split(',')]
                                for etf in etfs:
                                    if etf:
                                        all_etfs.add(etf)
                
                return len(all_etfs), sorted(all_etfs)
    
    return 0, []

count_1, etfs_1 = count_etfs('Portfolio_1_0xLong.ipynb')
count_15, etfs_15 = count_etfs('Portfolio_1_5xLong.ipynb')

print(f"Portfolio 1.0x: {count_1} unique ETFs")
print(f"Portfolio 1.5x: {count_15} unique ETFs")

print(f"\nPortfolio 1.5x ETFs ({count_15}):")
print(etfs_15)
