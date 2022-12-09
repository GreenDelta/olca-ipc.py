# %%
import olca_schema as lca
from olca_ipc import rest

# create a rest client for an endpoint
client = rest.RestClient("http://localhost:8080")


# %%
# get a reference of the first product system in the database
system_ref = client.get_descriptors(lca.ProductSystem)[0]
assert system_ref and system_ref.id
print(system_ref.name)


# %%
# get the parameter redefinitions of that system
parameters = client.get_parameters(lca.ProductSystem, system_ref.id)
for p in parameters:
    print(f"{p.name} \t| {p.value}")

# %%
# get all providers from the database
providers = client.get_providers()
print(f"there are {len(providers)} tech. flow providers in the database")

# %%
# get providers of a single flow
flow = providers[42].flow
assert flow and flow.id
flow_providers = client.get_providers(flow_id=flow.id)
print(f"there are {len(flow_providers)} providers for flow: {flow.name}")

# %%
