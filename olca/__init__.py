import datetime
import uuid

from .ipc import *
from .schema import *

from typing import Optional, TypeVar, Union

T = TypeVar('T')


def ref(model_type: Union[T, str], uid: str, name: Optional[str] = None) -> Ref:
    """
    Creates a new reference for a data set with the given type and ID.

    In the openLCA data format, references are used to point to another
    data set, e.g. when an input or output of a process points to a flow we do
    not include the complete flow but just a reference to the flow in the
    respective exchange. A reference must have a type and an ID. Other
    attributes like name, description etc. are optional but often useful when
    inspecting a data set.

    Parameters
    ----------

    model_type: Union[T, str]
        The class of the model type of the reference, e.g. olca.Flow of 'Flow'

    uid: str
        The ID (UUID) of the model / data set this reference points to.

    name: Optional[str]
        The name of the model / data set this reference points to.

    Example
    -------
    ```python
    mass_ref = olca.ref(
        olca.FlowProperty,
        '93a60a56-a3c8-11da-a746-0800200b9a66',
        'Mass')
    ```
    """
    r = Ref()
    r.olca_type = model_type if isinstance(model_type, str) \
        else model_type.__name__
    r.id = uid
    if name is not None:
        r.name = name
    return r


def unit_of(name='', conversion_factor=1.0) -> Unit:
    """
    Creates a new unit.

    Parameters
    ----------

    name: str
        The name of the unit, e.g. 'kg'

    conversion_factor: float, optional
        An optional conversion factor to the reference unit
        of the unit group where this unit lives. Defaults
        to 1.0

    Example
    -------

    ```python
    kg = olca.unit_of('kg')
    ```
    """
    unit = Unit()
    unit.id = str(uuid.uuid4())
    unit.name = name
    unit.conversion_factor = conversion_factor
    unit.reference_unit = conversion_factor == 1.0
    return unit


def unit_group_of(name: str, unit: Union[str, Unit]) -> UnitGroup:
    """
    Creates a new unit group.

    Parameters
    ----------
    name: str
        The name of the new unit group.

    unit: Union[str, Unit]
        The reference unit or the name of the reference unit of
        the new unit group.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    ```
    """
    u: Unit = unit if isinstance(unit, Unit) else unit_of(unit)
    u.reference_unit = True
    group = UnitGroup()
    _set_base_attributes(group, name)
    group.units = [u]
    return group


def flow_property_of(name: str,
                     unit_group: Union[Ref, UnitGroup]) -> FlowProperty:
    """
    Creates a new flow property (quantity).

    Parameters
    ----------
    name: str
        The name of the new flow property

    unit_group: Union[Ref, UnitGroup]
        The unit group or reference to the unit group if this flow property.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    fp = olca.flow_property_of('Mass', units)
    ```
    """
    fp = FlowProperty()
    _set_base_attributes(fp, name)
    fp.unit_group = ref('UnitGroup', unit_group.id, unit_group.name)
    return fp


def flow_of(name: str, flow_type: FlowType,
            flow_property: Union[Ref, FlowProperty]):
    """
    Creates a new flow.

    See also the more convenient methods:
    * product_flow_of
    * waste_flow_of
    * elementary_flow_of

    Parameters
    ----------
    name: str
        The name of the new flow.

    flow_type: FlowType
        The type of the new flow (product, waste, or elementary flow).

    flow_property: Union[Ref, FlowProperty]
        The (reference to the) flow property (quantity) of the flow.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    steel = olca.flow_of('Steel', olca.FlowType.PRODUCT_FLOW, mass)
    ```
    """

    flow = Flow()
    _set_base_attributes(flow, name)
    flow.flow_type = flow_type

    prop = FlowPropertyFactor()
    prop.conversion_factor = 1.0
    prop.reference_flow_property = True
    prop.flow_property = ref(
        'FlowProperty', flow_property.id, flow_property.name)
    flow.flow_properties = [prop]
    return flow


