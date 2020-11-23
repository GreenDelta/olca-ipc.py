import os

import requests
import olca.schema as schema

from enum import Enum
from typing import Iterator, List, Optional, Type, TypeVar

T = TypeVar('T')


class ProductResult(schema.Entity):
    """
    The ProductResult type is not an olca-schema type but a return
    type of the IPC protocol. However, it implements the same interface
    as the olca.schema.Entity type.

    Attributes:
    -----------
    process: olca.schema.Ref

    product: olca.schema.Ref

    amount: float

    """

    def __init__(self):
        super(ProductResult, self).__init__()
        process: Optional[schema.Ref] = None
        product: Optional[schema.Ref] = None
        amount: Optional[float] = None

    def to_json(self) -> dict:
        json: dict = super(ProductResult, self).to_json()
        if self.process is not None:
            json['process'] = self.process.to_json()
        if self.product is not None:
            json['product'] = self.product.to_json()
        if self.amount is not None:
            json['amount'] = self.amount
        return json

    def read_json(self, json: dict):
        super(ProductResult, self).read_json(json)
        val = json.get('process')
        if val is not None:
            self.process = schema.Ref.from_json(val)
        val = json.get('product')
        if val is not None:
            self.product = schema.Ref.from_json(val)
        val = json.get('amount')
        if val is not None:
            self.amount = val

    @staticmethod
    def from_json(json: dict):
        instance = ProductResult()
        instance.read_json(json)
        return instance


class ContributionItem(schema.Entity):
    """
    The ContributionItem type is not an olca-schema type but a return
    type of the IPC protocol. However, it implements the same interface
    as the olca.schema.Entity type.

    Attributes:
    -----------
    item: olca.schema.Ref

    amount: float

    share: float

    rest: bool

    unit: str

    """

    def __init__(self):
        super(ContributionItem, self).__init__()
        item: Optional[schema.Ref] = None
        amount: Optional[float] = None
        share: Optional[float] = None
        rest: Optional[bool] = None
        unit: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(ContributionItem, self).to_json()
        if self.item is not None:
            json['item'] = self.item.to_json()
        if self.amount is not None:
            json['amount'] = self.amount
        if self.share is not None:
            json['share'] = self.share
        if self.rest is not None:
            json['rest'] = self.rest
        if self.unit is not None:
            json['unit'] = self.unit
        return json

    def read_json(self, json: dict):
        super(ContributionItem, self).read_json(json)
        val = json.get('item')
        if val is not None:
            self.item = schema.Ref.from_json(val)
        val = json.get('amount')
        if val is not None:
            self.amount = val
        val = json.get('share')
        if val is not None:
            self.share = val
        val = json.get('rest')
        if val is not None:
            self.rest = val
        val = json.get('unit')
        if val is not None:
            self.unit = val

    @staticmethod
    def from_json(json: dict):
        instance = ContributionItem()
        instance.read_json(json)
        return instance


