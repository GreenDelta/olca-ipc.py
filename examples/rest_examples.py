# %%
import olca_schema as lca
from olca_ipc import rest

client = rest.RestClient("http://localhost:8080")

actor = client.get(lca.Actor, "002ed891-c4e6-35ae-99b3-560e65e62cb2")
assert actor
actor.to_json()
# %%
