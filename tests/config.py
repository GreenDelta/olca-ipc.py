import olca_ipc as ipc
import olca_ipc.protocol as protocol
import olca_ipc.rest as rest

# configure here the client against which
# the test suite should be executed
client: protocol.IpcProtocol
use_rest = False
if use_rest:
    client = rest.RestClient("http://localhost:8080")
else:
    client = ipc.Client(8080)
