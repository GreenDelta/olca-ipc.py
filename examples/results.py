import olca_ipc as ipc
import olca_schema as lca
import olca_schema.results as res
import pandas as pd

# First, we need to create a calculation setup. The calculation target can
# be a product system or process. This is just a minimal setup for a product
# system. The result is calculated for the quantitative reference defined
# in that system but this can be overwritten in the calculation setup, see
# http://greendelta.github.io/olca-schema/classes/CalculationSetup.html
setup = res.CalculationSetup(
    target=lca.Ref(
        model_type="ProductSystem", id="7c328e9b-d8e3-402b-a1ac-95620d021b99"
    ),
    impact_method=lca.Ref(
        model_type="ImpactMethod", id="787c02f1-d1f2-36d6-8e06-2307cc3ebebc"
    ),
)

# create a client connection and run the calculation
client = ipc.Client(8080)
result = client.calculate(setup)


state = result.get_state()
print(state)
# ResultState(
#   id='ca2ba8f8-c16d-4982-b1af-b56ef89a98f2',
#   error=None, is_ready=False, is_scheduled=True, time=1669731184674)

# actively waiting for a result
import time

while not result.get_state().is_ready:
    time.sleep(1)

# or better do this:
state = result.wait_until_ready()
# then check for errors
if state.error:
    pass


tech_flows = result.get_tech_flows()
print(
    pd.DataFrame(
      [(tf.provider.name, tf.flow.name) for tf in tech_flows],
      columns=["Provider", "Flow"]
      ).head()
)

envi_flows = result.get_envi_flows()
print(pd.DataFrame(envi_flows).info())

impact_categories = result.get_impact_categories()
print(pd.DataFrame(impact_categories))

# it is important to dispose a result when it is not needed anymore
result.dispose()
