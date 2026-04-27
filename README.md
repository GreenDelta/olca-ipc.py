# olca-ipc

`olca-ipc` is a Python package for inter-process communication (IPC) with
openLCA. With this, it is possible to call functions of openLCA and processing
their results in Python. It implements the unified IPC protocol of openLCA for
JSON-RPC and REST APIs. The documentation of these protocols and examples can be
found here:

__[https://greendelta.github.io/openLCA-ApiDoc](https://greendelta.github.io/openLCA-ApiDoc)__.

This package is available on [pypi.org](https://pypi.org/project/olca-ipc) and
can be installed / updated like this:

```bash
pip install -U olca-ipc
```

If you just want to read and write data for openLCA 2, you can also use the
[olca-schema package](https://pypi.org/project/olca-schema/) directly, which is
a dependency of `olca-ipc`.


## Tests and packaging

If you want to run the test suite, make sure you have a server running and
configured in [tests/config.py](./tests/config.py). Then you can run the tests
with `pytest`, e.g. with `uv`:

```bash
cd olca-ipc.py
# create a virtual environment
uv venv [-p 3.12]
# install the test dependencies
uv sync --extra test
# run all tests
uv run pytest tests
```

Build and validate a release package with:

```bash
# install the packaging dependencies
uv sync --extra packaging
# build the source and wheel distributions
uv run python -m build
# validate the generated artifacts
uv run twine check dist/*
```