class Client(object):
    """
    A client to communicate with an openLCA IPC server.

    An openLCA IPC server is always connected to a database and operations
    that are executed via this client are thus executed on that database.

    Parameters
    ----------

    port: int, optional
        The port of the server connection; optional, defaults to 8080.
    """

    def __init__(self, port: int = 8080):
        self.url = 'http://localhost:%i' % port
        self.next_id = 1

    def insert(self, model: schema.RootEntity):
        """
        Inserts the given model into the database of the IPC server.

        Example
        -------
        ```
        import olca

        flow = olca.Flow()
        flow.name = 'CO2'
        flow.id = str(uuid.uuid4())
        prop = olca.FlowPropertyFactor()
        prop.flow_property = olca.ref(
            olca.FlowProperty,
            '93a60a56-a3c8-11da-a746-0800200b9a66',
            'Mass'
        )
        prop.conversion_factor = 1.0
        prop.reference_flow_property = True
        flow.flow_properties = [prop]
        response = olca.Client().insert(flow)
        print(response)
        ```

        """
        if model is None:
            return
        json = model.to_json()
        return self.__post('insert/model', json)

    def update(self, model: schema.RootEntity):
        """
        Update the given model in the database of the IPC server.
        """
        if model is None:
            return
        json = model.to_json()
        return self.__post('update/model', json)

    def delete(self, model: schema.RootEntity):
        """
        Delete the given model from the database of the IPC server.
        """
        if model is None:
            return
        json = model.to_json()
        return self.__post('delete/model', json)

    def calculate(self, setup: schema.CalculationSetup) -> schema.SimpleResult:
        """
        Calculates a result for the given calculation setup.

        Parameters
        ----------

        setup: olca.schema.CalculationSetup
            The setup of the calculation.

        Example
        -------
        ```
        client = olca.Client()
        setup = olca.CalculationSetup()
        setup.calculation_type = olca.CalculationType.UPSTREAM_ANALYSIS
        setup.product_system = olca.ref(
            olca.ProductSystem,
            '91c2c4a5-2d9d-482e-8c8c-678d7e1b9f55'
        )
        setup.impact_method = olca.ref(
            olca.ImpactMethod,
            'd2c781ce-21b4-3218-8fca-78133f2c8d4d'
        )
        setup.amount = 1.0
        result = client.calculate(setup)
        # do something with the result
        # you should always dispose the result when you
        # do not need it anymore to avoid memory leaks.
        client.dispose(result)
        ```
        """
        if setup is None:
            raise ValueError('Invalid calculation setup')
        resp = self.__post('calculate', setup.to_json())
        return schema.SimpleResult.from_json(resp)

    def simulator(self, setup: schema.CalculationSetup) -> schema.Ref:
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
        setup.calculation_type = olca.CalculationType.MONTE_CARLO_SIMULATION
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
        if setup is None:
            raise ValueError('Invalid calculation setup')
        r = self.__post('simulator', setup.to_json())
        return schema.Ref.from_json(r)

    def next_simulation(self, simulator: schema.Ref) -> schema.SimpleResult:
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
            raise ValueError('No simulator given')
        resp = self.__post('next/simulation', simulator.to_json())
        return schema.SimpleResult.from_json(resp)

    def get_descriptors(self, model_type: Type[T]) -> Iterator[schema.Ref]:
        """
        Get the list of descriptors of the entities with the given model type.

        Parameters
        ----------
        model_type: T
            A class, e.g. olca.Flow

        Returns
        -------
        Iterator[schema.Ref]
            An iterator with Ref objects.
        """
        params = {'@type': model_type.__name__}
        result = self.__post('get/descriptors', params)
        for r in result:
            yield schema.Ref.from_json(r)

    def get_descriptor(self, model_type: Type[T], model_id: str) -> schema.Ref:
        """
        Get a descriptor of the model with the given ID.

        Models like product systems can be very large but often we just need
        a reference to a model (e.g. in a calculation setup). In this case
        this method can be useful.

        since: openLCA 2.0

        Parameters
        ----------
        model_type: T
            A model class, e.g. olca.ProductSystem
        model_id: str
            The ID of the model.

        Returns
        -------
        schema.Ref
            The descriptor of the model.

        Example
        -------
        ```
        import olca

        client = olca.Client()
        system_ref = client.get_descriptor(
            olca.ProductSystem,
            'f50ee15a-968f-4316-a160-4c7741284c62')
        print(system_ref.to_json())
        ```
        """
        params = {'@type': model_type.__name__, '@id': model_id}
        result = self.__post('get/descriptor', params)
        return schema.Ref.from_json(result)

    def get(self, model_type: Type[T], model_id: str) -> T:
        params = {'@type': model_type.__name__, '@id': model_id}
        result = self.__post('get/model', params)
        return model_type.from_json(result)

    def get_all(self, model_type: Type[T]) -> Iterator[T]:
        """
        Returns a generator for all instances of the given type from the
        database. Note that this will first fetch the complete JSON list from
        the IPC server and thus should be only used when a small amount of
        instances is expected as return value.

        Example
        -------
        ```python
        import olca

        client = olca.Client()
        currencies = client.get_all(olca.Currency)
        for c in currencies:
            print(c.name)
        ```
        """
        params = {'@type': model_type.__name__}
        result = self.__post('get/models', params)
        for r in result:
            yield model_type.from_json(r)

    def find(self, model_type, name: str) -> schema.Ref:
        """Searches for a data set with the given type and name.

        :param model_type: The class of the data set, e.g. `olca.Flow`.
        :param name: The name of the data set.
        :return: The reference to the first data set with the given name and
                 type from the databases or ``None`` if there is no such data
                 set in the database.
        """
        for d in self.get_descriptors(model_type):
            if d.name == name:
                return d

    def excel_export(self, result: schema.SimpleResult, path: str):
        """Export the given result to an Excel file with the given path.

        :param result: The result that should be exported.
        :param path: The path of the Excel file to which the result should be
                     written.
        """
        abs_path = os.path.abspath(path)
        params = {
            '@id': result.id,
            'path': abs_path
        }
        self.__post('export/excel', params)

    def dispose(self, entity: schema.Entity):
        """
        Removes the given entity from the memory of the IPC server.

        This is required for calculation results that are hold on the server for
        further processing.

        Parameters
        ----------

        entity: olca.schema.Entity
            The entity that should be disposed (typically a result).

        Example
        -------
        ```python
        client = olca.Client()
        setup = olca.CalculationSetup()
        setup.calculation_type = olca.CalculationType.UPSTREAM_ANALYSIS
        setup.product_system = olca.ref(
          olca.ProductSystem,
          '7d1cbce0-b5b3-47ba-95b5-014ab3c7f569'
        )
        setup.amount = 1.0
        result = client.calculate(setup)
        # do something with the result
        # ...
        response = client.dispose(result)
        print(response)  # should print `ok`
        ```
        """
        if entity is None:
            return
        arg = {'@type': type(entity).__name__, '@id': entity.id}
        return self.__post('dispose', arg)

    def shutdown_server(self):
        """
        Close the database and shutdown the server.

        This method is probably most useful when running a headless server
        (a server without openLCA user interface).
        """
        self.__post('runtime/shutdown', None)

    def create_product_system(self, process_id: str,
                              default_providers='prefer',
                              preferred_type='LCI_RESULT'):
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

        ```
        import olca

        client = olca.Client(8080)
        process_id = '4aee0b0c-eb46-37f1-8c7a-7e5b1adfd014'
        ref = client.create_product_system(process_id)
        print('Created product system %s' % ref.id)
        ```
        """

        r = self.__post('create/product_system', {
            'processId': process_id,
            'preferredType': preferred_type,
            'providerLinking': default_providers,
        })
        return schema.Ref.from_json(r)

    def lci_inputs(self, result: schema.SimpleResult) -> List[schema.FlowResult]:
        """
        Returns the inputs of the given inventory result.

        Example
        -------
        ```python
        result = client.calculate(setup)
        # print the first input
        print(client.lci_inputs(result)[0])
        client.dispose(result)
        ```
        """
        raw = self.__post('get/inventory/inputs', {
            'resultId': result.id,
        })
        return [schema.FlowResult.from_json(it) for it in raw]

    def lci_outputs(self, result: schema.SimpleResult) -> list:
        """
        Returns the outputs of the given inventory result.

        Example
        -------
        ```python
        result = client.calculate(setup)
        # print the first output
        print(client.lci_outputs(result)[0])
        client.dispose(result)
        ```
        """
        raw = self.__post('get/inventory/outputs', {
            'resultId': result.id,
        })
        return [schema.FlowResult.from_json(it) for it in raw]

    def lci_location_contributions(self, result: schema.SimpleResult,
                                   flow: schema.Ref) -> List[ContributionItem]:
        """
        Get the contributions of the result of the given flow by location.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The result which needs to be at least a contribution result.

        flow: olca.schema.Ref
            The (reference of the) flow for which the calculations should be
            calculated.

        Returns
        -------
        List[ContributionItem]
            The contributions to the flow result by location.

        Example
        -------
        ```python
        # ...
        result = client.calculate(setup)
        # select the first output of the LCI result
        output = client.lci_outputs(result)[0]
        # calculate the location contributions of the flow of that output
        cons = client.lci_location_contributions(result, output.flow)
        # ...
        client.dispose(result)
        ```
        """
        raw = self.__post('get/inventory/contributions/locations', {
            'resultId': result.id,
            'flow': flow.to_json(),
        })
        return [ContributionItem.from_json(it) for it in raw]

    def lci_total_requirements(self, result: schema.SimpleResult) -> List[ProductResult]:
        """
        Returns the total requirements of the given result.

        The total requirements are the product amounts that are required to
        fulfill the demand of the product system. As our technology matrix
        \\(A\\) is indexed symmetrically (means rows and columns refer to the
        same process-product pair) our product amounts are on the diagonal of
        the technology matrix and the total requirements can be calculated by
        the following equation where \\(s\\) is the scaling vector (
        \\(\\odot\\) denotes element-wise multiplication):

        $$t = diag(A) \odot s$$

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The simple result from which the total requirements should be
            returned.

        Example
        -------
        ```python
        import olca

        client = olca.Client()
        setup = olca.CalculationSetup()
        setup.calculation_type = olca.CalculationType.UPSTREAM_ANALYSIS
        setup.product_system = olca.ref(
            olca.ProductSystem,
            '7d1cbce0-b5b3-47ba-95b5-014ab3c7f569'
        )
        setup.amount = 1.0
        result = client.calculate(setup)
        print(client.lci_total_requirements(result)[0])
        client.dispose(result)
        ```
        """

        raw = self.__post('get/inventory/total_requirements', {
            'resultId': result.id
        })
        return [ProductResult.from_json(it) for it in raw]

    def lcia(self, result: schema.SimpleResult) -> List[schema.ImpactResult]:
        """
        Returns the LCIA result of the given result.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The result from which the LCIA result should be returned.

        Example
        -------
        ```python
        # ...
        result = client.calculate(setup)
        lcia = client.lcia(result)
        # ...
        client.dispose(result)
        ```
        """

        raw = self.__post('get/impacts', {
            'resultId': result.id,
        })
        return [schema.ImpactResult.from_json(it) for it in raw]

    def lcia_flow_contributions(self, result: schema.SimpleResult,
                                impact: schema.Ref) -> List[ContributionItem]:
        """
        Get the flow contributions to the result of the given impact category.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The result.

        impact: olca.schema.Ref
            The (reference to the) LCIA category.

        Example
        -------
        ```python
        # ...
        result = client.calculate(setup)
        # select the first LCIA result
        impact_result = client.lcia(result)[0]
        # get the flow contributions to the LCIA category of that result
        cons = client.lcia_flow_contributions(
            result, impact_result.impact_category)
        # ...
        client.dispose(result)
        ```
        """

        raw = self.__post('get/impacts/contributions/flows', {
            'resultId': result.id,
            'impactCategory': impact.to_json(),
        })
        return [ContributionItem.from_json(it) for it in raw]

    def lcia_location_contributions(self, result: schema.SimpleResult,
                                    impact: schema.Ref) -> List[ContributionItem]:
        """
        Get the contributions to the result of the given impact category by
        locations.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The result.

        impact: olca.schema.Ref
            The (reference to the) LCIA category.


        Example
        -------
        ```python
        # ...
        result = client.calculate(setup)
        # select the first LCIA result
        impact_result = client.lcia(result)[0]
        # get the flow contributions to the LCIA category of that result
        cons = client.lcia_location_contributions(
            result, impact_result.impact_category)
        # ...
        client.dispose(result)
        ```
        """

        raw = self.__post('get/impacts/contributions/locations', {
            'resultId': result.id,
            'impactCategory': impact.to_json(),
        })
        return [ContributionItem.from_json(it) for it in raw]

    def lcia_process_contributions(self, result: schema.SimpleResult,
                                   impact: schema.Ref) -> List[ContributionItem]:
        """
        Get the contributions to the result of the given impact category by
        processes.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The result.

        impact: olca.schema.Ref
            The (reference to the) LCIA category.


        Example
        -------
        ```python
        # ...
        result = client.calculate(setup)
        # select the first LCIA result
        impact_result = client.lcia(result)[0]
        # get the flow contributions to the LCIA category of that result
        cons = client.lcia_process_contributions(
            result, impact_result.impact_category)
        # ...
        client.dispose(result)
        ```
        """

        raw = self.__post('get/impacts/contributions/processes', {
            'resultId': result.id,
            'impactCategory': impact.to_json(),
        })
        return [ContributionItem.from_json(it) for it in raw]

    def __post(self, method: str, params):
        req = {
            'jsonrpc': '2.0',
            'id': self.next_id,
            'method': method,
            'params': params
        }
        self.next_id += 1
        resp = requests.post(self.url, json=req).json()  # type: dict
        err = resp.get('error')  # type: dict
        if err is not None:
            msg = '%i: %s' % (err.get('code'), err.get('message'))
            raise Exception(msg)
        result = resp.get('result')
        if result is None:
            raise Exception(
                'No error and no result: invalid JSON-RPC response')
        return result
