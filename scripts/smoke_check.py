"""Execute existing notebook cells with bounded sizes, without rewriting outputs.

This verifies execution paths, not the historical numerical results. For the
Air Quality notebook only data preparation and linear baselines are executed.
"""
from pathlib import Path
import ast
import contextlib
import io
import json
import os
import time
import warnings

os.environ.setdefault('MPLBACKEND', 'Agg')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def _numeric_literal(node):
    """True for size expressions such as 5000 or 10**4, not for computed arrays."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float)) and not isinstance(node.value, bool)
    if isinstance(node, ast.BinOp):
        return _numeric_literal(node.left) and _numeric_literal(node.right)
    if isinstance(node, ast.UnaryOp):
        return _numeric_literal(node.operand)
    return False


class BoundSizes(ast.NodeTransformer):
    """Bound assignments to existing size variables for a fast execution check."""
    names = {'n', 'N', 'm', 'n_samples', 'n_obs', 'n_iter'}

    def visit_Constant(self, node):
        if isinstance(node.value, int) and not isinstance(node.value, bool) and node.value >= 5000:
            return ast.copy_location(ast.Constant(min(node.value, 1000)), node)
        return node

    def visit_Assign(self, node):
        node = self.generic_visit(node)
        if any(isinstance(t, ast.Name) and t.id == 'burn' for t in node.targets):
            node.value = ast.Constant(100)  # burn-in must stay below the bounded chain length
        if any(isinstance(t, ast.Name) and t.id in self.names for t in node.targets) and _numeric_literal(node.value):
            node.value = ast.Call(func=ast.Name(id='min', ctx=ast.Load()), args=[node.value, ast.Constant(1000)], keywords=[])
        return node


def run_notebook(path):
    nb = json.loads(path.read_text(encoding='utf-8'))
    namespace = {'__name__': '__main__'}
    np.random.seed(42)
    count = 0
    start = time.perf_counter()
    caught = []
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] != 'code':
                continue
            if path.name.startswith('01_'):
                # Actual data preparation and baseline fitting at original size.
                if cell['metadata']['source_cell'] > 36:
                    continue
            source = ''.join(cell['source'])
            tree = ast.parse(source)
            if not path.name.startswith('01_'):
                tree = BoundSizes().visit(tree)
                ast.fix_missing_locations(tree)
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(tree, f'{path.name}:cell-{i}', 'exec'), namespace)
            plt.close('all')
            count += 1
        caught = sorted({str(w.message) for w in captured})
    # Semantic checks on variables already computed by the notebook.
    if path.name.startswith('01_'):
        assert namespace['X_train_s'].shape == (5552, 8)
        assert namespace['X_test_s'].shape == (1389, 8)
        for row in namespace['results']:
            assert np.isfinite(row['R²'])
    if path.name.startswith('06_'):
        result = namespace['run_em'](namespace['sample'], .5, 0, 1, .5, 2, 30)
        assert np.isfinite(result[-1]).all()
        assert (np.diff(result[-1]) >= -1e-7).all()
    return {'notebook': path.name, 'executed_cells': count, 'seconds': round(time.perf_counter()-start,2),
            'scope': 'original-size preprocessing and OLS/ridge only' if path.name.startswith('01_') else 'all selected cells; sample sizes bounded in memory',
            'warnings': caught, 'status': 'PASS'}


if __name__ == '__main__':
    os.chdir(ROOT)
    results = []
    for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
        result = run_notebook(path)
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    print('Existing-code smoke checks passed. Saved outputs were not changed.')
