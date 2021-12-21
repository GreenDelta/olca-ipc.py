import logging as log
import os

import requests
import olca.schema as schema
import olca.upstream_tree as utree

from dataclasses import dataclass

from typing import Any, Iterator, List, Optional, Tuple, Type, TypeVar, Union

E = TypeVar('E', bound=schema.RootEntity)
ModelType = Union[Type[E], str]


def _model_type(param: ModelType) -> str:
    """Get the @type tag for a JSON request."""
    if isinstance(param, str):
        return param
    else:
        return param.__name__


def _model_class(param: ModelType) -> Type[schema.RootEntity]:
    if isinstance(param, str):
        return schema.__dict__[param]
    else:
        return param


@dataclass
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


@dataclass
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def close(self):
        return

    def insert(self, model: E):
        """
        Inserts the given model into the database of the IPC server.

        Example
        -------
        ```python
        import olca
        import uuid

        flow = olca.Flow()
        flow.name = 'CO2'
        flow.id = str(uuid.uuid4())
        flow.flow_type = olca.FlowType.ELEMENTARY_FLOW
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
        resp, err = self.__post('insert/model', json)
        if err:
            log.error('failed to insert model: %s', err)
            return err
        return resp

    def update(self, model: E):
        """
        Update the given model in the database of the IPC server.
        """
        if model is None:
            return
        json = model.to_json()
        resp, err = self.__post('update/model', json)
        if err:
            log.error('failed to update model: %s', err)
            return err
        return resp

    def delete(self, model: E):
        """
        Delete the given model from the database of the IPC server.
        """
        if model is None:
            return
        json = model.to_json()
        resp, err = self.__post('delete/model', json)
        if err:
            log.error('failed to delete model: %s', err)
            return err
        return resp

    def calculate(self, setup: schema.CalculationSetup) -> schema.SimpleResult:
        """
        Calculates a result for the given calculation setup.

        Parameters
        ----------

        setup: olca.schema.CalculationSetup
            The setup of the calculation.

        Example
        -------
        ```python
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
        resp, err = self.__post('calculate', setup.to_json())
        if err:
            log.error('calculation failed: %s', err)
            return schema.SimpleResult()
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
        resp, err = self.__post('simulator', setup.to_json())
        if err:
            log.error('failed to create simulator: %s', err)
            return schema.Ref()
        return schema.Ref.from_json(resp)

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
        resp, err = self.__post('next/simulation', simulator.to_json())
        if err:
            log.error('failed to get simulation result: %s', err)
            return schema.SimpleResult()
        return schema.SimpleResult.from_json(resp)

    def get_descriptors(self, model_type: ModelType) -> Iterator[schema.Ref]:
        """
        Get the descriptors of the entities with the type from the database.

        Parameters
        ----------
        model_type: ModelType
            The model type, e.g. olca.Flow or `'Flow'`

        Returns
        -------
        Iterator[schema.Ref]
            An iterator with Ref objects.

        Example:
        --------
        ```python
        import olca

        with olca.Client() as client:
            for a in client.get_descriptors('Actor'):
                print('found Actor: %s' % a.name)
            for s in client.get_descriptors(olca.Source):
                print('found Source: %s' % s.name)
        ```

        """
        params = {'@type': _model_type(model_type)}
        result, err = self.__post('get/descriptors', params)
        if err:
            log.error('failed to get descriptors of type %s: %s',
                      model_type, err)
            return []
        for r in result:
            yield schema.Ref.from_json(r)

    def get_descriptor(self, model_type: ModelType,
                       uid='', name='') -> Optional[schema.Ref]:
        """
        Get a descriptor of the model with the given ID or name from the database.

        Models like product systems can be very large but often we just need
        a reference to a model (e.g. in a calculation setup). In this case
        this method can be useful.

        since: openLCA 2.0

        Parameters
        ----------
        model_type: ModelType
            The type of the model, e.g. olca.ProductSystem or `'ProductSystem'`
        uid: str, optional
            The ID of the model.
        name: str, optional
            The name of the model.

        Returns
        -------
        schema.Ref
            The descriptor of the model.

        Example
        -------
        ```python
        import olca

        client = olca.Client()
        system_ref = client.get_descriptor(
            olca.ProductSystem,
            'f50ee15a-968f-4316-a160-4c7741284c62')
        print(system_ref.to_json())
        ```
        """

        params = {'@type': _model_type(model_type)}
        if uid != '':
            params['@id'] = uid
        if name != '':
            params['name'] = name
        result, err = self.__post('get/descriptor', params)
        if err:
            log.error('failed to get descriptor: %s', err)
            return None
        return schema.Ref.from_json(result)

    def get(self, model_type: Type[E],
            uid='', name='') -> Optional[E]:
        params = {'@type': _model_type(model_type)}
        if uid != '':
            params['@id'] = uid
        if name != '':
            params['name'] = name
        result, err = self.__post('get/model', params)
        if err:
            log.error('failed to get entity of type %s: %s',
                      model_type, err)
            return None
        return _model_class(model_type).from_json(result)

    def get_all(self, model_type: Type[E]) -> Iterator[E]:
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
        result, err = self.__post('get/models', params)
        if err:
            log.error('failed to get all of type %s: %s',
                      model_type, err)
        clazz = _model_class(model_type)
        for r in result:
            yield clazz.from_json(r)

    def find(self, model_type: ModelType, name: str) -> Optional[schema.Ref]:
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

    def get_providers_of(self, flow: Union[schema.Ref, schema.Flow]) \
            -> Iterator[schema.Ref]:
        """
        Get the providers for the given flow.

        For products, these are the processes that have an output of the given
        product. For waste flows, these are the waste treatment processes that
        have this flow on the input side. Elementary flows do not have a
        provider.

        Parameters
        ----------
        flow: Union[schema.Ref, schema.Flow]
            The flow or reference to the flow for which the providers should be
            returned.

        Example
        -------
        ```python
        steel = client.get('Flow', 'Steel')
        for provider in client.get_providers_of(steel):
            print(provider.name)
        ```
        """
        params = {
            '@type': 'Flow',
            '@id': flow.id,
            'name': flow.name,
        }
        providers, err = self.__post('get/providers', params)
        if err:
            log.error('failed to get providers: %s', err)
            return []
        for obj in providers:
            yield schema.Ref.from_json(obj)

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
        _, err = self.__post('export/excel', params)
        if err:
            log.error('Excel export to %s failed: %s', path, err)

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
        _, err = self.__post('dispose', arg)
        if err:
            log.error('failed to dispose object: %s', err)

    def shutdown_server(self):
        """
        Close the database and shutdown the server.

        This method is probably most useful when running a headless server
        (a server without openLCA user interface).
        """
        _, err = self.__post('runtime/shutdown', None)
        if err:
            log.error('failed to shutdown server: %s', err)

    def create_product_system(self, process_id: str, default_providers='prefer',
                              preferred_type='LCI_RESULT') -> Optional[schema.Ref]:
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

        r, err = self.__post('create/product_system', {
            'processId': process_id,
            'preferredType': preferred_type,
            'providerLinking': default_providers,
        })
        if err:
            log.error('failed to create product system: %s', err)
            return None
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
        raw, err = self.__post('get/inventory/inputs', {
            'resultId': result.id,
        })
        if err:
            log.error('failed to get LCI inputs')
            return []
        return [schema.FlowResult.from_json(it) for it in raw]

    def lci_outputs(self, result: schema.SimpleResult) -> List[dict]:
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
        raw, err = self.__post('get/inventory/outputs', {
            'resultId': result.id,
        })
        if err:
            log.error('failed to get LCI outputs: %s', err)
            return []
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
        list[ContributionItem]
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
        raw, err = self.__post('get/inventory/contributions/locations', {
            'resultId': result.id,
            'flow': flow.to_json(),
        })
        if err:
            log.error('failed to ger contributions by location')
            return []
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

        raw, err = self.__post('get/inventory/total_requirements', {
            'resultId': result.id
        })
        if err:
            log.error('failed to get total requirements %s', err)
            return []
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

        raw, err = self.__post('get/impacts', {
            'resultId': result.id,
        })
        if err:
            log.error('failed to get impact results: %s', err)
            return []
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

        raw, err = self.__post('get/impacts/contributions/flows', {
            'resultId': result.id,
            'impactCategory': impact.to_json(),
        })
        if err:
            log.error('failed to get contribution items: %s', err)
            return []
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

        raw, err = self.__post('get/impacts/contributions/locations', {
            'resultId': result.id,
            'impactCategory': impact.to_json(),
        })
        if err:
            log.error('Failed to get contribution items: %s', err)
            return []
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

        raw, err = self.__post('get/impacts/contributions/processes', {
            'resultId': result.id,
            'impactCategory': impact.to_json(),
        })
        if err:
            log.error('Failed to get contribution items: %s', err)
            return []
        return [ContributionItem.from_json(it) for it in raw]

    def upstream_tree_of(self, result: schema.SimpleResult, ref: schema.Ref,
                         max_depth=5, min_contribution=0.1,
                         max_recursion_depth=3) -> Optional[utree.UpstreamTree]:
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
        raw, err = self.__post('get/upstream/tree', {
            'resultId': result.id,
            'ref': ref.to_json(),
            'maxDepth': max_depth,
            'minContribution': min_contribution,
            'maxRecursionDepth': max_recursion_depth
        })
        if err:
            log.error('Failed to get upstream tree: %s', err)
            return None
        return utree.UpstreamTree.from_json(raw)

    def __post(self, method: str, params) -> Tuple[Any, Optional[str]]:
        """
        Performs a request with the given parameters.

        It returns a tuple (result, error).
        """
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
            err_msg = '%i: %s' % (err.get('code'), err.get('message'))
            return None, err_msg
        result = resp.get('result')
        if result is None:
            err_msg = 'No error and no result: invalid JSON-RPC response'
            return None, err_msg
        return result, None
