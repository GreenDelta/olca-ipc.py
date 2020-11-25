# This is an example that shows how to create an openLCA product system from
# scratch and calculate it via the openLCA IPC interface. It assumes that an
# openLCA IPC server is started at port 8080 and that it is connected to a
# databases which contains the openLCA reference data. You can start such an
# IPC server via the openLCA user interface under `Window > Developer tools >
# IPC server`. If the server is running, you should be able to run this example
# script simply via `python example.py`.

# We use the uuid package from the standard library to generate unique IDs for
# our new data sets.
import uuid

# The `olca` package is the only third party package we need to import. It has
# no other dependencies than the Python standard library. It provides a class
# based implementation of the openLCA data exchange model and an API for
# communicating with an openLCA IPC server (https://github.com/GreenDelta/olca-schema)
import olca


def main():
    # This is the entry point of our script

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

    # we use the helper function create flow to create some flow data sets
    # and save them into openLCA.
    steel = create_flow(client, 'steel', mass)
    co2 = create_flow(client, 'CO2', mass, olca.FlowType.ELEMENTARY_FLOW)

    # Now, we delete everything we created in reverse order
    client.delete(co2)
    client.delete(steel)


def create_flow(client: olca.Client, name: str,
                flow_property: olca.FlowProperty,
                flow_type=olca.FlowType.PRODUCT_FLOW) -> olca.Flow:
    """ Create a new flow with the given name and insert it into the database.
    """
    flow = olca.Flow()
    flow.olca_type = 'Flow'
    flow.id = str(uuid.uuid4())
    flow.name = name
    flow.flow_type = flow_type

    # A flow has one ore more quantities in which amounts of the flow can be
    # specified. In openLCA (and the ILCD format) these quantities are named
    # `flow properties` and they have flow specific conversion factors. Each
    # flow has at least one reference flow property and thus one flow property
    # factor:
    factor = olca.FlowPropertyFactor()
    factor.flow_property = flow_property
    factor.conversion_factor = 1.0
    factor.reference_flow_property = True
    flow.flow_properties = [factor]
    client.insert(flow)
    return flow


if __name__ == '__main__':
    main()
