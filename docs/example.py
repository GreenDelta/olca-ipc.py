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

    # First we create a connection to the IPC server. The `Client` class
    # provides all the methods we need to communicate with the IPC server.
    client = olca.Client(8080)

    # Search for the flow property `Mass` and unit `kg` in the database.
    # The `find` method does not return a full data set but just a reference
    # to the data set.
    mass_ref = client.find(olca.FlowProperty, 'Mass')
    assert type(mass_ref) == olca.Ref
    mass = client.get(olca.FlowProperty, mass_ref.id)
    assert type(mass) == olca.FlowProperty
    units_of_mass = client.get(olca.UnitGroup, mass.unit_group.id)
    kg = None
    for unit in units_of_mass.units:
        if unit.name == 'kg':
            kg = unit
            break
    assert kg is not None, 'Could not find unit kg'



if __name__ == '__main__':
    main()
