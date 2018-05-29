# This is an example that shows how to create an openLCA product system from
# scratch and calculate it via the openLCA IPC interface. It assumes that an
# openLCA IPC server is started at port 8080 and that it is connected to a
# databases which contains the openLCA reference data. You can start such an
# IPC server via the openLCA user interface under `Window > Developer tools >
# IPC server`. If the server is running, you should be able to run this example
# script simply via `python example.py`.

# The `olca` package is the only thing we need to import. It provides a class
# based implementation of the openLCA data exchange model and an API for
# communicating with an openLCA IPC server (https://github.com/GreenDelta/olca-schema)
import olca


def main():
    # this is the entry point of our script
    assert 1 == 1


if __name__ == '__main__':
    main()