def product_flow_of(name: str, flow_property: Union[Ref, FlowProperty]) -> Flow:
    """
    Creates a new product flow.

    Parameters
    ----------
    name: str
        The name of the new flow.

    flow_property: Union[Ref, FlowProperty]
        The (reference to the) flow property (quantity) of the flow.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    steel = olca.product_flow_of('Steel', mass)
    ```
    """
    return flow_of(name, FlowType.PRODUCT_FLOW, flow_property)


def waste_flow_of(name: str, flow_property: Union[Ref, FlowProperty]) -> Flow:
    """
    Creates a new waste flow.

    Parameters
    ----------
    name: str
        The name of the new flow.

    flow_property: Union[Ref, FlowProperty]
        The (reference to the) flow property (quantity) of the flow.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    scrap = olca.waste_flow_of('Scrap', mass)
    ```
    """
    return flow_of(name, FlowType.WASTE_FLOW, flow_property)


def elementary_flow_of(name: str, flow_property: Union[Ref, FlowProperty]) -> Flow:
    """
    Creates a new elementary flow.

    Parameters
    ----------
    name: str
        The name of the new flow.

    flow_property: Union[Ref, FlowProperty]
        The (reference to the) flow property (quantity) of the flow.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    co2 = olca.elementary_flow_of('CO2', mass)
    ```
    """
    return flow_of(name, FlowType.ELEMENTARY_FLOW, flow_property)


def process_of(name: str) -> Process:
    """
    Creates a new process.

    Parameters
    ----------
    name: str
        The name of the new process.

    Example
    -------
    ```python
    process = olca.process_of('Steel production')
    ```
    """
    process = Process()
    _set_base_attributes(process, name)
    process.process_type = ProcessType.UNIT_PROCESS
    return process


def exchange_of(process: Process,
                flow: Union[Ref, Flow],
                amount: Union[str, float] = 1.0,
                unit: Optional[Union[Ref, Unit]] = None) -> Exchange:
    """
    Creates a new exchange.

    See the more convenient functions:
    * input_of
    * output_of

    Parameters
    ----------
    process: Process
        The process of the new exchange.
    
    flow: Union[Ref, Flow]
        The flow or reference to the flow of this exchange.

    amount: Union[str, float], optional
        The amount of the exchange; defaults to 1.0. Strings a floating point
        numbers are allowed. If a string is passed as amount, we assume that
        it is a valid formula.

    unit: Union[Ref, Unit], optional
        The unit of the exchange. If not provided the exchange amount is given
        in the reference unit of the linked flow.
    
    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    steel = olca.product_flow_of('Steel', mass)
    process = olca.process_of('Steel production')
    output = exchange_of(process, steel, 1.0)
    output.quantitative_reference = True
    ```
    """
    if process.last_internal_id is None:
        internal_id = 1
    else:
        internal_id = process.last_internal_id + 1
    process.last_internal_id = internal_id
    exchange = Exchange()
    exchange.internal_id = internal_id
    if isinstance(amount, str):
        exchange.amount_formula = amount
    else:
        exchange.amount = amount
    exchange.flow = ref('Flow', flow.id, flow.name)
    if unit:
        exchange.unit = ref('Unit', unit.id, unit.name)
    if process.exchanges is None:
        process.exchanges = [exchange]
    else:
        process.exchanges.append(exchange)
    return exchange


def output_of(process: Process,
              flow: Union[Ref, Flow],
              amount: Union[str, float] = 1.0,
              unit: Optional[Union[Ref, Unit]] = None) -> Exchange:
    """
    Creates a new output.

    This is the same as `exchange_of` but it sets the the exchange as an
    output additionally.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    steel = olca.product_flow_of('Steel', mass)
    process = olca.process_of('Steel production')
    output = olca.output_of(process, steel, 1.0)
    output.quantitative_reference = True
    ```
    """
    exchange = exchange_of(process, flow, amount, unit)
    exchange.input = False
    return exchange


