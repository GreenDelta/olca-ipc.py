# DO NOT CHANGE THIS CODE AS THIS IS GENERATED AUTOMATICALLY

# This module contains a Python API of the JSON-LD based
# openLCA data exchange model.package schema.
# For more information see http://greendelta.github.io/olca-schema/

from __future__ import annotations

import json as jsonlib

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class AllocationType(Enum):
    """
    An enumeration type for allocation methods. This type is used to define the
    type of an [AllocationFactor], the default allocation method of a
    multi-functional [Process], or the allocation method in a
    [CalculationSetup].
    """

    PHYSICAL_ALLOCATION = 'PHYSICAL_ALLOCATION'
    ECONOMIC_ALLOCATION = 'ECONOMIC_ALLOCATION'
    CAUSAL_ALLOCATION = 'CAUSAL_ALLOCATION'
    USE_DEFAULT_ALLOCATION = 'USE_DEFAULT_ALLOCATION'
    NO_ALLOCATION = 'NO_ALLOCATION'


class CalculationType(Enum):
    """
    An enumeration of the different calculation methods supported by openLCA.
    """

    SIMPLE_CALCULATION = 'SIMPLE_CALCULATION'
    """
    Calculates the total results for elementary flows, LCIA indicators, costs,
    etc. of a product system.
    """

    CONTRIBUTION_ANALYSIS = 'CONTRIBUTION_ANALYSIS'
    """
    Includes the total result vectors of a simple calculation but calculates
    also the direct contributions of each process (or better process product in
    case of multi-output processes) to these total results.
    """

    UPSTREAM_ANALYSIS = 'UPSTREAM_ANALYSIS'
    """
    Extends the contribution analysis by providing also the upstream results of
    each process (process product) in the product system. The upstream result
    contains the direct contributions of the respective process but also the
    result of the supply chain up to this process scaled to the demand of the
    process in the product system.
    """

    REGIONALIZED_CALCULATION = 'REGIONALIZED_CALCULATION'
    """
    A regionalized calculation is a contribution analysis but with an LCIA
    method that supports regionalized characterization factors (via region
    specific parameters in formulas) and a product system with processes that
    have geographic information assigned (point, line, or polygon shapes).
    """

    MONTE_CARLO_SIMULATION = 'MONTE_CARLO_SIMULATION'
    """
    A Monte Carlo simulation generates for each run, of a given number of a
    given number of iterations, random values according to the uncertainty
    distributions of process inputs/outputs, parameters, characterization
    factors, etc. of a product system and then performs a simple calculation
    for that specific run.
    """



class FlowPropertyType(Enum):
    """
    An enumeration of flow property types.
    """

    ECONOMIC_QUANTITY = 'ECONOMIC_QUANTITY'
    PHYSICAL_QUANTITY = 'PHYSICAL_QUANTITY'


class FlowType(Enum):
    """
    The basic flow types.
    """

    ELEMENTARY_FLOW = 'ELEMENTARY_FLOW'
    PRODUCT_FLOW = 'PRODUCT_FLOW'
    WASTE_FLOW = 'WASTE_FLOW'


class ModelType(Enum):
    """
    An enumeration of the root entity types.
    """

    ACTOR = 'ACTOR'
    CATEGORY = 'CATEGORY'
    CURRENCY = 'CURRENCY'
    DQ_SYSTEM = 'DQ_SYSTEM'
    FLOW = 'FLOW'
    FLOW_PROPERTY = 'FLOW_PROPERTY'
    IMPACT_CATEGORY = 'IMPACT_CATEGORY'
    IMPACT_METHOD = 'IMPACT_METHOD'
    LOCATION = 'LOCATION'
    NW_SET = 'NW_SET'
    PARAMETER = 'PARAMETER'
    PROCESS = 'PROCESS'
    PRODUCT_SYSTEM = 'PRODUCT_SYSTEM'
    PROJECT = 'PROJECT'
    SOCIAL_INDICATOR = 'SOCIAL_INDICATOR'
    SOURCE = 'SOURCE'
    UNIT = 'UNIT'
    UNIT_GROUP = 'UNIT_GROUP'


class ParameterScope(Enum):
    """
    The possible scopes of parameters. Parameters can be defined globally, in
    processes, or impact categories. They can be redefined in calculation
    setups on the project and product system level, but the initial definition
    is always only global, in a process, or an LCIA category.
    """

    PROCESS_SCOPE = 'PROCESS_SCOPE'
    """
    Indicates that the evaluation scope of a parameter is the process where it
    is defined.
    """

    IMPACT_SCOPE = 'IMPACT_SCOPE'
    """
    Indicates that the evaluation scope of a parameter is the impact category
    where it is defined.
    """

    GLOBAL_SCOPE = 'GLOBAL_SCOPE'
    """
    Indicates that the evaluation scope of a parameter is the global scope.
    """



class ProcessType(Enum):
    LCI_RESULT = 'LCI_RESULT'
    UNIT_PROCESS = 'UNIT_PROCESS'


class RiskLevel(Enum):
    """

    """

    NO_OPPORTUNITY = 'NO_OPPORTUNITY'
    HIGH_OPPORTUNITY = 'HIGH_OPPORTUNITY'
    MEDIUM_OPPORTUNITY = 'MEDIUM_OPPORTUNITY'
    LOW_OPPORTUNITY = 'LOW_OPPORTUNITY'
    NO_RISK = 'NO_RISK'
    VERY_LOW_RISK = 'VERY_LOW_RISK'
    LOW_RISK = 'LOW_RISK'
    MEDIUM_RISK = 'MEDIUM_RISK'
    HIGH_RISK = 'HIGH_RISK'
    VERY_HIGH_RISK = 'VERY_HIGH_RISK'
    NO_DATA = 'NO_DATA'
    NOT_APPLICABLE = 'NOT_APPLICABLE'


class UncertaintyType(Enum):
    """
    Enumeration of uncertainty distribution types that can be used in
    exchanges, parameters, LCIA factors, etc.
    """

    LOG_NORMAL_DISTRIBUTION = 'LOG_NORMAL_DISTRIBUTION'
    NORMAL_DISTRIBUTION = 'NORMAL_DISTRIBUTION'
    TRIANGLE_DISTRIBUTION = 'TRIANGLE_DISTRIBUTION'
    UNIFORM_DISTRIBUTION = 'UNIFORM_DISTRIBUTION'



@dataclass
class Entity(object):
    """
    The most generic type of the openLCA data model.
    """

    id: str = ''
    olca_type: str = ''

    def _repr_html_(self):
        code = jsonlib.dumps(self.to_json(), indent=2, sort_keys=True)
        if len(code) > 10000:
            code = code[0:10000] + '...'
        return f'<pre><code class="language-json">{code}</code></pre>'
        
    def to_json(self) -> dict:
        o_type = self.olca_type
        if o_type is None:
            o_type = type(self).__name__
        json = {'@type': o_type}
        if self.id is not None:
            json['@id'] = self.id
        return json

    def read_json(self, json: dict):
        self.id = json.get('@id')
        self.olca_type = json.get('@type')

    @staticmethod
    def from_json(json: dict):
        instance = Entity()
        instance.read_json(json)
        return instance


@dataclass
class AllocationFactor(Entity):
    """
    A single allocation factor in a process.

    Attributes
    ----------
    allocation_type: AllocationType
        The type of allocation.

    product: Ref
        The output product (or waste input) to which this allocation factor is
        related. The must be an exchange with this product output (or waste
        input) in this process.

    value: float
        The value of the allocation factor.

    formula: str
        An optional formula from which the value of the allocation factor is
        calculated.

    exchange: ExchangeRef
        A product input, waste output, or elementary flow exchange which is
        allocated by this factor. This is only valid for causal allocation
        where allocation factors can be assigned to single exchanges.

    """

    olca_type: str = 'AllocationFactor'
    allocation_type: Optional[AllocationType] = None
    product: Optional[Ref] = None
    value: Optional[float] = None
    formula: Optional[str] = None
    exchange: Optional[ExchangeRef] = None

    def to_json(self) -> dict:
        json: dict = super(AllocationFactor, self).to_json()
        if self.allocation_type is not None:
            json['allocationType'] = self.allocation_type.value
        if self.product is not None:
            json['product'] = self.product.to_json()
        if self.value is not None:
            json['value'] = self.value
        if self.formula is not None:
            json['formula'] = self.formula
        if self.exchange is not None:
            json['exchange'] = self.exchange.to_json()
        return json

    def read_json(self, json: dict):
        super(AllocationFactor, self).read_json(json)
        val = json.get('allocationType')
        if val is not None:
            self.allocation_type = AllocationType(val)
        val = json.get('product')
        if val is not None:
            self.product = Ref()
            self.product.read_json(val)
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('formula')
        if val is not None:
            self.formula = val
        val = json.get('exchange')
        if val is not None:
            self.exchange = ExchangeRef()
            self.exchange.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = AllocationFactor()
        instance.read_json(json)
        return instance


@dataclass
class CalculationSetup(Entity):
    """
    A setup for a product system calculation.

    Attributes
    ----------
    calculation_type: CalculationType
        The type of calculation that should be performed.

    product_system: Ref
        The product system that should be calculated (required).

    impact_method: Ref
        The LCIA method for the calculation (optional).

    with_costs: bool
        Indicates whether life cycle costs should be also calculated
        (optional).

    with_regionalization: bool
        Indicates whether a regionalized result should be calculated or not. If
        this is set to true, the intervention matrix is indexed by (elementary
        flow, location) - pairs instead of just elementary flows. The LCI
        result then contains results for these pairs which can be then used in
        regionalized impact assessments.

    nw_set: Ref
        The normalisation and weighting set for the calculation (optional).

    allocation_method: AllocationType
        The calculation type to be used in the calculation (optional).

    parameter_redefs: List[ParameterRedef]
        A list of parameter redefinitions to be used in the calculation
        (optional).

    amount: float
        (optional)

    unit: Ref
        (optional)

    flow_property: Ref
        (optional)

    """

    olca_type: str = 'CalculationSetup'
    calculation_type: Optional[CalculationType] = None
    product_system: Optional[Ref] = None
    impact_method: Optional[Ref] = None
    with_costs: Optional[bool] = None
    with_regionalization: Optional[bool] = None
    nw_set: Optional[Ref] = None
    allocation_method: Optional[AllocationType] = None
    parameter_redefs: Optional[List[ParameterRedef]] = None
    amount: Optional[float] = None
    unit: Optional[Ref] = None
    flow_property: Optional[Ref] = None

    def to_json(self) -> dict:
        json: dict = super(CalculationSetup, self).to_json()
        if self.calculation_type is not None:
            json['calculationType'] = self.calculation_type.value
        if self.product_system is not None:
            json['productSystem'] = self.product_system.to_json()
        if self.impact_method is not None:
            json['impactMethod'] = self.impact_method.to_json()
        if self.with_costs is not None:
            json['withCosts'] = self.with_costs
        if self.with_regionalization is not None:
            json['withRegionalization'] = self.with_regionalization
        if self.nw_set is not None:
            json['nwSet'] = self.nw_set.to_json()
        if self.allocation_method is not None:
            json['allocationMethod'] = self.allocation_method.value
        if self.parameter_redefs is not None:
            json['parameterRedefs'] = []
            for e in self.parameter_redefs:
                json['parameterRedefs'].append(e.to_json())
        if self.amount is not None:
            json['amount'] = self.amount
        if self.unit is not None:
            json['unit'] = self.unit.to_json()
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        return json

    def read_json(self, json: dict):
        super(CalculationSetup, self).read_json(json)
        val = json.get('calculationType')
        if val is not None:
            self.calculation_type = CalculationType(val)
        val = json.get('productSystem')
        if val is not None:
            self.product_system = Ref()
            self.product_system.read_json(val)
        val = json.get('impactMethod')
        if val is not None:
            self.impact_method = Ref()
            self.impact_method.read_json(val)
        val = json.get('withCosts')
        if val is not None:
            self.with_costs = val
        val = json.get('withRegionalization')
        if val is not None:
            self.with_regionalization = val
        val = json.get('nwSet')
        if val is not None:
            self.nw_set = Ref()
            self.nw_set.read_json(val)
        val = json.get('allocationMethod')
        if val is not None:
            self.allocation_method = AllocationType(val)
        val = json.get('parameterRedefs')
        if val is not None:
            self.parameter_redefs = []
            for d in val:
                e = ParameterRedef()
                e.read_json(d)
                self.parameter_redefs.append(e)
        val = json.get('amount')
        if val is not None:
            self.amount = val
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.read_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = CalculationSetup()
        instance.read_json(json)
        return instance


