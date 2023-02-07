# olca-ipc

`olca-ipc` is a Python package for inter-process communication (IPC) with
openLCA. With this, it is possible to call functions of openLCA and processing
their results in Python. It implements the unified IPC protocol of openLCA for
JSON-RPC and REST APIs. The documentation of these protocols and examples can be
found in the __[openLCA IPC
documentation](https://greendelta.github.io/openLCA-ApiDoc/ipc/)__.

**Note** that this is an unstable alpha version that only works with the latest
development version of openLCA 2 that may is not published yet. The latest
stable version for openLCA 1.x is
[0.0.12](https://pypi.org/project/olca-ipc/0.0.12/):

```bash
# for openLCA 1.x
pip install olca-ipc==0.0.12
```

The source code and API documentation of the version for openLCA 1.x is in the
`v1` branch of olca-ipc repository. Alpha versions for openLCA 2 are available
on pypi.org, see the [releases
there](https://pypi.org/project/olca-ipc/#history).

```bash
# alpha versions for openLCA 2
pip install olca-ipc==2.0.0a[NUMBER]
```

If you just want to read and write data for openLCA 2, you can also directly
use the [olca-schema package](https://pypi.org/project/olca-schema/), which
is a dependency of `olca-ipc` now.