def input_of(process: Process,
             flow: Union[Ref, Flow],
             amount: Union[str, float] = 1.0,
             unit: Optional[Union[Ref, Unit]] = None) -> Exchange:
    """
    Creates a new input.

    This is the same as `exchange_of` but it sets the the exchange as an
    input additionally.

    Example
    -------
    ```python
    units = olca.unit_group_of('Units of mass', 'kg')
    mass = olca.flow_property_of('Mass', units)
    scrap = olca.waste_flow_of('Scrap', mass)
    process = olca.process_of('Steel production')
    input = olca.input_of(process, scrap, 0.1)
    ```
    """
    exchange = exchange_of(process, flow, amount, unit)
    exchange.input = True
    return exchange


def location_of(name: str, code: Optional[str] = None) -> Location:
    """
    Creates a new location.

    Parameters
    ----------
    name: str
        The name of the new location.

    code: Optional[str]
        An optional location code.

    Example
    -------
    ```python
    de = olca.location_of('Germany', 'DE')
    ```
    """
    location = Location()
    _set_base_attributes(location, name)
    location.code = code or name
    return location


def parameter_of(name: str, value: Union[str, float],
                 scope=ParameterScope.GLOBAL_SCOPE) -> Parameter:
    """
    Creates a new parameter.

    Parameters
    ----------
    name: str
        The name of the new parameter. Note that parameters can be used
        in formulas. So that the name of the parameter has to follow
        specific syntax rules, i.e. it cannot contain whitespaces or
        special characters.
    value: Union[str, float]
        The parameter value. If a string is passed as value into this
        function we assume that this is a formula and we will create
        a dependent, calculated parameter. Otherwise we create an
        input parameter
    scope: ParameterScope, optional
        The scope of the parameter. If not specified otherwise this
        defaults to global scope.

    Example
    -------
    ```python
    import olca

    # create a global input parameter
    global_scrap_rate = olca.parameter_of('global_scrap_rate', 1.0)

    # create a local calculated parameter of a process
    local_scrap_rate = olca.parameter_of(
        'local_scrap_rate',
        'global_scrap_rate * 0.9',
        olca.ParameterScope.PROCESS_SCOPE)
    process = olca.process_of('Steel production')
    process.parameters = [local_scrap_rate]

    # insert this in a database
    with olca.Client() as client:
        client.insert(global_scrap_rate)
        client.insert(process)
    ```
    """
    param = Parameter()
    _set_base_attributes(param, name)
    param.parameter_scope = scope
    if isinstance(value, str):
        param.formula = value
        param.input_parameter = False
    else:
        param.value = value
        param.input_parameter = True
    return param


def physical_allocation_of(
        process: Process,
        product: Union[Ref, Flow],
        amount: Union[str, float]) -> AllocationFactor:
    f = _allocation_of(process, product, amount)
    f.allocation_type = AllocationType.PHYSICAL_ALLOCATION
    return f


def economic_allocation_of(
        process: Process,
        product: Union[Ref, Flow],
        amount: Union[str, float]) -> AllocationFactor:
    f = _allocation_of(process, product, amount)
    f.allocation_type = AllocationType.ECONOMIC_ALLOCATION
    return f


def causal_allocation_of(
        process: Process,
        product: Union[Ref, Flow],
        amount: Union[str, float],
        exchange: Union[Exchange, ExchangeRef]) -> AllocationFactor:
    f = _allocation_of(process, product, amount)
    f.allocation_type = AllocationType.CAUSAL_ALLOCATION
    f.exchange = ExchangeRef()
    f.exchange.internal_id = exchange.internal_id
    return f


def _allocation_of(
        process: Process,
        product: Union[Ref, Flow],
        amount: Union[str, float]) -> AllocationFactor:
    f = AllocationFactor()
    f.product = ref(Flow, product.id, product.name)
    if isinstance(amount, str):
        f.formula = amount
    else:
        f.value = amount
    if process.allocation_factors is None:
        process.allocation_factors = [f]
    else:
        process.allocation_factors.append(f)
    return f


def _set_base_attributes(entity: RootEntity, name: str):
    entity.id = str(uuid.uuid4())
    entity.name = name
    entity.version = '00.00.000'
    entity.last_change = datetime.datetime.utcnow().isoformat() + 'Z'
