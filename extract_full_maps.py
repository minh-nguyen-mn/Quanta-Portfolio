import json

def extract_full_signal_map(notebook_path):
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
                
                # Clean up: remove comments and blank lines, keep only active signals
                lines = []
                for line in signal_map_code.split('\n'):
                    stripped = line.strip()
                    # Keep lines that are active (not commented out) and either part of dict or signal definitions
                    if stripped and not stripped.startswith('#'):
                        lines.append(line)
                    elif stripped.startswith('# '):
                        # Keep inline comments explaining signal status
                        continue
                
                return '\n'.join(lines)
    
    return None

# Extract both
code_1 = extract_full_signal_map('Portfolio_1_0xLong.ipynb')
code_15 = extract_full_signal_map('Portfolio_1_5xLong.ipynb')

print("=" * 80)
print("PORTFOLIO_1_0XLONG.IPYNB - SIGNAL_MAP")
print("=" * 80)
print(code_1)

print("\n\n" + "=" * 80)
print("PORTFOLIO_1_5XLONG.IPYNB - SIGNAL_MAP")
print("=" * 80)
print(code_15)
