# olca-ipc

__Note that this is an unstable alpha version that only works with the latest
development version of openLCA 2 that may is not published yet.__

`olca-ipc` is a Python package for inter-process communication (IPC) with
openLCA. With this, it is possible to call functions of openLCA and processing
their results in Python. It implements the unified IPC protocol of openLCA
for the JSON-RPC and REST based protocols. The documentation of these
protocols and examples can be found in the
__[openLCA IPC documentation](https://greendelta.github.io/openLCA-ApiDoc/ipc/)__.

`olca-ipc` uses the [openLCA schema](http://greendelta.github.io/olca-schema/)
(`olca-schema`) as data exchange format. If you just want to read or write
data sets in that format you can use the [olca-schema Python package](https://pypi.org/project/olca-schema/)
instead.

## Installation

The current stable version of `olca-ipc` is available on
[pypi.org](https://pypi.org/project/olca-ipc/) and can be installed (and
uninstalled) with pip:

```bash
pip install -U olca-ipc
```
