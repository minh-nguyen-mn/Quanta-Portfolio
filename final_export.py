import json

def extract_signal_map_clean(notebook_path, notebook_name):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'SIGNAL_MAP = {' in source:
                # Find and extract the dictionary
                start = source.find('SIGNAL_MAP = {')
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
                
                # Clean up the formatting: remove extra spaces and comments
                lines = []
                for line in signal_map_code.split('\n'):
                    stripped = line.strip()
                    # Keep non-empty, non-comment lines
                    if stripped and not stripped.startswith('#'):
                        lines.append(stripped)
                
                # Reconstruct with proper formatting
                clean_code = 'SIGNAL_MAP = {\n'
                for i, line in enumerate(lines[1:]):  # Skip first "SIGNAL_MAP = {"
                    if line == '}':
                        clean_code += '}\n'
                    else:
                        clean_code += '    ' + line + '\n'
                
                return clean_code
    
    return None

# Extract both
print("=" * 100)
print(f"Portfolio_1_0xLong.ipynb - SIGNAL_MAP (19 signals, 230 unique ETFs)")
print("=" * 100)
code_1 = extract_signal_map_clean('Portfolio_1_0xLong.ipynb', 'Portfolio_1_0xLong.ipynb')
print(code_1)

print("\n" + "=" * 100)
print(f"Portfolio_1_5xLong.ipynb - SIGNAL_MAP (11 signals, 142 unique ETFs)")
print("=" * 100)
code_15 = extract_signal_map_clean('Portfolio_1_5xLong.ipynb', 'Portfolio_1_5xLong.ipynb')
print(code_15)
