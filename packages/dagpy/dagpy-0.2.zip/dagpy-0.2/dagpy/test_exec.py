import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

with open('playground/B.ipynb') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

try:
    out = ep.preprocess(nb, {'metadata': {'path': 'playground/'}})
except CellExecutionError:
    out = None
    msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
    msg += 'See notebook "%s" for the traceback.' % notebook_filename_out
    print(msg)
    raise
finally:
    with open('playground/_B.ipynb', mode='wt') as f:
        nbformat.write(nb, f)