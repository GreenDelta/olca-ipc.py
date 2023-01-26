import logging as log
import os

import requests
import olca_schema as schema
import olca_schema.results as results

from .ipc_types import *
from .result import Result

from typing import Any, Optional, Tuple, Type, TypeVar, Union

E = TypeVar("E", bound=schema.RootEntity)
ModelType = Union[Type[E], str]


def _model_type(param: ModelType) -> str:
    """Get the @type tag for a JSON request."""
    if isinstance(param, str):
        return param
    else:
        return param.__name__


def _model_class(param: ModelType) -> Type:
    if isinstance(param, str):
        return schema.__dict__[param]
    else:
        return param


class Client(object):
    """
    A client to communicate with an openLCA IPC server over the JSON-RPC
    protocol.

    Parameters
    ----------

    port: int, optional
        The port of the server connection; optional, defaults to 8080.
    """

    def __init__(self, port: int = 8080):
        self.url = "http://localhost:%i" % port
        self.next_id = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def close(self):
        return

    def put(self, model: schema.RootEntity) -> schema.Ref | None:
        if model is None:
            return None
        json = model.to_dict()
        resp, err = self.rpc_call("data/put", json)
        if err:
            log.error("failed to insert model: %s", err)
            return None
        return schema.Ref.from_dict(resp)

    def put_all(self, *models: schema.RootEntity):
        for model in models:
            self.put(model)

    def delete(
        self, model: schema.RootEntity | schema.Ref
    ) -> schema.Ref | None:
        if model is None:
            return
        json = model.to_dict()
        resp, err = self.rpc_call("data/delete", json)
        if err:
            log.error("failed to delete model: %s", err)
            return None
        return schema.Ref.from_dict(resp)

    def calculate(self, setup: results.CalculationSetup) -> Result:
        """Calculates a result for the given calculation setup."""
        resp, err = self.rpc_call("result/calculate", setup.to_dict())
        if err:
            return Result(
                uid="", client=self, error=results.ResultState(id="", error=err)
            )
        state = results.ResultState.from_dict(resp)
        return Result(uid=state.id, client=self, error=None)

    def simulator(self, setup: results.CalculationSetup) -> schema.Ref:
        """
        Create a simulator to run Monte-Carlo simulations for the given setup.

        Parameters
        ----------

        setup: olca.schema.CalculationSetup
            The calculation setup that should be used.

        Returns
        -------

        olca.schema.Ref
            A reference to an simulator instance.

        Example
        -------
        ```python
        import olca

        client = olca.Client()
        # creating the calculation setup
        setup = olca.CalculationSetup()
        setup.impact_method = client.find(olca.ImpactMethod, 'TRACI [v2.1, February 2014]')
        setup.product_system = client.find(olca.ProductSystem, 'compost plant, open')
        setup.amount = 1.0

        # create the simulator
        simulator = client.simulator(setup)

        for i in range(0, 10):
            result = client.next_simulation(simulator)
            first_impact = result.impact_results[0]
            print('iteration %i: result for %s = %4.4f' %
                  (i, first_impact.impact_category.name, first_impact.value))
            # we do not have to dispose the result here (it is not cached
            # in openLCA); but we need to dispose the simulator later (see below)

        # export the complete result of all simulations
        client.excel_export(simulator, 'simulation_result.xlsx')

        # the result remains accessible (for exports etc.) until
        # you dispose it, which you should always do when you do
        # not need it anymore
        client.dispose(simulator)
        ```
        """
        resp, err = self.rpc_call("simulator", setup.to_dict())
        if err:
            log.error("failed to create simulator: %s", err)
            return schema.Ref()
        return schema.Ref.from_dict(resp)

    def next_simulation(self, simulator: schema.Ref) -> schema.Result:
        """
        Runs the next Monte-Carlo simulation with the given simulator reference.
        It returns the result of the simulation. Note that this result is not
        cached (the simulator is cached).
        See [the simulator example](#olca.ipc.Client.simulator).

        Parameters
        ----------
        simulator: olca.schema.Ref
            The reference to the simulator which is called to run the next
            simulation step.

        """
        if simulator is None:
            raise ValueError("No simulator given")
        resp, err = self.rpc_call("next/simulation", simulator.to_dict())
        if err:
            log.error("failed to get simulation result: %s", err)
            return schema.Result()
        return schema.Result.from_dict(resp)

    def get_descriptors(self, model_type: ModelType) -> list[schema.Ref]:
        params = {"@type": _model_type(model_type)}
        result, err = self.rpc_call("data/get/descriptors", params)
        if err:
            log.error(
                "failed to get descriptors of type %s: %s", model_type, err
            )
            return []
        return [schema.Ref.from_dict(r) for r in result]

    def get_descriptor(
        self, model_type: ModelType, uid="", name=""
    ) -> Optional[schema.Ref]:
        params = {"@type": _model_type(model_type)}
        if uid != "":
            params["@id"] = uid
        if name != "":
            params["name"] = name
        result, err = self.rpc_call("data/get/descriptor", params)
        if err:
            log.error("failed to get descriptor: %s", err)
            return None
        return schema.Ref.from_dict(result)

    def get(self, model_type: Type[E], uid="", name="") -> Optional[E]:
        params = {"@type": _model_type(model_type)}
        if uid != "":
            params["@id"] = uid
        if name != "":
            params["name"] = name
        result, err = self.rpc_call("data/get", params)
        if err:
            log.warning("failed to get entity of type %s: %s", model_type, err)
            return None
        return _model_class(model_type).from_dict(result)

    def get_all(self, model_type: Type[E]) -> list[E]:
        params = {"@type": model_type.__name__}
        result, err = self.rpc_call("data/get/all", params)
        if err:
            log.error("failed to get all of type %s: %s", model_type, err)
        clazz = _model_class(model_type)
        return [clazz.from_dict(r) for r in result]

    def find(self, model_type: ModelType, name: str) -> schema.Ref | None:
        for d in self.get_descriptors(model_type):
            if d.name == name:
                return d

    def get_providers(
        self, flow: schema.Ref | schema.Flow | None = None
    ) -> list[results.TechFlow]:
        if flow is None:
            params = {}
        else:
            params = {
                "@type": "Flow",
                "@id": flow.id,
                "name": flow.name,
            }
        providers, err = self.rpc_call("data/get/providers", params)
        if err:
            log.error("failed to get providers: %s", err)
            return []
        return [results.TechFlow.from_dict(d) for d in providers]

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[schema.Parameter | schema.ParameterRedef]:
        params = {"@type": model_type.__name__, "@id": uid}
        params, err = self.rpc_call("data/get/parameters", params)
        if err:
            log.error("failed to get parameters of %s id=%d", model_type, uid)
            return []
        if model_type in (schema.Process, schema.ImpactCategory):
            return [schema.Parameter.from_dict(p) for p in params]
        else:
            return [schema.ParameterRedef.from_dict(p) for p in params]

    def excel_export(self, result: schema.Result, path: str):
        """Export the given result to an Excel file with the given path.

        :param result: The result that should be exported.
        :param path: The path of the Excel file to which the result should be
                     written.
        """
        abs_path = os.path.abspath(path)
        params = {"@id": result.id, "path": abs_path}
        _, err = self.rpc_call("export/excel", params)
        if err:
            log.error("Excel export to %s failed: %s", path, err)

    def shutdown_server(self):
        """
        Close the database and shutdown the server.

        This method is probably most useful when running a headless server
        (a server without openLCA user interface).
        """
        _, err = self.rpc_call("runtime/shutdown", None)
        if err:
            log.error("failed to shutdown server: %s", err)

    def create_product_system(
        self,
        process_id: str,
        default_providers="prefer",
        preferred_type="LCI_RESULT",
    ) -> Optional[schema.Ref]:
        """
        Creates a product system from the process with the given ID.

        Parameters
        ----------

        process_id: str
            The ID of the process from which the product system should be
            generated. This will be the reference process of the product system
            with upstream and downstream processes added recursively.

        default_providers: {'prefer', 'ignore', 'only'}, optional
            Indicates how default providers of product inputs and waste outputs
            should be considered during the linking. `only` means that only
            product inputs and waste outputs should be linked that have a
            default provider and that this default provider is used. `prefer`
            means that a default provider is used during the linking if there
            are multiple options. `ignore` means that the default providers
            have no specific role.

        preferred_type : {'LCI_RESULT', 'UNIT_PROCESS'}, optional
            When there are multiple provider processes available for linking a
            product input or waste output the `preferred_type` indicates which
            type of process (LCI results or unit processes) should be preferred
            during the linking.

        Returns
        -------

        olca.schema.Ref
            A descriptor of the created product system.

        Example
        -------

        ```python
        import olca

        client = olca.Client(8080)
        process_id = '4aee0b0c-eb46-37f1-8c7a-7e5b1adfd014'
        ref = client.create_product_system(process_id)
        print('Created product system %s' % ref.id)
        ```
        """

        r, err = self.rpc_call(
            "create/product_system",
            {
                "processId": process_id,
                "preferredType": preferred_type,
                "providerLinking": default_providers,
            },
        )
        if err:
            log.error("failed to create product system: %s", err)
            return None
        return schema.Ref.from_dict(r)

    def upstream_tree_of(
        self,
        result: schema.Result,
        ref: schema.Ref,
        max_depth=5,
        min_contribution=0.1,
        max_recursion_depth=3,
    ) -> Optional[UpstreamTree]:
        """
        Get an upstream tree for an impact category or flow.

        This function is only available in openLCA 2.x.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The previously calculated result. This needs to be an upstream
            result.

        ref: olca.schema.Ref
            The result reference of the upstream tree: a flow or impact
            category reference.

        max_depth: int
            The maximum number of levels of the tree. A value < 0 means
            unlimited. In this case reasonable recursion limits are
            required if the underlying product system has cycles.

        min_contribution: float
            In addition to the maximum tree depth, this parameter describes
            the minimum upstream contribution of a node in the tree. A value
            < 0 means that there is no minimum contribution.

        max_recursion_depth: int
            When the max. tree depth is unlimited and the underlying product
            system has cycles, this parameter indicates how often a process
            can occur in a tree path. It defines the maximum number of
            expansions of a loop in a tree path.

        Example
        -------
        ```python
        client = olca.Client()

        # create the calculation setup and run the calculation
        setup = olca.CalculationSetup()
        setup.calculation_type = olca.CalculationType.UPSTREAM_ANALYSIS
        setup.product_system = olca.ref(
            olca.ProductSystem,
            '7d1cbce0-b5b3-47ba-95b5-014ab3c7f569'
        )
        setup.impact_method = olca.ref(
            olca.ImpactMethod,
            '99b9d86b-ec6f-4610-ba9f-68ebfe5691dd'
        )
        setup.amount = 1.0
        result = client.calculate(setup)

        # calculate the upstream tree and traverse it
        impact = olca.ref(
            olca.ImpactCategory,
            '2a26b243-23cb-4f90-baab-239d3d7397fa')
        tree = client.upstream_tree_of(result, impact)

        def traversal_handler(n: Tuple[UpstreamNode, int]):
            (node, depth) = n
            print('%s+ %s %.3f' % (
                '  ' * depth,
                node.product.process.name,
                node.result
            ))

        tree.traverse(traversal_handler)

        # dispose the result
        client.dispose(result)
        ```
        """
        raw, err = self.rpc_call(
            "get/upstream/tree",
            {
                "resultId": result.id,
                "ref": ref.to_dict(),
                "maxDepth": max_depth,
                "minContribution": min_contribution,
                "maxRecursionDepth": max_recursion_depth,
            },
        )
        if err:
            log.error("Failed to get upstream tree: %s", err)
            return None
        return UpstreamTree.from_dict(raw)

    def rpc_call(self, method: str, params) -> Tuple[Any, Optional[str]]:
        """
        Performs a JSON-RPC request with the given parameters.

        It returns a tuple (result, error).
        """
        req = {
            "jsonrpc": "2.0",
            "id": self.next_id,
            "method": method,
            "params": params,
        }
        self.next_id += 1
        resp: dict = requests.post(self.url, json=req).json()
        err: dict | None = resp.get("error")
        if err is not None:
            err_msg = "%i: %s" % (err.get("code"), err.get("message"))
            return None, err_msg
        result = resp.get("result")
        if result is None:
            return None, "No error and no result: invalid JSON-RPC response"
        return result, None
