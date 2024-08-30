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

Note that this version only works with the openLCA >= 2.x and requires
**Python >= 3.11**. The last stable version for openLCA 1.x is
[0.0.12](https://pypi.org/project/olca-ipc/0.0.12/):

```bash
# for openLCA 1.x
pip install olca-ipc==0.0.12
```

The source code and API documentation of the version for openLCA 1.x is in the
`v1` branch of this repository. If you just want to read and write data for
openLCA 2, you can also just use the
[olca-schema package](https://pypi.org/project/olca-schema/), which is a
dependency of `olca-ipc`.
