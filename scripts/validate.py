"""Check the portfolio's structure, Python syntax and local document links."""
from pathlib import Path
import ast
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []
code_cells = 0
for path in sorted((ROOT / 'notebooks').glob('*.ipynb')):
    nb = json.loads(path.read_text(encoding='utf-8'))
    assert nb['nbformat'] == 4
    ids = [c.get('id') for c in nb['cells']]
    if len(ids) != len(set(ids)):
        errors.append(f'{path.name}: duplicate cell IDs')
    for i, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'code':
            code_cells += 1
            try:
                ast.parse(source)
            except SyntaxError as e:
                errors.append(f'{path.name}:{i}: {e}')
            if any(o.get('output_type') == 'error' for o in cell.get('outputs', [])):
                errors.append(f'{path.name}:{i}: stored error output')
        elif cell['cell_type'] == 'markdown':
            for link in re.findall(r'\]\(([^)]+)\)', source):
                if not re.match(r'^(https?://|#|mailto:)', link):
                    target = path.parent / unquote(link.split('#')[0])
                    if not target.exists():
                        errors.append(f'{path.name}: missing {link}')
for path in ROOT.rglob('*.py'):
    try:
        ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError as e:
        errors.append(f'{path.relative_to(ROOT)}: {e}')
for path in ROOT.rglob('*.md'):
    text = path.read_text(encoding='utf-8')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if not re.match(r'^(https?://|#|mailto:)', link):
            target = path.parent / unquote(link.split('#')[0])
            if not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing {link}')
for path in list(ROOT.rglob('*.md')) + list(ROOT.rglob('*.ipynb')):
    text = path.read_text(encoding='utf-8')
    if re.search(r'[Cc]:[\\/]+Users[\\/]', text):
        errors.append(f'{path.relative_to(ROOT)}: local user path')
print(f'Parsed {code_cells} notebook code cells and all Python files.')
print(f'Checked {len(list(ROOT.rglob("*.md")))} Markdown documents and notebook links.')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('Structure, syntax, local links and publication hygiene: PASS')