@dataclass
class DQIndicator(Entity):
    """
    An indicator of a data quality system ([DQSystem]).

    Attributes
    ----------
    name: str

    position: int

    scores: List[DQScore]

    """

    olca_type: str = 'DQIndicator'
    name: Optional[str] = None
    position: Optional[int] = None
    scores: Optional[List[DQScore]] = None

    def to_json(self) -> dict:
        json: dict = super(DQIndicator, self).to_json()
        if self.name is not None:
            json['name'] = self.name
        if self.position is not None:
            json['position'] = self.position
        if self.scores is not None:
            json['scores'] = []
            for e in self.scores:
                json['scores'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(DQIndicator, self).read_json(json)
        val = json.get('name')
        if val is not None:
            self.name = val
        val = json.get('position')
        if val is not None:
            self.position = val
        val = json.get('scores')
        if val is not None:
            self.scores = []
            for d in val:
                e = DQScore()
                e.read_json(d)
                self.scores.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = DQIndicator()
        instance.read_json(json)
        return instance


@dataclass
class DQScore(Entity):
    """
    An score value of an indicator ([DQIndicator]) in a data quality system
    ([DQSystem]).

    Attributes
    ----------
    position: int

    label: str

    description: str

    uncertainty: float

    """

    olca_type: str = 'DQScore'
    position: Optional[int] = None
    label: Optional[str] = None
    description: Optional[str] = None
    uncertainty: Optional[float] = None

    def to_json(self) -> dict:
        json: dict = super(DQScore, self).to_json()
        if self.position is not None:
            json['position'] = self.position
        if self.label is not None:
            json['label'] = self.label
        if self.description is not None:
            json['description'] = self.description
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty
        return json

    def read_json(self, json: dict):
        super(DQScore, self).read_json(json)
        val = json.get('position')
        if val is not None:
            self.position = val
        val = json.get('label')
        if val is not None:
            self.label = val
        val = json.get('description')
        if val is not None:
            self.description = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = val

    @staticmethod
    def from_json(json: dict):
        instance = DQScore()
        instance.read_json(json)
        return instance


@dataclass
class Exchange(Entity):
    """
    An Exchange is an input or output of a [Flow] in a [Process]. The amount of
    an exchange is given in a specific unit of a quantity ([FlowProperty]) of
    the flow. The allowed units and flow properties that can be used for a flow
    in an exchange are defined by the flow property information in that flow
    (see also the [FlowPropertyFactor] type).

    Attributes
    ----------
    avoided_product: bool
        Indicates whether this exchange is an avoided product.

    cost_formula: str
        A formula for calculating the costs of this exchange.

    cost_value: float
        The costs of this exchange.

    currency: Ref
        The currency in which the costs of this exchange are given.

    internal_id: int
        The process internal ID of the exchange. This is used to identify
        exchanges unambiguously within a process (e.g. when linking exchanges
        in a product system where multiple exchanges with the same flow are
        allowed). The value should be >= 1.

    flow: Ref
        The reference to the flow of the exchange.

    flow_property: Ref
        The quantity in which the amount is given.

    input: bool

    quantitative_reference: bool
        Indicates whether the exchange is the quantitative reference of the
        process.

    base_uncertainty: float

    default_provider: Ref
        A default provider is a [Process] that is linked as the provider of a
        product input or the waste treatment provider of a waste output. It is
        just an optional default setting which can be also ignored when
        building product systems in openLCA. The user is always free to link
        processes in product systems ignoring these defaults (but the flows and
        flow directions have to match of course).

    amount: float

    amount_formula: str

    unit: Ref

    dq_entry: str
        A data quality entry like `(1;3;2;5;1)`. The entry is a vector of data
        quality values that need to match the data quality scheme for flow
        inputs and outputs that is assigned to the [Process]. In such a scheme
        the data quality indicators have fixed positions and the respective
        values in the `dqEntry` vector map to these positions.

    uncertainty: Uncertainty

    description: str
        A general comment about the input or output.

    """

    olca_type: str = 'Exchange'
    avoided_product: Optional[bool] = None
    cost_formula: Optional[str] = None
    cost_value: Optional[float] = None
    currency: Optional[Ref] = None
    internal_id: Optional[int] = None
    flow: Optional[Ref] = None
    flow_property: Optional[Ref] = None
    input: Optional[bool] = None
    quantitative_reference: Optional[bool] = None
    base_uncertainty: Optional[float] = None
    default_provider: Optional[Ref] = None
    amount: Optional[float] = None
    amount_formula: Optional[str] = None
    unit: Optional[Ref] = None
    dq_entry: Optional[str] = None
    uncertainty: Optional[Uncertainty] = None
    description: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(Exchange, self).to_json()
        if self.avoided_product is not None:
            json['avoidedProduct'] = self.avoided_product
        if self.cost_formula is not None:
            json['costFormula'] = self.cost_formula
        if self.cost_value is not None:
            json['costValue'] = self.cost_value
        if self.currency is not None:
            json['currency'] = self.currency.to_json()
        if self.internal_id is not None:
            json['internalId'] = self.internal_id
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        if self.input is not None:
            json['input'] = self.input
        if self.quantitative_reference is not None:
            json['quantitativeReference'] = self.quantitative_reference
        if self.base_uncertainty is not None:
            json['baseUncertainty'] = self.base_uncertainty
        if self.default_provider is not None:
            json['defaultProvider'] = self.default_provider.to_json()
        if self.amount is not None:
            json['amount'] = self.amount
        if self.amount_formula is not None:
            json['amountFormula'] = self.amount_formula
        if self.unit is not None:
            json['unit'] = self.unit.to_json()
        if self.dq_entry is not None:
            json['dqEntry'] = self.dq_entry
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty.to_json()
        if self.description is not None:
            json['description'] = self.description
        return json

    def read_json(self, json: dict):
        super(Exchange, self).read_json(json)
        val = json.get('avoidedProduct')
        if val is not None:
            self.avoided_product = val
        val = json.get('costFormula')
        if val is not None:
            self.cost_formula = val
        val = json.get('costValue')
        if val is not None:
            self.cost_value = val
        val = json.get('currency')
        if val is not None:
            self.currency = Ref()
            self.currency.read_json(val)
        val = json.get('internalId')
        if val is not None:
            self.internal_id = val
        val = json.get('flow')
        if val is not None:
            self.flow = Ref()
            self.flow.read_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.read_json(val)
        val = json.get('input')
        if val is not None:
            self.input = val
        val = json.get('quantitativeReference')
        if val is not None:
            self.quantitative_reference = val
        val = json.get('baseUncertainty')
        if val is not None:
            self.base_uncertainty = val
        val = json.get('defaultProvider')
        if val is not None:
            self.default_provider = Ref()
            self.default_provider.read_json(val)
        val = json.get('amount')
        if val is not None:
            self.amount = val
        val = json.get('amountFormula')
        if val is not None:
            self.amount_formula = val
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.read_json(val)
        val = json.get('dqEntry')
        if val is not None:
            self.dq_entry = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.read_json(val)
        val = json.get('description')
        if val is not None:
            self.description = val

    @staticmethod
    def from_json(json: dict):
        instance = Exchange()
        instance.read_json(json)
        return instance


@dataclass
class ExchangeRef(Entity):
    """
    An instance of this class describes a reference to an exchange in a
    process. When we reference such an exchange we only need the information to
    indentify that exchange unambiguously in a process.

    Attributes
    ----------
    internal_id: int
        The internal ID of the exchange.

    """

    olca_type: str = 'ExchangeRef'
    internal_id: Optional[int] = None

    def to_json(self) -> dict:
        json: dict = super(ExchangeRef, self).to_json()
        if self.internal_id is not None:
            json['internalId'] = self.internal_id
        return json

    def read_json(self, json: dict):
        super(ExchangeRef, self).read_json(json)
        val = json.get('internalId')
        if val is not None:
            self.internal_id = val

    @staticmethod
    def from_json(json: dict):
        instance = ExchangeRef()
        instance.read_json(json)
        return instance


@dataclass
class FlowMapEntry(Entity):
    """
    A mapping from a source flow to a target flow.

    Attributes
    ----------
    from_: FlowMapRef
        Describes the source flow of the mapping.

    to: FlowMapRef
        Describes the target of the mapping.

    conversion_factor: float
        The conversion factor to convert the amount of 1 unit of the source
        flow into the corresponding quantity of the target flow.

    """

    olca_type: str = 'FlowMapEntry'
    from_: Optional[FlowMapRef] = None
    to: Optional[FlowMapRef] = None
    conversion_factor: Optional[float] = None

    def to_json(self) -> dict:
        json: dict = super(FlowMapEntry, self).to_json()
        if self.from_ is not None:
            json['from'] = self.from_.to_json()
        if self.to is not None:
            json['to'] = self.to.to_json()
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        return json

    def read_json(self, json: dict):
        super(FlowMapEntry, self).read_json(json)
        val = json.get('from')
        if val is not None:
            self.from_ = FlowMapRef()
            self.from_.read_json(val)
        val = json.get('to')
        if val is not None:
            self.to = FlowMapRef()
            self.to.read_json(val)
        val = json.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val

    @staticmethod
    def from_json(json: dict):
        instance = FlowMapEntry()
        instance.read_json(json)
        return instance


@dataclass
class FlowMapRef(Entity):
    """
    Describes a source or target flow in a `FlowMappingEntry` of a `FlowMap`.
    Such a flow reference can also optionally specify the unit and flow
    property (quantity) for which the mapping is valid. If the unit or quantity
    is not given, the mapping is based on the respective reference unit and
    reference flow property of the flow.

    Attributes
    ----------
    flow: Ref
        The reference to the flow data set.

    flow_property: Ref
        An optional reference to a flow property of the flow for which the
        mapping is valid.

    unit: Ref
        An optional reference to a unit of the flow for which the mapping is
        valid

    provider: Ref
        In case of a product or waste flow a flow mapping can contain a
        provider which is the process that produces the product or a waste
        treatment process that consumes the waste flow. This is useful when we
        want to apply mappings of product and waste flows on databases and link
        them in the corresponding processes and product systems.

    """

    olca_type: str = 'FlowMapRef'
    flow: Optional[Ref] = None
    flow_property: Optional[Ref] = None
    unit: Optional[Ref] = None
    provider: Optional[Ref] = None

    def to_json(self) -> dict:
        json: dict = super(FlowMapRef, self).to_json()
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        if self.unit is not None:
            json['unit'] = self.unit.to_json()
        if self.provider is not None:
            json['provider'] = self.provider.to_json()
        return json

    def read_json(self, json: dict):
        super(FlowMapRef, self).read_json(json)
        val = json.get('flow')
        if val is not None:
            self.flow = Ref()
            self.flow.read_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.read_json(val)
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.read_json(val)
        val = json.get('provider')
        if val is not None:
            self.provider = Ref()
            self.provider.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = FlowMapRef()
        instance.read_json(json)
        return instance


@dataclass
class FlowPropertyFactor(Entity):
    """
    A FlowPropertyFactor is a conversion factor between <a
    href="./FlowProperty.html">flow properties (quantities)</a> of a <a
    href="./Flow.html">flow</a>. As an example the amount of the flow 'water'
    in a process could be expressed in 'kg' mass or 'm3' volume. In this case
    the flow water would have two flow property factors: one for the flow
    property 'mass' and one for 'volume'. Each of these flow properties has a
    reference to a <a href="./UnitGroup.html">unit group</a> which again has a
    reference unit. In the example the flow property 'mass' could reference the
    unit group 'units of mass' with 'kg' as reference unit and volume could
    reference the unit group 'units of volume' with 'm3' as reference unit. The
    flow property factor is now the conversion factor between these two
    reference units where the factor of the reference flow property of the flow
    is 1. If the reference flow property of 'water' in the example would be
    'mass' the respective flow property factor would be 1 and the factor for
    'volume' would be 0.001 (as 1 kg water is 0.001 m3). The amount of water in
    a process can now be also given in liter, tons, grams etc. For this, the
    unit conversion factor of the respective unit group can be used to convert
    into the reference unit (which then can be used to convert to the reference
    unit of another flow property). Another thing to note is that different
    flow properties can refer to the same unit group (e.g. MJ upper calorific
    value and MJ lower calorific value.)

    Attributes
    ----------
    flow_property: Ref
        The flow property (quantity) of the factor.

    conversion_factor: float
        The value of the conversion factor.

    reference_flow_property: bool
        Indicates whether the flow property of the factor is the reference flow
        property of the flow. The reference flow property must have a
        conversion factor of 1.0 and there should be only one reference flow
        property.

    """

    olca_type: str = 'FlowPropertyFactor'
    flow_property: Optional[Ref] = None
    conversion_factor: Optional[float] = None
    reference_flow_property: Optional[bool] = None

    def to_json(self) -> dict:
        json: dict = super(FlowPropertyFactor, self).to_json()
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        if self.reference_flow_property is not None:
            json['referenceFlowProperty'] = self.reference_flow_property
        return json

    def read_json(self, json: dict):
        super(FlowPropertyFactor, self).read_json(json)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.read_json(val)
        val = json.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val
        val = json.get('referenceFlowProperty')
        if val is not None:
            self.reference_flow_property = val

    @staticmethod
    def from_json(json: dict):
        instance = FlowPropertyFactor()
        instance.read_json(json)
        return instance


@dataclass
class FlowResult(Entity):
    """
    A result value for a flow; given in the reference unit of the flow.

    Attributes
    ----------
    flow: Ref
        The flow reference.

    input: bool
        Indicates whether the flow is an input or not.

    value: float
        The value of the flow amount.

    location: Ref
        The (reference to the) location of this flow result in case of a
        regionalized result.

    """

    olca_type: str = 'FlowResult'
    flow: Optional[Ref] = None
    input: Optional[bool] = None
    value: Optional[float] = None
    location: Optional[Ref] = None

    def to_json(self) -> dict:
        json: dict = super(FlowResult, self).to_json()
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.input is not None:
            json['input'] = self.input
        if self.value is not None:
            json['value'] = self.value
        if self.location is not None:
            json['location'] = self.location.to_json()
        return json

    def read_json(self, json: dict):
        super(FlowResult, self).read_json(json)
        val = json.get('flow')
        if val is not None:
            self.flow = Ref()
            self.flow.read_json(val)
        val = json.get('input')
        if val is not None:
            self.input = val
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('location')
        if val is not None:
            self.location = Ref()
            self.location.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = FlowResult()
        instance.read_json(json)
        return instance


@dataclass
class ImpactFactor(Entity):
    """
    A single characterisation factor of a LCIA category for a flow.

    Attributes
    ----------
    flow: Ref
        The [Flow] of the impact assessment factor.

    location: Ref
        In case of a regionalized impact category, this field can contain the
        location for which this factor is valid.

    flow_property: Ref
        The quantity of the flow to which the LCIA factor is related (e.g.
        Mass).

    unit: Ref
        The flow unit to which the LCIA factor is related (e.g. kg).

    value: float
        The value of the impact assessment factor.

    formula: str
        A mathematical formula for calculating the value of the LCIA factor.

    uncertainty: Uncertainty
        The uncertainty distribution of the factors' value.

    """

    olca_type: str = 'ImpactFactor'
    flow: Optional[Ref] = None
    location: Optional[Ref] = None
    flow_property: Optional[Ref] = None
    unit: Optional[Ref] = None
    value: Optional[float] = None
    formula: Optional[str] = None
    uncertainty: Optional[Uncertainty] = None

    def to_json(self) -> dict:
        json: dict = super(ImpactFactor, self).to_json()
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.location is not None:
            json['location'] = self.location.to_json()
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        if self.unit is not None:
            json['unit'] = self.unit.to_json()
        if self.value is not None:
            json['value'] = self.value
        if self.formula is not None:
            json['formula'] = self.formula
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty.to_json()
        return json

    def read_json(self, json: dict):
        super(ImpactFactor, self).read_json(json)
        val = json.get('flow')
        if val is not None:
            self.flow = Ref()
            self.flow.read_json(val)
        val = json.get('location')
        if val is not None:
            self.location = Ref()
            self.location.read_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.read_json(val)
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.read_json(val)
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('formula')
        if val is not None:
            self.formula = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = ImpactFactor()
        instance.read_json(json)
        return instance


@dataclass
class ImpactResult(Entity):
    """
    A result value for an impact assessment category.

    Attributes
    ----------
    impact_category: Ref
        The reference to the impact assessment category.

    value: float
        The value of the flow amount.

    """

    olca_type: str = 'ImpactResult'
    impact_category: Optional[Ref] = None
    value: Optional[float] = None

    def to_json(self) -> dict:
        json: dict = super(ImpactResult, self).to_json()
        if self.impact_category is not None:
            json['impactCategory'] = self.impact_category.to_json()
        if self.value is not None:
            json['value'] = self.value
        return json

    def read_json(self, json: dict):
        super(ImpactResult, self).read_json(json)
        val = json.get('impactCategory')
        if val is not None:
            self.impact_category = Ref()
            self.impact_category.read_json(val)
        val = json.get('value')
        if val is not None:
            self.value = val

    @staticmethod
    def from_json(json: dict):
        instance = ImpactResult()
        instance.read_json(json)
        return instance


@dataclass
class NwFactor(Entity):
    """
    A normalization and weighting factor of a [NwSet] related to an impact
    category. Depending on the purpose of the [NwSet] (normalization,
    weighting, or both) the normalization and weighting factor can be present
    or not.

    Attributes
    ----------
    impact_category: Ref

    normalisation_factor: float

    weighting_factor: float

    """

    olca_type: str = 'NwFactor'
    impact_category: Optional[Ref] = None
    normalisation_factor: Optional[float] = None
    weighting_factor: Optional[float] = None

    def to_json(self) -> dict:
        json: dict = super(NwFactor, self).to_json()
        if self.impact_category is not None:
            json['impactCategory'] = self.impact_category.to_json()
        if self.normalisation_factor is not None:
            json['normalisationFactor'] = self.normalisation_factor
        if self.weighting_factor is not None:
            json['weightingFactor'] = self.weighting_factor
        return json

    def read_json(self, json: dict):
        super(NwFactor, self).read_json(json)
        val = json.get('impactCategory')
        if val is not None:
            self.impact_category = Ref()
            self.impact_category.read_json(val)
        val = json.get('normalisationFactor')
        if val is not None:
            self.normalisation_factor = val
        val = json.get('weightingFactor')
        if val is not None:
            self.weighting_factor = val

    @staticmethod
    def from_json(json: dict):
        instance = NwFactor()
        instance.read_json(json)
        return instance


@dataclass
class ParameterRedef(Entity):
    """
    A redefinition of a parameter in a product system.

    Attributes
    ----------
    context: Ref
        The context of the paramater (a process or LCIA method). If no context
        is provided it is assumed that this is a redefinition of a global
        parameter.

    description: str
        A description of this parameter redefinition.

    name: str
        The name of the redefined parameter. Note that parameter names are used
        in formulas so they need to follow specific syntax rules. A
        redefinition replaces a bound parameter in a specific context and thus
        has to exactly match the respective name.

    uncertainty: Uncertainty
        An uncertainty distribution for the redefined parameter value.

    value: float
        The value of the redefined parameter.

    """

    olca_type: str = 'ParameterRedef'
    context: Optional[Ref] = None
    description: Optional[str] = None
    name: Optional[str] = None
    uncertainty: Optional[Uncertainty] = None
    value: Optional[float] = None

    def to_json(self) -> dict:
        json: dict = super(ParameterRedef, self).to_json()
        if self.context is not None:
            json['context'] = self.context.to_json()
        if self.description is not None:
            json['description'] = self.description
        if self.name is not None:
            json['name'] = self.name
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty.to_json()
        if self.value is not None:
            json['value'] = self.value
        return json

    def read_json(self, json: dict):
        super(ParameterRedef, self).read_json(json)
        val = json.get('context')
        if val is not None:
            self.context = Ref()
            self.context.read_json(val)
        val = json.get('description')
        if val is not None:
            self.description = val
        val = json.get('name')
        if val is not None:
            self.name = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.read_json(val)
        val = json.get('value')
        if val is not None:
            self.value = val

    @staticmethod
    def from_json(json: dict):
        instance = ParameterRedef()
        instance.read_json(json)
        return instance


@dataclass
class ParameterRedefSet(Entity):
    """
    An instance of this class is just a set of parameter redefinitions attached
    to a product system. It can have a name and a description. One of the
    parameter sets can be defined as the baseline of the product system. In the
    calculation the baseline set is then taken by default.

    Attributes
    ----------
    name: str
        The name of the parameter set.

    description: str
        A description of the parameter set.

    is_baseline: bool
        Indicates if this set of parameter redefinitions is the baseline for a
        product system.

    parameters: List[ParameterRedef]
        The parameter redefinitions of this redefinition set.

    """

    olca_type: str = 'ParameterRedefSet'
    name: Optional[str] = None
    description: Optional[str] = None
    is_baseline: Optional[bool] = None
    parameters: Optional[List[ParameterRedef]] = None

    def to_json(self) -> dict:
        json: dict = super(ParameterRedefSet, self).to_json()
        if self.name is not None:
            json['name'] = self.name
        if self.description is not None:
            json['description'] = self.description
        if self.is_baseline is not None:
            json['isBaseline'] = self.is_baseline
        if self.parameters is not None:
            json['parameters'] = []
            for e in self.parameters:
                json['parameters'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(ParameterRedefSet, self).read_json(json)
        val = json.get('name')
        if val is not None:
            self.name = val
        val = json.get('description')
        if val is not None:
            self.description = val
        val = json.get('isBaseline')
        if val is not None:
            self.is_baseline = val
        val = json.get('parameters')
        if val is not None:
            self.parameters = []
            for d in val:
                e = ParameterRedef()
                e.read_json(d)
                self.parameters.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = ParameterRedefSet()
        instance.read_json(json)
        return instance


@dataclass
class ProcessDocumentation(Entity):
    """


    Attributes
    ----------
    time_description: str

    valid_until: str

    valid_from: str

    technology_description: str

    data_collection_description: str

    completeness_description: str

    data_selection_description: str

    review_details: str

    data_treatment_description: str

    inventory_method_description: str

    modeling_constants_description: str

    reviewer: Ref

    sampling_description: str

    sources: List[Ref]

    restrictions_description: str

    copyright: bool

    creation_date: str

    data_documentor: Ref

    data_generator: Ref

    data_set_owner: Ref

    intended_application: str

    project_description: str

    publication: Ref

    geography_description: str

    """

    olca_type: str = 'ProcessDocumentation'
    time_description: Optional[str] = None
    valid_until: Optional[str] = None
    valid_from: Optional[str] = None
    technology_description: Optional[str] = None
    data_collection_description: Optional[str] = None
    completeness_description: Optional[str] = None
    data_selection_description: Optional[str] = None
    review_details: Optional[str] = None
    data_treatment_description: Optional[str] = None
    inventory_method_description: Optional[str] = None
    modeling_constants_description: Optional[str] = None
    reviewer: Optional[Ref] = None
    sampling_description: Optional[str] = None
    sources: Optional[List[Ref]] = None
    restrictions_description: Optional[str] = None
    copyright: Optional[bool] = None
    creation_date: Optional[str] = None
    data_documentor: Optional[Ref] = None
    data_generator: Optional[Ref] = None
    data_set_owner: Optional[Ref] = None
    intended_application: Optional[str] = None
    project_description: Optional[str] = None
    publication: Optional[Ref] = None
    geography_description: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(ProcessDocumentation, self).to_json()
        if self.time_description is not None:
            json['timeDescription'] = self.time_description
        if self.valid_until is not None:
            json['validUntil'] = self.valid_until
        if self.valid_from is not None:
            json['validFrom'] = self.valid_from
        if self.technology_description is not None:
            json['technologyDescription'] = self.technology_description
        if self.data_collection_description is not None:
            json['dataCollectionDescription'] = self.data_collection_description
        if self.completeness_description is not None:
            json['completenessDescription'] = self.completeness_description
        if self.data_selection_description is not None:
            json['dataSelectionDescription'] = self.data_selection_description
        if self.review_details is not None:
            json['reviewDetails'] = self.review_details
        if self.data_treatment_description is not None:
            json['dataTreatmentDescription'] = self.data_treatment_description
        if self.inventory_method_description is not None:
            json['inventoryMethodDescription'] = self.inventory_method_description
        if self.modeling_constants_description is not None:
            json['modelingConstantsDescription'] = self.modeling_constants_description
        if self.reviewer is not None:
            json['reviewer'] = self.reviewer.to_json()
        if self.sampling_description is not None:
            json['samplingDescription'] = self.sampling_description
        if self.sources is not None:
            json['sources'] = []
            for e in self.sources:
                json['sources'].append(e.to_json())
        if self.restrictions_description is not None:
            json['restrictionsDescription'] = self.restrictions_description
        if self.copyright is not None:
            json['copyright'] = self.copyright
        if self.creation_date is not None:
            json['creationDate'] = self.creation_date
        if self.data_documentor is not None:
            json['dataDocumentor'] = self.data_documentor.to_json()
        if self.data_generator is not None:
            json['dataGenerator'] = self.data_generator.to_json()
        if self.data_set_owner is not None:
            json['dataSetOwner'] = self.data_set_owner.to_json()
        if self.intended_application is not None:
            json['intendedApplication'] = self.intended_application
        if self.project_description is not None:
            json['projectDescription'] = self.project_description
        if self.publication is not None:
            json['publication'] = self.publication.to_json()
        if self.geography_description is not None:
            json['geographyDescription'] = self.geography_description
        return json

    def read_json(self, json: dict):
        super(ProcessDocumentation, self).read_json(json)
        val = json.get('timeDescription')
        if val is not None:
            self.time_description = val
        val = json.get('validUntil')
        if val is not None:
            self.valid_until = val
        val = json.get('validFrom')
        if val is not None:
            self.valid_from = val
        val = json.get('technologyDescription')
        if val is not None:
            self.technology_description = val
        val = json.get('dataCollectionDescription')
        if val is not None:
            self.data_collection_description = val
        val = json.get('completenessDescription')
        if val is not None:
            self.completeness_description = val
        val = json.get('dataSelectionDescription')
        if val is not None:
            self.data_selection_description = val
        val = json.get('reviewDetails')
        if val is not None:
            self.review_details = val
        val = json.get('dataTreatmentDescription')
        if val is not None:
            self.data_treatment_description = val
        val = json.get('inventoryMethodDescription')
        if val is not None:
            self.inventory_method_description = val
        val = json.get('modelingConstantsDescription')
        if val is not None:
            self.modeling_constants_description = val
        val = json.get('reviewer')
        if val is not None:
            self.reviewer = Ref()
            self.reviewer.read_json(val)
        val = json.get('samplingDescription')
        if val is not None:
            self.sampling_description = val
        val = json.get('sources')
        if val is not None:
            self.sources = []
            for d in val:
                e = Ref()
                e.read_json(d)
                self.sources.append(e)
        val = json.get('restrictionsDescription')
        if val is not None:
            self.restrictions_description = val
        val = json.get('copyright')
        if val is not None:
            self.copyright = val
        val = json.get('creationDate')
        if val is not None:
            self.creation_date = val
        val = json.get('dataDocumentor')
        if val is not None:
            self.data_documentor = Ref()
            self.data_documentor.read_json(val)
        val = json.get('dataGenerator')
        if val is not None:
            self.data_generator = Ref()
            self.data_generator.read_json(val)
        val = json.get('dataSetOwner')
        if val is not None:
            self.data_set_owner = Ref()
            self.data_set_owner.read_json(val)
        val = json.get('intendedApplication')
        if val is not None:
            self.intended_application = val
        val = json.get('projectDescription')
        if val is not None:
            self.project_description = val
        val = json.get('publication')
        if val is not None:
            self.publication = Ref()
            self.publication.read_json(val)
        val = json.get('geographyDescription')
        if val is not None:
            self.geography_description = val

    @staticmethod
    def from_json(json: dict):
        instance = ProcessDocumentation()
        instance.read_json(json)
        return instance


@dataclass
class ProcessLink(Entity):
    """
    A process link is a connection between two processes in a product system.

    Attributes
    ----------
    provider: Ref
        The descriptor of the process or product system that provides a product
        or a waste treatment.

    flow: Ref
        The descriptor of the flow that is exchanged between the two processes.

    process: Ref
        The descriptor of the process that is linked to the provider.

    exchange: ExchangeRef
        The exchange of the linked process (this is useful if the linked
        process has multiple exchanges with the same flow that are linked to
        different provides, e.g. in an electricity mix).

    """

    olca_type: str = 'ProcessLink'
    provider: Optional[Ref] = None
    flow: Optional[Ref] = None
    process: Optional[Ref] = None
    exchange: Optional[ExchangeRef] = None

    def to_json(self) -> dict:
        json: dict = super(ProcessLink, self).to_json()
        if self.provider is not None:
            json['provider'] = self.provider.to_json()
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.process is not None:
            json['process'] = self.process.to_json()
        if self.exchange is not None:
            json['exchange'] = self.exchange.to_json()
        return json

    def read_json(self, json: dict):
        super(ProcessLink, self).read_json(json)
        val = json.get('provider')
        if val is not None:
            self.provider = Ref()
            self.provider.read_json(val)
        val = json.get('flow')
        if val is not None:
            self.flow = Ref()
            self.flow.read_json(val)
        val = json.get('process')
        if val is not None:
            self.process = Ref()
            self.process.read_json(val)
        val = json.get('exchange')
        if val is not None:
            self.exchange = ExchangeRef()
            self.exchange.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = ProcessLink()
        instance.read_json(json)
        return instance


@dataclass
class RootEntity(Entity):
    """
    A standalone item in a database like a location, unit group, flow, or
    process. A root entity can be unambiguously identified by its id (the
    JSON-LD @id field), version, and lastChange fields.

    Attributes
    ----------
    name: str
        The name of the entity.

    description: str
        The description of the entity.

    version: str
        A version number in MAJOR.MINOR.PATCH format where the MINOR and PATCH
        fields are optional and the fields may have leading zeros (so 01.00.00
        is the same as 1.0.0 or 1).

    last_change: str
        The timestamp when the entity was changed the last time.

    """

    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    last_change: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(RootEntity, self).to_json()
        if self.name is not None:
            json['name'] = self.name
        if self.description is not None:
            json['description'] = self.description
        if self.version is not None:
            json['version'] = self.version
        if self.last_change is not None:
            json['lastChange'] = self.last_change
        return json

    def read_json(self, json: dict):
        super(RootEntity, self).read_json(json)
        val = json.get('name')
        if val is not None:
            self.name = val
        val = json.get('description')
        if val is not None:
            self.description = val
        val = json.get('version')
        if val is not None:
            self.version = val
        val = json.get('lastChange')
        if val is not None:
            self.last_change = val

    @staticmethod
    def from_json(json: dict):
        instance = RootEntity()
        instance.read_json(json)
        return instance


@dataclass
class SimpleResult(Entity):
    """


    Attributes
    ----------
    flow_results: List[FlowResult]

    impact_results: List[ImpactResult]

    """

    olca_type: str = 'SimpleResult'
    flow_results: Optional[List[FlowResult]] = None
    impact_results: Optional[List[ImpactResult]] = None

    def to_json(self) -> dict:
        json: dict = super(SimpleResult, self).to_json()
        if self.flow_results is not None:
            json['flowResults'] = []
            for e in self.flow_results:
                json['flowResults'].append(e.to_json())
        if self.impact_results is not None:
            json['impactResults'] = []
            for e in self.impact_results:
                json['impactResults'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(SimpleResult, self).read_json(json)
        val = json.get('flowResults')
        if val is not None:
            self.flow_results = []
            for d in val:
                e = FlowResult()
                e.read_json(d)
                self.flow_results.append(e)
        val = json.get('impactResults')
        if val is not None:
            self.impact_results = []
            for d in val:
                e = ImpactResult()
                e.read_json(d)
                self.impact_results.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = SimpleResult()
        instance.read_json(json)
        return instance


@dataclass
class SocialAspect(Entity):
    """
    An instance of this class describes a social aspect related to a social
    indicator in a process.

    Attributes
    ----------
    activity_value: float
        The value of the activity variable of the related indicator.

    comment: str

    quality: str
        A data quality entry, e.g. `(3,1,2,4,1)`.

    raw_amount: str
        The raw amount of the indicator's unit of measurement (not required to
        be numeric currently)

    risk_level: RiskLevel

    social_indicator: Ref

    source: Ref

    """

    olca_type: str = 'SocialAspect'
    activity_value: Optional[float] = None
    comment: Optional[str] = None
    quality: Optional[str] = None
    raw_amount: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    social_indicator: Optional[Ref] = None
    source: Optional[Ref] = None

    def to_json(self) -> dict:
        json: dict = super(SocialAspect, self).to_json()
        if self.activity_value is not None:
            json['activityValue'] = self.activity_value
        if self.comment is not None:
            json['comment'] = self.comment
        if self.quality is not None:
            json['quality'] = self.quality
        if self.raw_amount is not None:
            json['rawAmount'] = self.raw_amount
        if self.risk_level is not None:
            json['riskLevel'] = self.risk_level.value
        if self.social_indicator is not None:
            json['socialIndicator'] = self.social_indicator.to_json()
        if self.source is not None:
            json['source'] = self.source.to_json()
        return json

    def read_json(self, json: dict):
        super(SocialAspect, self).read_json(json)
        val = json.get('activityValue')
        if val is not None:
            self.activity_value = val
        val = json.get('comment')
        if val is not None:
            self.comment = val
        val = json.get('quality')
        if val is not None:
            self.quality = val
        val = json.get('rawAmount')
        if val is not None:
            self.raw_amount = val
        val = json.get('riskLevel')
        if val is not None:
            self.risk_level = RiskLevel(val)
        val = json.get('socialIndicator')
        if val is not None:
            self.social_indicator = Ref()
            self.social_indicator.read_json(val)
        val = json.get('source')
        if val is not None:
            self.source = Ref()
            self.source.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = SocialAspect()
        instance.read_json(json)
        return instance


@dataclass
class Uncertainty(Entity):
    """
    Defines the parameter values of an uncertainty distribution. Depending on
    the uncertainty distribution type different parameters could be used.

    Attributes
    ----------
    distribution_type: UncertaintyType
        The uncertainty distribution type

    mean: float
        The arithmetic mean (used for normal distributions).

    mean_formula: str
        A mathematical formula for the arithmetic mean.

    geom_mean: float
        The geometric mean value (used for log-normal distributions).

    geom_mean_formula: str
        A mathematical formula for the geometric mean.

    minimum: float
        The minimum value (used for uniform and triangle distributions).

    minimum_formula: str
        A mathematical formula for the minimum value.

    sd: float
        The arithmetic standard deviation (used for normal distributions).

    sd_formula: str
        A mathematical formula for the arithmetic standard deviation.

    geom_sd: float
        The geometric standard deviation (used for log-normal distributions).

    geom_sd_formula: str
        A mathematical formula for the geometric standard deviation.

    mode: float
        The most likely value (used for triangle distributions).

    mode_formula: str
        A mathematical formula for the most likely value.

    maximum: float
        The maximum value (used for uniform and triangle distributions).

    maximum_formula: str
        A mathematical formula for the maximum value.

    """

    olca_type: str = 'Uncertainty'
    distribution_type: Optional[UncertaintyType] = None
    mean: Optional[float] = None
    mean_formula: Optional[str] = None
    geom_mean: Optional[float] = None
    geom_mean_formula: Optional[str] = None
    minimum: Optional[float] = None
    minimum_formula: Optional[str] = None
    sd: Optional[float] = None
    sd_formula: Optional[str] = None
    geom_sd: Optional[float] = None
    geom_sd_formula: Optional[str] = None
    mode: Optional[float] = None
    mode_formula: Optional[str] = None
    maximum: Optional[float] = None
    maximum_formula: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(Uncertainty, self).to_json()
        if self.distribution_type is not None:
            json['distributionType'] = self.distribution_type.value
        if self.mean is not None:
            json['mean'] = self.mean
        if self.mean_formula is not None:
            json['meanFormula'] = self.mean_formula
        if self.geom_mean is not None:
            json['geomMean'] = self.geom_mean
        if self.geom_mean_formula is not None:
            json['geomMeanFormula'] = self.geom_mean_formula
        if self.minimum is not None:
            json['minimum'] = self.minimum
        if self.minimum_formula is not None:
            json['minimumFormula'] = self.minimum_formula
        if self.sd is not None:
            json['sd'] = self.sd
        if self.sd_formula is not None:
            json['sdFormula'] = self.sd_formula
        if self.geom_sd is not None:
            json['geomSd'] = self.geom_sd
        if self.geom_sd_formula is not None:
            json['geomSdFormula'] = self.geom_sd_formula
        if self.mode is not None:
            json['mode'] = self.mode
        if self.mode_formula is not None:
            json['modeFormula'] = self.mode_formula
        if self.maximum is not None:
            json['maximum'] = self.maximum
        if self.maximum_formula is not None:
            json['maximumFormula'] = self.maximum_formula
        return json

    def read_json(self, json: dict):
        super(Uncertainty, self).read_json(json)
        val = json.get('distributionType')
        if val is not None:
            self.distribution_type = UncertaintyType(val)
        val = json.get('mean')
        if val is not None:
            self.mean = val
        val = json.get('meanFormula')
        if val is not None:
            self.mean_formula = val
        val = json.get('geomMean')
        if val is not None:
            self.geom_mean = val
        val = json.get('geomMeanFormula')
        if val is not None:
            self.geom_mean_formula = val
        val = json.get('minimum')
        if val is not None:
            self.minimum = val
        val = json.get('minimumFormula')
        if val is not None:
            self.minimum_formula = val
        val = json.get('sd')
        if val is not None:
            self.sd = val
        val = json.get('sdFormula')
        if val is not None:
            self.sd_formula = val
        val = json.get('geomSd')
        if val is not None:
            self.geom_sd = val
        val = json.get('geomSdFormula')
        if val is not None:
            self.geom_sd_formula = val
        val = json.get('mode')
        if val is not None:
            self.mode = val
        val = json.get('modeFormula')
        if val is not None:
            self.mode_formula = val
        val = json.get('maximum')
        if val is not None:
            self.maximum = val
        val = json.get('maximumFormula')
        if val is not None:
            self.maximum_formula = val

    @staticmethod
    def from_json(json: dict):
        instance = Uncertainty()
        instance.read_json(json)
        return instance


@dataclass
class CategorizedEntity(RootEntity):
    """
    A root entity which can have a category.

    Attributes
    ----------
    category: Ref
        The category of the entity.

    tags: List[str]
        A list of optional tags. A tag is just a string which should not
        contain commas (and other special characters).

    library: str
        If this entity is part of a library, this field contains the identifier
        of that library. The identifier is typically just the combination of
        the library name and version.

    """

    category: Optional[Ref] = None
    tags: Optional[List[str]] = None
    library: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(CategorizedEntity, self).to_json()
        if self.category is not None:
            json['category'] = self.category.to_json()
        if self.tags is not None:
            json['tags'] = []
            for e in self.tags:
                json['tags'].append(e)
        if self.library is not None:
            json['library'] = self.library
        return json

    def read_json(self, json: dict):
        super(CategorizedEntity, self).read_json(json)
        val = json.get('category')
        if val is not None:
            self.category = Ref()
            self.category.read_json(val)
        val = json.get('tags')
        if val is not None:
            self.tags = []
            for d in val:
                e = d
                self.tags.append(e)
        val = json.get('library')
        if val is not None:
            self.library = val

    @staticmethod
    def from_json(json: dict):
        instance = CategorizedEntity()
        instance.read_json(json)
        return instance


@dataclass
class FlowMap(RootEntity):
    """
    A crosswalk of flows from a source flow list to a target flow list.

    Attributes
    ----------
    source: Ref
        The reference (id, name, description) of the source flow list.

    target: Ref
        The reference (id, name, description) of the target flow list.

    mappings: List[FlowMapEntry]
        A list of flow mappings from flows in a source flow list to flows in a
        target flow list.

    """

    olca_type: str = 'FlowMap'
    source: Optional[Ref] = None
    target: Optional[Ref] = None
    mappings: Optional[List[FlowMapEntry]] = None

    def to_json(self) -> dict:
        json: dict = super(FlowMap, self).to_json()
        if self.source is not None:
            json['source'] = self.source.to_json()
        if self.target is not None:
            json['target'] = self.target.to_json()
        if self.mappings is not None:
            json['mappings'] = []
            for e in self.mappings:
                json['mappings'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(FlowMap, self).read_json(json)
        val = json.get('source')
        if val is not None:
            self.source = Ref()
            self.source.read_json(val)
        val = json.get('target')
        if val is not None:
            self.target = Ref()
            self.target.read_json(val)
        val = json.get('mappings')
        if val is not None:
            self.mappings = []
            for d in val:
                e = FlowMapEntry()
                e.read_json(d)
                self.mappings.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = FlowMap()
        instance.read_json(json)
        return instance


@dataclass
class NwSet(RootEntity):
    """
    A normalization and weighting set.

    Attributes
    ----------
    weighted_score_unit: str
        This is the optional unit of the (normalized and) weighted score when
        this normalization and weighting set was applied on a LCIA result.

    factors: List[NwFactor]
        The list of normalization and weighting factors of this set.

    """

    olca_type: str = 'NwSet'
    weighted_score_unit: Optional[str] = None
    factors: Optional[List[NwFactor]] = None

    def to_json(self) -> dict:
        json: dict = super(NwSet, self).to_json()
        if self.weighted_score_unit is not None:
            json['weightedScoreUnit'] = self.weighted_score_unit
        if self.factors is not None:
            json['factors'] = []
            for e in self.factors:
                json['factors'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(NwSet, self).read_json(json)
        val = json.get('weightedScoreUnit')
        if val is not None:
            self.weighted_score_unit = val
        val = json.get('factors')
        if val is not None:
            self.factors = []
            for d in val:
                e = NwFactor()
                e.read_json(d)
                self.factors.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = NwSet()
        instance.read_json(json)
        return instance


@dataclass
class Ref(RootEntity):
    """
    A Ref is a reference to a [RootEntity]. When serializing an entity (e.g. a
    [Process]) that references another standalone entity (e.g. a [Flow] in an
    [Exchange]) we do not want to write the complete referenced entity into the
    serialized JSON object but just a reference. However, the reference
    contains some meta-data like name, category path etc. that are useful to
    display.

    Attributes
    ----------
    category_path: List[str]
        The full path of the category of the referenced entity from top to
        bottom, e.g. `"Elementary flows", "Emissions to air", "unspecified"`.

    library: str
        If the entity that is described by this reference is part of a library,
        this field contains the identifier of that library. The identifier is
        typically just the combination of the library name and version.

    ref_unit: str
        This field is only valid for references of flows or impact categories
        and contains the name (symbol) of the reference unit of that respective
        flow or impact category.

    location: str
        This field is only valid for references of processes or flows and
        contains the location name or code of that respective process or flow.

    flow_type: FlowType
        In case of a reference to a flow, this field can contain the type of
        flow that is referenced.

    process_type: ProcessType
        In case of a reference to a process, this fiel can contain the type of
        process that is referenced.

    """

    olca_type: str = 'Ref'
    category_path: Optional[List[str]] = None
    library: Optional[str] = None
    ref_unit: Optional[str] = None
    location: Optional[str] = None
    flow_type: Optional[FlowType] = None
    process_type: Optional[ProcessType] = None

    def to_json(self) -> dict:
        json: dict = super(Ref, self).to_json()
        if self.category_path is not None:
            json['categoryPath'] = []
            for e in self.category_path:
                json['categoryPath'].append(e)
        if self.library is not None:
            json['library'] = self.library
        if self.ref_unit is not None:
            json['refUnit'] = self.ref_unit
        if self.location is not None:
            json['location'] = self.location
        if self.flow_type is not None:
            json['flowType'] = self.flow_type.value
        if self.process_type is not None:
            json['processType'] = self.process_type.value
        return json

    def read_json(self, json: dict):
        super(Ref, self).read_json(json)
        val = json.get('categoryPath')
        if val is not None:
            self.category_path = []
            for d in val:
                e = d
                self.category_path.append(e)
        val = json.get('library')
        if val is not None:
            self.library = val
        val = json.get('refUnit')
        if val is not None:
            self.ref_unit = val
        val = json.get('location')
        if val is not None:
            self.location = val
        val = json.get('flowType')
        if val is not None:
            self.flow_type = FlowType(val)
        val = json.get('processType')
        if val is not None:
            self.process_type = ProcessType(val)

    @staticmethod
    def from_json(json: dict):
        instance = Ref()
        instance.read_json(json)
        return instance


@dataclass
class Unit(RootEntity):
    """
    An unit of measure

    Attributes
    ----------
    conversion_factor: float
        The conversion factor to the reference unit of the unit group to which
        this unit belongs.

    reference_unit: bool
        Indicates whether the unit is the reference unit of the unit group to
        which this unit belongs. If it is the reference unit the conversion
        factor must be 1.0. There should be always only one reference unit in a
        unit group. The reference unit is used to convert amounts given in one
        unit to amounts given in another unit of the respective unit group.

    synonyms: List[str]
        A list of synonyms for the unit.

    """

    olca_type: str = 'Unit'
    conversion_factor: Optional[float] = None
    reference_unit: Optional[bool] = None
    synonyms: Optional[List[str]] = None

    def to_json(self) -> dict:
        json: dict = super(Unit, self).to_json()
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        if self.reference_unit is not None:
            json['referenceUnit'] = self.reference_unit
        if self.synonyms is not None:
            json['synonyms'] = []
            for e in self.synonyms:
                json['synonyms'].append(e)
        return json

    def read_json(self, json: dict):
        super(Unit, self).read_json(json)
        val = json.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val
        val = json.get('referenceUnit')
        if val is not None:
            self.reference_unit = val
        val = json.get('synonyms')
        if val is not None:
            self.synonyms = []
            for d in val:
                e = d
                self.synonyms.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = Unit()
        instance.read_json(json)
        return instance


@dataclass
class Actor(CategorizedEntity):
    """
    An actor is a person or organisation.

    Attributes
    ----------
    address: str

    city: str

    country: str

    email: str

    telefax: str

    telephone: str

    website: str

    zip_code: str

    """

    olca_type: str = 'Actor'
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    telefax: Optional[str] = None
    telephone: Optional[str] = None
    website: Optional[str] = None
    zip_code: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(Actor, self).to_json()
        if self.address is not None:
            json['address'] = self.address
        if self.city is not None:
            json['city'] = self.city
        if self.country is not None:
            json['country'] = self.country
        if self.email is not None:
            json['email'] = self.email
        if self.telefax is not None:
            json['telefax'] = self.telefax
        if self.telephone is not None:
            json['telephone'] = self.telephone
        if self.website is not None:
            json['website'] = self.website
        if self.zip_code is not None:
            json['zipCode'] = self.zip_code
        return json

    def read_json(self, json: dict):
        super(Actor, self).read_json(json)
        val = json.get('address')
        if val is not None:
            self.address = val
        val = json.get('city')
        if val is not None:
            self.city = val
        val = json.get('country')
        if val is not None:
            self.country = val
        val = json.get('email')
        if val is not None:
            self.email = val
        val = json.get('telefax')
        if val is not None:
            self.telefax = val
        val = json.get('telephone')
        if val is not None:
            self.telephone = val
        val = json.get('website')
        if val is not None:
            self.website = val
        val = json.get('zipCode')
        if val is not None:
            self.zip_code = val

    @staticmethod
    def from_json(json: dict):
        instance = Actor()
        instance.read_json(json)
        return instance


@dataclass
class Category(CategorizedEntity):
    """
    A category is used for the categorisation of types like processes, flows,
    etc. The tricky thing is that the `Category` class inherits also from the
    [CategorizedEntity] type so that a category can have a category attribute
    which is then the parent category of this category (uff).

    Attributes
    ----------
    model_type: ModelType
        The type of models that can be linked to the category.

    """

    olca_type: str = 'Category'
    model_type: Optional[ModelType] = None

    def to_json(self) -> dict:
        json: dict = super(Category, self).to_json()
        if self.model_type is not None:
            json['modelType'] = self.model_type.value
        return json

    def read_json(self, json: dict):
        super(Category, self).read_json(json)
        val = json.get('modelType')
        if val is not None:
            self.model_type = ModelType(val)

    @staticmethod
    def from_json(json: dict):
        instance = Category()
        instance.read_json(json)
        return instance


@dataclass
class Currency(CategorizedEntity):
    """


    Attributes
    ----------
    code: str

    conversion_factor: float

    reference_currency: Ref

    """

    olca_type: str = 'Currency'
    code: Optional[str] = None
    conversion_factor: Optional[float] = None
    reference_currency: Optional[Ref] = None

    def to_json(self) -> dict:
        json: dict = super(Currency, self).to_json()
        if self.code is not None:
            json['code'] = self.code
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        if self.reference_currency is not None:
            json['referenceCurrency'] = self.reference_currency.to_json()
        return json

    def read_json(self, json: dict):
        super(Currency, self).read_json(json)
        val = json.get('code')
        if val is not None:
            self.code = val
        val = json.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val
        val = json.get('referenceCurrency')
        if val is not None:
            self.reference_currency = Ref()
            self.reference_currency.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = Currency()
        instance.read_json(json)
        return instance


@dataclass
class DQSystem(CategorizedEntity):
    """
    A data quality system (DQS) in openLCA describes a pedigree matrix of $m$
    data quality indicators (DQIs) and $n$ data quality scores (DQ scores).
    Such a system can then be used to assess the data quality of processes and
    exchanges by tagging them with an instance of the system $D$ where $D$ is a
    $m * n$ matrix with an entry $d_{ij}$ containing the value of the data
    quality score $j$ for indicator $i$. As each indicator in $D$ can only have
    a single score value, $D$ can be stored in a vector $d$ where $d_i$
    contains the data quality score for indicator $i$. The possible values of
    the data quality scores are defined as a linear order $1 \dots n$. In
    openLCA, the data quality entry $d$ of a process or exchange is stored as a
    string like `(3;2;4;n.a.;2)` which means the data quality score for the
    first indicator is `3`, for the second `2` etc. A specific value is `n.a.`
    which stands for _not applicable_. In calculations, these data quality
    entries can be aggregated in different ways. For example, the data quality
    entry of a flow $f$ with a contribution of `0.5 kg` and a data quality
    entry of `(3;2;4;n.a.;2)` in a process $p$ and a contribution of `1.5 kg`
    and a data quality entry of `(2;3;1;n.a.;5)` in a process $q$ could be
    aggregated to `(2;3;2;n.a.;4)` by applying an weighted average and
    rounding. Finally, custom labels like `A, B, C, ...` or `Very good, Good,
    Fair, ...` for the DQ scores can be assigned by the user. These labels are
    then displayed instead of `1, 2, 3 ...` in the user interface or result
    exports. However, internally the numeric values are used in the data model
    and calculations.

    Attributes
    ----------
    has_uncertainties: bool

    source: Ref

    indicators: List[DQIndicator]

    """

    olca_type: str = 'DQSystem'
    has_uncertainties: Optional[bool] = None
    source: Optional[Ref] = None
    indicators: Optional[List[DQIndicator]] = None

    def to_json(self) -> dict:
        json: dict = super(DQSystem, self).to_json()
        if self.has_uncertainties is not None:
            json['hasUncertainties'] = self.has_uncertainties
        if self.source is not None:
            json['source'] = self.source.to_json()
        if self.indicators is not None:
            json['indicators'] = []
            for e in self.indicators:
                json['indicators'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(DQSystem, self).read_json(json)
        val = json.get('hasUncertainties')
        if val is not None:
            self.has_uncertainties = val
        val = json.get('source')
        if val is not None:
            self.source = Ref()
            self.source.read_json(val)
        val = json.get('indicators')
        if val is not None:
            self.indicators = []
            for d in val:
                e = DQIndicator()
                e.read_json(d)
                self.indicators.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = DQSystem()
        instance.read_json(json)
        return instance


@dataclass
class Flow(CategorizedEntity):
    """
    Everything that can be an input or output of a process (e.g. a substance, a
    product, a waste, a service etc.)

    Attributes
    ----------
    flow_type: FlowType
        The type of the flow. Note that this type is more a descriptor of how
        the flow is handled in calculations.

    cas: str
        A CAS number of the flow.

    formula: str
        A chemical formula of the flow.

    flow_properties: List[FlowPropertyFactor]
        The flow properties (quantities) in which amounts of the flow can be
        expressed together with conversion factors between these flow flow
        properties.

    location: Ref
        The location of the flow. Normally the location of a flow is defined by
        the process location where the flow is an input or output. However,
        some data formats define a location as a property of a flow.

    synonyms: str
        A list of synonyms but packed into a single field. Best is to use
        semicolons as separator as commas are sometimes used in names of
        chemicals.

    infrastructure_flow: bool
        Indicates whether this flow describes an infrastructure product. This
        field is part of the openLCA schema because of backward compatibility
        with EcoSpold 1. It does not really have a meaning in openLCA and
        should not be used anymore.

    """

    olca_type: str = 'Flow'
    flow_type: Optional[FlowType] = None
    cas: Optional[str] = None
    formula: Optional[str] = None
    flow_properties: Optional[List[FlowPropertyFactor]] = None
    location: Optional[Ref] = None
    synonyms: Optional[str] = None
    infrastructure_flow: Optional[bool] = None

    def to_json(self) -> dict:
        json: dict = super(Flow, self).to_json()
        if self.flow_type is not None:
            json['flowType'] = self.flow_type.value
        if self.cas is not None:
            json['cas'] = self.cas
        if self.formula is not None:
            json['formula'] = self.formula
        if self.flow_properties is not None:
            json['flowProperties'] = []
            for e in self.flow_properties:
                json['flowProperties'].append(e.to_json())
        if self.location is not None:
            json['location'] = self.location.to_json()
        if self.synonyms is not None:
            json['synonyms'] = self.synonyms
        if self.infrastructure_flow is not None:
            json['infrastructureFlow'] = self.infrastructure_flow
        return json

    def read_json(self, json: dict):
        super(Flow, self).read_json(json)
        val = json.get('flowType')
        if val is not None:
            self.flow_type = FlowType(val)
        val = json.get('cas')
        if val is not None:
            self.cas = val
        val = json.get('formula')
        if val is not None:
            self.formula = val
        val = json.get('flowProperties')
        if val is not None:
            self.flow_properties = []
            for d in val:
                e = FlowPropertyFactor()
                e.read_json(d)
                self.flow_properties.append(e)
        val = json.get('location')
        if val is not None:
            self.location = Ref()
            self.location.read_json(val)
        val = json.get('synonyms')
        if val is not None:
            self.synonyms = val
        val = json.get('infrastructureFlow')
        if val is not None:
            self.infrastructure_flow = val

    @staticmethod
    def from_json(json: dict):
        instance = Flow()
        instance.read_json(json)
        return instance


@dataclass
class FlowProperty(CategorizedEntity):
    """
    A flow property is a quantity that can be used to express amounts of a
    flow.

    Attributes
    ----------
    flow_property_type: FlowPropertyType
        The type of the flow property

    unit_group: Ref
        The units of measure that can be used to express quantities of the flow
        property.

    """

    olca_type: str = 'FlowProperty'
    flow_property_type: Optional[FlowPropertyType] = None
    unit_group: Optional[Ref] = None

    def to_json(self) -> dict:
        json: dict = super(FlowProperty, self).to_json()
        if self.flow_property_type is not None:
            json['flowPropertyType'] = self.flow_property_type.value
        if self.unit_group is not None:
            json['unitGroup'] = self.unit_group.to_json()
        return json

    def read_json(self, json: dict):
        super(FlowProperty, self).read_json(json)
        val = json.get('flowPropertyType')
        if val is not None:
            self.flow_property_type = FlowPropertyType(val)
        val = json.get('unitGroup')
        if val is not None:
            self.unit_group = Ref()
            self.unit_group.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = FlowProperty()
        instance.read_json(json)
        return instance


@dataclass
class ImpactCategory(CategorizedEntity):
    """


    Attributes
    ----------
    reference_unit_name: str
        The name of the reference unit of the LCIA category (e.g. kg CO2-eq.).

    parameters: List[Parameter]
        A set of parameters which can be used in formulas of the
        characterisation factors in this impact category.

    impact_factors: List[ImpactFactor]
        The characterisation factors of the LCIA category.

    """

    olca_type: str = 'ImpactCategory'
    reference_unit_name: Optional[str] = None
    parameters: Optional[List[Parameter]] = None
    impact_factors: Optional[List[ImpactFactor]] = None

    def to_json(self) -> dict:
        json: dict = super(ImpactCategory, self).to_json()
        if self.reference_unit_name is not None:
            json['referenceUnitName'] = self.reference_unit_name
        if self.parameters is not None:
            json['parameters'] = []
            for e in self.parameters:
                json['parameters'].append(e.to_json())
        if self.impact_factors is not None:
            json['impactFactors'] = []
            for e in self.impact_factors:
                json['impactFactors'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(ImpactCategory, self).read_json(json)
        val = json.get('referenceUnitName')
        if val is not None:
            self.reference_unit_name = val
        val = json.get('parameters')
        if val is not None:
            self.parameters = []
            for d in val:
                e = Parameter()
                e.read_json(d)
                self.parameters.append(e)
        val = json.get('impactFactors')
        if val is not None:
            self.impact_factors = []
            for d in val:
                e = ImpactFactor()
                e.read_json(d)
                self.impact_factors.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = ImpactCategory()
        instance.read_json(json)
        return instance


@dataclass
class ImpactMethod(CategorizedEntity):
    """
    An impact assessment method.

    Attributes
    ----------
    impact_categories: List[Ref]
        The impact categories of the method.

    nw_sets: List[NwSet]
        The normalization and weighting sets of the method.

    """

    olca_type: str = 'ImpactMethod'
    impact_categories: Optional[List[Ref]] = None
    nw_sets: Optional[List[NwSet]] = None

    def to_json(self) -> dict:
        json: dict = super(ImpactMethod, self).to_json()
        if self.impact_categories is not None:
            json['impactCategories'] = []
            for e in self.impact_categories:
                json['impactCategories'].append(e.to_json())
        if self.nw_sets is not None:
            json['nwSets'] = []
            for e in self.nw_sets:
                json['nwSets'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(ImpactMethod, self).read_json(json)
        val = json.get('impactCategories')
        if val is not None:
            self.impact_categories = []
            for d in val:
                e = Ref()
                e.read_json(d)
                self.impact_categories.append(e)
        val = json.get('nwSets')
        if val is not None:
            self.nw_sets = []
            for d in val:
                e = NwSet()
                e.read_json(d)
                self.nw_sets.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = ImpactMethod()
        instance.read_json(json)
        return instance


@dataclass
class Location(CategorizedEntity):
    """
    A location like a country, state, city, etc.

    Attributes
    ----------
    code: str
        The code of the location (e.g. an ISO 2-letter country code).

    latitude: float
        The average latitude of the location.

    longitude: float
        The average longitude of the location.

    geometry: dict
        A GeoJSON object.

    """

    olca_type: str = 'Location'
    code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geometry: Optional[dict] = None

    def to_json(self) -> dict:
        json: dict = super(Location, self).to_json()
        if self.code is not None:
            json['code'] = self.code
        if self.latitude is not None:
            json['latitude'] = self.latitude
        if self.longitude is not None:
            json['longitude'] = self.longitude
        if self.geometry is not None:
            json['geometry'] = self.geometry
        return json

    def read_json(self, json: dict):
        super(Location, self).read_json(json)
        val = json.get('code')
        if val is not None:
            self.code = val
        val = json.get('latitude')
        if val is not None:
            self.latitude = val
        val = json.get('longitude')
        if val is not None:
            self.longitude = val
        val = json.get('geometry')
        if val is not None:
            self.geometry = val

    @staticmethod
    def from_json(json: dict):
        instance = Location()
        instance.read_json(json)
        return instance


@dataclass
class Parameter(CategorizedEntity):
    """
    In openLCA, parameters can be defined in different scopes: global, process,
    or LCIA method. The parameter name can be used in formulas and, thus, need
    to conform to a specific syntax. Within a scope the parameter name should
    be unique (otherwise the evaluation is not deterministic). There are two
    types of parameters in openLCA: input parameters and dependent parameters.
    An input parameter can have an optional uncertainty distribution but not a
    formula. A dependent parameter can (should) have a formula (where also
    other parameters can be used) but no uncertainty distribution.

    Attributes
    ----------
    parameter_scope: ParameterScope
        The scope where the parameter is valid.

    input_parameter: bool
        Indicates whether the parameter is an input parameter (true) or a
        dependent/calculated parameter (false). A parameter can have a formula
        if it is not an input parameter.

    value: float
        The parameter value.

    formula: str
        A mathematical expression to calculate the parameter value.

    uncertainty: Uncertainty
        An uncertainty distribution of the parameter value. This is only valid
        for input parameters.

    """

    olca_type: str = 'Parameter'
    parameter_scope: Optional[ParameterScope] = None
    input_parameter: Optional[bool] = None
    value: Optional[float] = None
    formula: Optional[str] = None
    uncertainty: Optional[Uncertainty] = None

    def to_json(self) -> dict:
        json: dict = super(Parameter, self).to_json()
        if self.parameter_scope is not None:
            json['parameterScope'] = self.parameter_scope.value
        if self.input_parameter is not None:
            json['inputParameter'] = self.input_parameter
        if self.value is not None:
            json['value'] = self.value
        if self.formula is not None:
            json['formula'] = self.formula
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty.to_json()
        return json

    def read_json(self, json: dict):
        super(Parameter, self).read_json(json)
        val = json.get('parameterScope')
        if val is not None:
            self.parameter_scope = ParameterScope(val)
        val = json.get('inputParameter')
        if val is not None:
            self.input_parameter = val
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('formula')
        if val is not None:
            self.formula = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = Parameter()
        instance.read_json(json)
        return instance


@dataclass
class Process(CategorizedEntity):
    """


    Attributes
    ----------
    allocation_factors: List[AllocationFactor]

    default_allocation_method: AllocationType

    exchanges: List[Exchange]
        The inputs and outputs of the process.

    last_internal_id: int
        This field holds the last internal ID that was used in an exchange
        (which may have been deleted, so it can be larger than the largest
        internal ID of the exchanges of the process.) The internal ID of an
        exchange is used to identify exchanges within a process (for updates,
        data exchanges (see process links), etc.). When you add an exchange to
        a process, you should increment this field in the process and set the
        resulting value as the internal ID of that exchange. The sequence of
        internal IDs should start with `1`.

    location: Ref
        The location of the process.

    parameters: List[Parameter]

    process_documentation: ProcessDocumentation

    process_type: ProcessType

    dq_system: Ref
        A reference to a data quality system ([DQSystem]) with which the
        overall quality of the process can be assessed.

    exchange_dq_system: Ref
        A reference to a data quality system ([DQSystem]) with which the
        quality of individual inputs and outputs ([Exchange]s) of the process
        can be assessed.

    social_dq_system: Ref
        A reference to a data quality system ([DQSystem]) with which the
        quality of individual social aspects of the process can be assessed.

    dq_entry: str
        A data quality entry like `(1;3;2;5;1)`. The entry is a vector of data
        quality values that need to match the overall data quality system of
        the process (the system that is stored in the `dqSystem` property). In
        such a system the data quality indicators have fixed positions and the
        respective values in the `dqEntry` vector map to these positions.

    infrastructure_process: bool
        Indicates whether this process describes an infrastructure process.
        This field is part of the openLCA schema because of backward
        compatibility with EcoSpold 1. It does not really have a meaning in
        openLCA and should not be used anymore.

    social_aspects: List[SocialAspect]
        A set of social aspects related to this process.

    """

    olca_type: str = 'Process'
    allocation_factors: Optional[List[AllocationFactor]] = None
    default_allocation_method: Optional[AllocationType] = None
    exchanges: Optional[List[Exchange]] = None
    last_internal_id: Optional[int] = None
    location: Optional[Ref] = None
    parameters: Optional[List[Parameter]] = None
    process_documentation: Optional[ProcessDocumentation] = None
    process_type: Optional[ProcessType] = None
    dq_system: Optional[Ref] = None
    exchange_dq_system: Optional[Ref] = None
    social_dq_system: Optional[Ref] = None
    dq_entry: Optional[str] = None
    infrastructure_process: Optional[bool] = None
    social_aspects: Optional[List[SocialAspect]] = None

    def to_json(self) -> dict:
        json: dict = super(Process, self).to_json()
        if self.allocation_factors is not None:
            json['allocationFactors'] = []
            for e in self.allocation_factors:
                json['allocationFactors'].append(e.to_json())
        if self.default_allocation_method is not None:
            json['defaultAllocationMethod'] = self.default_allocation_method.value
        if self.exchanges is not None:
            json['exchanges'] = []
            for e in self.exchanges:
                json['exchanges'].append(e.to_json())
        if self.last_internal_id is not None:
            json['lastInternalId'] = self.last_internal_id
        if self.location is not None:
            json['location'] = self.location.to_json()
        if self.parameters is not None:
            json['parameters'] = []
            for e in self.parameters:
                json['parameters'].append(e.to_json())
        if self.process_documentation is not None:
            json['processDocumentation'] = self.process_documentation.to_json()
        if self.process_type is not None:
            json['processType'] = self.process_type.value
        if self.dq_system is not None:
            json['dqSystem'] = self.dq_system.to_json()
        if self.exchange_dq_system is not None:
            json['exchangeDqSystem'] = self.exchange_dq_system.to_json()
        if self.social_dq_system is not None:
            json['socialDqSystem'] = self.social_dq_system.to_json()
        if self.dq_entry is not None:
            json['dqEntry'] = self.dq_entry
        if self.infrastructure_process is not None:
            json['infrastructureProcess'] = self.infrastructure_process
        if self.social_aspects is not None:
            json['socialAspects'] = []
            for e in self.social_aspects:
                json['socialAspects'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(Process, self).read_json(json)
        val = json.get('allocationFactors')
        if val is not None:
            self.allocation_factors = []
            for d in val:
                e = AllocationFactor()
                e.read_json(d)
                self.allocation_factors.append(e)
        val = json.get('defaultAllocationMethod')
        if val is not None:
            self.default_allocation_method = AllocationType(val)
        val = json.get('exchanges')
        if val is not None:
            self.exchanges = []
            for d in val:
                e = Exchange()
                e.read_json(d)
                self.exchanges.append(e)
        val = json.get('lastInternalId')
        if val is not None:
            self.last_internal_id = val
        val = json.get('location')
        if val is not None:
            self.location = Ref()
            self.location.read_json(val)
        val = json.get('parameters')
        if val is not None:
            self.parameters = []
            for d in val:
                e = Parameter()
                e.read_json(d)
                self.parameters.append(e)
        val = json.get('processDocumentation')
        if val is not None:
            self.process_documentation = ProcessDocumentation()
            self.process_documentation.read_json(val)
        val = json.get('processType')
        if val is not None:
            self.process_type = ProcessType(val)
        val = json.get('dqSystem')
        if val is not None:
            self.dq_system = Ref()
            self.dq_system.read_json(val)
        val = json.get('exchangeDqSystem')
        if val is not None:
            self.exchange_dq_system = Ref()
            self.exchange_dq_system.read_json(val)
        val = json.get('socialDqSystem')
        if val is not None:
            self.social_dq_system = Ref()
            self.social_dq_system.read_json(val)
        val = json.get('dqEntry')
        if val is not None:
            self.dq_entry = val
        val = json.get('infrastructureProcess')
        if val is not None:
            self.infrastructure_process = val
        val = json.get('socialAspects')
        if val is not None:
            self.social_aspects = []
            for d in val:
                e = SocialAspect()
                e.read_json(d)
                self.social_aspects.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = Process()
        instance.read_json(json)
        return instance


@dataclass
class ProductSystem(CategorizedEntity):
    """
    A product system describes the supply chain of a product (the functional
    unit) ...

    Attributes
    ----------
    processes: List[Ref]
        The descriptors of all processes and sub-systems that are contained in
        the product system.

    reference_process: Ref
        The descriptor of the process that provides the flow of the functional
        unit of the product system.

    reference_exchange: ExchangeRef
        The exchange of the reference processes (typically the product output)
        that provides the flow of the functional unit of the product system.

    target_amount: float
        The flow amount of the functional unit of the product system.

    target_unit: Ref
        The unit in which the flow amount of the functional unit is given.

    target_flow_property: Ref
        The flow property in which the flow amount of the functional unit is
        given.

    process_links: List[ProcessLink]
        The process links of the product system.

    parameter_sets: List[ParameterRedefSet]
        A list of possible sets of parameter redefinitions for this product
        system.

    """

    olca_type: str = 'ProductSystem'
    processes: Optional[List[Ref]] = None
    reference_process: Optional[Ref] = None
    reference_exchange: Optional[ExchangeRef] = None
    target_amount: Optional[float] = None
    target_unit: Optional[Ref] = None
    target_flow_property: Optional[Ref] = None
    process_links: Optional[List[ProcessLink]] = None
    parameter_sets: Optional[List[ParameterRedefSet]] = None

    def to_json(self) -> dict:
        json: dict = super(ProductSystem, self).to_json()
        if self.processes is not None:
            json['processes'] = []
            for e in self.processes:
                json['processes'].append(e.to_json())
        if self.reference_process is not None:
            json['referenceProcess'] = self.reference_process.to_json()
        if self.reference_exchange is not None:
            json['referenceExchange'] = self.reference_exchange.to_json()
        if self.target_amount is not None:
            json['targetAmount'] = self.target_amount
        if self.target_unit is not None:
            json['targetUnit'] = self.target_unit.to_json()
        if self.target_flow_property is not None:
            json['targetFlowProperty'] = self.target_flow_property.to_json()
        if self.process_links is not None:
            json['processLinks'] = []
            for e in self.process_links:
                json['processLinks'].append(e.to_json())
        if self.parameter_sets is not None:
            json['parameterSets'] = []
            for e in self.parameter_sets:
                json['parameterSets'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(ProductSystem, self).read_json(json)
        val = json.get('processes')
        if val is not None:
            self.processes = []
            for d in val:
                e = Ref()
                e.read_json(d)
                self.processes.append(e)
        val = json.get('referenceProcess')
        if val is not None:
            self.reference_process = Ref()
            self.reference_process.read_json(val)
        val = json.get('referenceExchange')
        if val is not None:
            self.reference_exchange = ExchangeRef()
            self.reference_exchange.read_json(val)
        val = json.get('targetAmount')
        if val is not None:
            self.target_amount = val
        val = json.get('targetUnit')
        if val is not None:
            self.target_unit = Ref()
            self.target_unit.read_json(val)
        val = json.get('targetFlowProperty')
        if val is not None:
            self.target_flow_property = Ref()
            self.target_flow_property.read_json(val)
        val = json.get('processLinks')
        if val is not None:
            self.process_links = []
            for d in val:
                e = ProcessLink()
                e.read_json(d)
                self.process_links.append(e)
        val = json.get('parameterSets')
        if val is not None:
            self.parameter_sets = []
            for d in val:
                e = ParameterRedefSet()
                e.read_json(d)
                self.parameter_sets.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = ProductSystem()
        instance.read_json(json)
        return instance


@dataclass
class Project(CategorizedEntity):
    """


    Attributes
    ----------
    impact_method: Ref

    nw_set: NwSet

    """

    olca_type: str = 'Project'
    impact_method: Optional[Ref] = None
    nw_set: Optional[NwSet] = None

    def to_json(self) -> dict:
        json: dict = super(Project, self).to_json()
        if self.impact_method is not None:
            json['impactMethod'] = self.impact_method.to_json()
        if self.nw_set is not None:
            json['nwSet'] = self.nw_set.to_json()
        return json

    def read_json(self, json: dict):
        super(Project, self).read_json(json)
        val = json.get('impactMethod')
        if val is not None:
            self.impact_method = Ref()
            self.impact_method.read_json(val)
        val = json.get('nwSet')
        if val is not None:
            self.nw_set = NwSet()
            self.nw_set.read_json(val)

    @staticmethod
    def from_json(json: dict):
        instance = Project()
        instance.read_json(json)
        return instance


@dataclass
class SocialIndicator(CategorizedEntity):
    """


    Attributes
    ----------
    activity_variable: str
        The name of the activity variable of the indicator.

    activity_quantity: Ref
        The quantity of the activity variable.

    activity_unit: Ref
        The unit of the activity variable.

    unit_of_measurement: str
        The unit in which the indicator is measured.

    evaluation_scheme: str
        Documentation of the evaluation scheme of the indicator.

    """

    olca_type: str = 'SocialIndicator'
    activity_variable: Optional[str] = None
    activity_quantity: Optional[Ref] = None
    activity_unit: Optional[Ref] = None
    unit_of_measurement: Optional[str] = None
    evaluation_scheme: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(SocialIndicator, self).to_json()
        if self.activity_variable is not None:
            json['activityVariable'] = self.activity_variable
        if self.activity_quantity is not None:
            json['activityQuantity'] = self.activity_quantity.to_json()
        if self.activity_unit is not None:
            json['activityUnit'] = self.activity_unit.to_json()
        if self.unit_of_measurement is not None:
            json['unitOfMeasurement'] = self.unit_of_measurement
        if self.evaluation_scheme is not None:
            json['evaluationScheme'] = self.evaluation_scheme
        return json

    def read_json(self, json: dict):
        super(SocialIndicator, self).read_json(json)
        val = json.get('activityVariable')
        if val is not None:
            self.activity_variable = val
        val = json.get('activityQuantity')
        if val is not None:
            self.activity_quantity = Ref()
            self.activity_quantity.read_json(val)
        val = json.get('activityUnit')
        if val is not None:
            self.activity_unit = Ref()
            self.activity_unit.read_json(val)
        val = json.get('unitOfMeasurement')
        if val is not None:
            self.unit_of_measurement = val
        val = json.get('evaluationScheme')
        if val is not None:
            self.evaluation_scheme = val

    @staticmethod
    def from_json(json: dict):
        instance = SocialIndicator()
        instance.read_json(json)
        return instance


@dataclass
class Source(CategorizedEntity):
    """
    A source is a literature reference.

    Attributes
    ----------
    url: str
        A URL that points to the source.

    text_reference: str
        The full text reference of the source.

    year: int
        The publication year of the source.

    external_file: str
        A direct link (relative or absolute URL) to the source file.

    """

    olca_type: str = 'Source'
    url: Optional[str] = None
    text_reference: Optional[str] = None
    year: Optional[int] = None
    external_file: Optional[str] = None

    def to_json(self) -> dict:
        json: dict = super(Source, self).to_json()
        if self.url is not None:
            json['url'] = self.url
        if self.text_reference is not None:
            json['textReference'] = self.text_reference
        if self.year is not None:
            json['year'] = self.year
        if self.external_file is not None:
            json['externalFile'] = self.external_file
        return json

    def read_json(self, json: dict):
        super(Source, self).read_json(json)
        val = json.get('url')
        if val is not None:
            self.url = val
        val = json.get('textReference')
        if val is not None:
            self.text_reference = val
        val = json.get('year')
        if val is not None:
            self.year = val
        val = json.get('externalFile')
        if val is not None:
            self.external_file = val

    @staticmethod
    def from_json(json: dict):
        instance = Source()
        instance.read_json(json)
        return instance


@dataclass
class UnitGroup(CategorizedEntity):
    """
    A group of units that can be converted into each other.

    Attributes
    ----------
    default_flow_property: Ref
        Some LCA data formats do not have the concept of flow properties or
        quantities. This field provides a default link to a flow property for
        units that are contained in this group.

    units: List[Unit]
        The units of the unit group.

    """

    olca_type: str = 'UnitGroup'
    default_flow_property: Optional[Ref] = None
    units: Optional[List[Unit]] = None

    def to_json(self) -> dict:
        json: dict = super(UnitGroup, self).to_json()
        if self.default_flow_property is not None:
            json['defaultFlowProperty'] = self.default_flow_property.to_json()
        if self.units is not None:
            json['units'] = []
            for e in self.units:
                json['units'].append(e.to_json())
        return json

    def read_json(self, json: dict):
        super(UnitGroup, self).read_json(json)
        val = json.get('defaultFlowProperty')
        if val is not None:
            self.default_flow_property = Ref()
            self.default_flow_property.read_json(val)
        val = json.get('units')
        if val is not None:
            self.units = []
            for d in val:
                e = Unit()
                e.read_json(d)
                self.units.append(e)

    @staticmethod
    def from_json(json: dict):
        instance = UnitGroup()
        instance.read_json(json)
        return instance

