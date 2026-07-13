import sys
from pathlib import Path

# Make the package importable as `fastapi_gen8` (not `src.fastapi_gen8`) without
# requiring an editable install. This keeps the tests runnable from a bare
# checkout (e.g. CI, which does not `pip install` the package) and lets mypy see
# each source file under a single module name.
SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
