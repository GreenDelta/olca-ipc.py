# This module contains a Python API of the JSON-LD based
# openLCA data exchange model.package schema.
# For more information see http://greendelta.github.io/olca-schema/

from enum import Enum
from typing import List


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
    """An enumeration of the different calculation methods supported by openLCA."""

    SIMPLE_CALCULATION = 'SIMPLE_CALCULATION'
    CONTRIBUTION_ANALYSIS = 'CONTRIBUTION_ANALYSIS'
    UPSTREAM_ANALYSIS = 'UPSTREAM_ANALYSIS'
    REGIONALIZED_CALCULATION = 'REGIONALIZED_CALCULATION'
    MONTE_CARLO_SIMULATION = 'MONTE_CARLO_SIMULATION'


class FlowPropertyType(Enum):
    """An enumeration of flow property types."""

    ECONOMIC_QUANTITY = 'ECONOMIC_QUANTITY'
    PHYSICAL_QUANTITY = 'PHYSICAL_QUANTITY'


class FlowType(Enum):
    """The basic flow types."""

    ELEMENTARY_FLOW = 'ELEMENTARY_FLOW'
    PRODUCT_FLOW = 'PRODUCT_FLOW'
    WASTE_FLOW = 'WASTE_FLOW'


class ModelType(Enum):
    """An enumeration of the root entity types."""

    PROJECT = 'PROJECT'
    IMPACT_METHOD = 'IMPACT_METHOD'
    IMPACT_CATEGORY = 'IMPACT_CATEGORY'
    PRODUCT_SYSTEM = 'PRODUCT_SYSTEM'
    PROCESS = 'PROCESS'
    FLOW = 'FLOW'
    FLOW_PROPERTY = 'FLOW_PROPERTY'
    UNIT_GROUP = 'UNIT_GROUP'
    UNIT = 'UNIT'
    ACTOR = 'ACTOR'
    SOURCE = 'SOURCE'
    CATEGORY = 'CATEGORY'
    LOCATION = 'LOCATION'
    NW_SET = 'NW_SET'
    SOCIAL_INDICATOR = 'SOCIAL_INDICATOR'


class ParameterScope(Enum):
    """The possible scopes of parameters."""

    PROCESS_SCOPE = 'PROCESS_SCOPE'
    LCIA_METHOD_SCOPE = 'LCIA_METHOD_SCOPE'
    GLOBAL_SCOPE = 'GLOBAL_SCOPE'


class ProcessType(Enum):
    LCI_RESULT = 'LCI_RESULT'
    UNIT_PROCESS = 'UNIT_PROCESS'


class UncertaintyType(Enum):
    """
    Enumeration of uncertainty distribution types that can be used in 
    exchanges, parameters, LCIA factors, etc. 
    """

    LOG_NORMAL_DISTRIBUTION = 'LOG_NORMAL_DISTRIBUTION'
    NORMAL_DISTRIBUTION = 'NORMAL_DISTRIBUTION'
    TRIANGLE_DISTRIBUTION = 'TRIANGLE_DISTRIBUTION'
    UNIFORM_DISTRIBUTION = 'UNIFORM_DISTRIBUTION'


class Entity(object):
    """The most generic type of the openLCA data model."""

    def __init__(self):
        self.id = None  # type: str
        self.olca_type = None  # type: str

    def to_json(self) -> dict:
        o_type = self.olca_type
        if o_type is None:
            o_type = type(self).__name__
        json = {'@type': o_type}
        if self.id is not None:
            json['@id'] = self.id
        return json

    def from_json(self, json: dict):
        self.id = json.get('@id')


class AllocationFactor(Entity):
    """A single allocation factor in a process.

    Attributes
    ----------
    product_exchange: Exchange
        The output product.

    allocation_type: AllocationType
        The type of allocation.

    value: float
        The value of the allocation factor.

    allocated_exchange: Exchange
        An input product or elementary flow exchange which is allocated by this
        factor. This is only valid for causal allocation where allocation
        factors can be assigned to single exchanges.


    """

    def __init__(self):
        super(AllocationFactor, self).__init__()
        self.product_exchange = None  # type: Exchange
        self.allocation_type = None  # type: AllocationType
        self.value = None  # type: float
        self.allocated_exchange = None  # type: Exchange

    def to_json(self) -> dict:
        json = super(AllocationFactor, self).to_json()  # type: dict
        if self.product_exchange is not None:
            json['productExchange'] = self.product_exchange.to_json()
        if self.allocation_type is not None:
            json['allocationType'] = self.allocation_type.value
        if self.value is not None:
            json['value'] = self.value
        if self.allocated_exchange is not None:
            json['allocatedExchange'] = self.allocated_exchange.to_json()
        return json

    def from_json(self, json: dict):
        super(AllocationFactor, self).from_json(json)
        val = json.get('productExchange')
        if val is not None:
            self.product_exchange = Exchange()
            self.product_exchange.from_json(val)
        val = json.get('allocationType')
        if val is not None:
            self.allocation_type = AllocationType(val)
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('allocatedExchange')
        if val is not None:
            self.allocated_exchange = Exchange()
            self.allocated_exchange.from_json(val)


class CalculationSetup(Entity):
    """A setup for a product system calculation.

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

    def __init__(self):
        super(CalculationSetup, self).__init__()
        self.calculation_type = None  # type: CalculationType
        self.product_system = None  # type: Ref
        self.impact_method = None  # type: Ref
        self.with_costs = None  # type: bool
        self.nw_set = None  # type: Ref
        self.allocation_method = None  # type: AllocationType
        self.parameter_redefs = None  # type: List[ParameterRedef]
        self.amount = None  # type: float
        self.unit = None  # type: Ref
        self.flow_property = None  # type: Ref

    def to_json(self) -> dict:
        json = super(CalculationSetup, self).to_json()  # type: dict
        if self.calculation_type is not None:
            json['calculationType'] = self.calculation_type.value
        if self.product_system is not None:
            json['productSystem'] = self.product_system.to_json()
        if self.impact_method is not None:
            json['impactMethod'] = self.impact_method.to_json()
        if self.with_costs is not None:
            json['withCosts'] = self.with_costs
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

    def from_json(self, json: dict):
        super(CalculationSetup, self).from_json(json)
        val = json.get('calculationType')
        if val is not None:
            self.calculation_type = CalculationType(val)
        val = json.get('productSystem')
        if val is not None:
            self.product_system = Ref()
            self.product_system.from_json(val)
        val = json.get('impactMethod')
        if val is not None:
            self.impact_method = Ref()
            self.impact_method.from_json(val)
        val = json.get('withCosts')
        if val is not None:
            self.with_costs = val
        val = json.get('nwSet')
        if val is not None:
            self.nw_set = Ref()
            self.nw_set.from_json(val)
        val = json.get('allocationMethod')
        if val is not None:
            self.allocation_method = AllocationType(val)
        val = json.get('parameterRedefs')
        if val is not None:
            self.parameter_redefs = []
            for d in val:
                e = ParameterRedef()
                e.from_json(d)
                self.parameter_redefs.append(e)
        val = json.get('amount')
        if val is not None:
            self.amount = val
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.from_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.from_json(val)


class DqIndicator(Entity):
    """An indicator of a data quality system ([DqSystem])."""

    def __init__(self):
        super(DqIndicator, self).__init__()
        self.name = None  # type: str
        self.position = None  # type: int
        self.scores = None  # type: List[DqScore]

    def to_json(self) -> dict:
        json = super(DqIndicator, self).to_json()  # type: dict
        if self.name is not None:
            json['name'] = self.name
        if self.position is not None:
            json['position'] = self.position
        if self.scores is not None:
            json['scores'] = []
            for e in self.scores:
                json['scores'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(DqIndicator, self).from_json(json)
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
                e = DqScore()
                e.from_json(d)
                self.scores.append(e)


class DqScore(Entity):
    """
    An score value of an indicator ([DqIndicator]) in a data quality system 
    ([DqSystem]). 
    """

    def __init__(self):
        super(DqScore, self).__init__()
        self.position = None  # type: int
        self.label = None  # type: str
        self.description = None  # type: str
        self.uncertainty = None  # type: float

    def to_json(self) -> dict:
        json = super(DqScore, self).to_json()  # type: dict
        if self.position is not None:
            json['position'] = self.position
        if self.label is not None:
            json['label'] = self.label
        if self.description is not None:
            json['description'] = self.description
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty
        return json

    def from_json(self, json: dict):
        super(DqScore, self).from_json(json)
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


class Exchange(Entity):
    """
    An Exchange is an input or output of a [Flow] in a [Process]. The amount of 
    an exchange is given in a specific unit of a quantity ([FlowProperty]) of 
    the flow. The allowed units and flow properties that can be used for a flow 
    in an exchange are defined by the flow property information in that flow 
    (see also the [FlowPropertyFactor] type). 

    Attributes
    ----------
    internal_id: int
        The process internal ID of the exchange. This is used to identify
        exchanges unambiguously within a process (e.g. when linking exchanges
        in a product system where multiple exchanges with the same flow are
        allowed). The value should be >= 1.

    avoided_product: bool
        Indicates whether this exchange is an avoided product.

    flow: FlowRef
        The reference to the flow of the exchange.

    flow_property: Ref
        The quantity in which the amount is given.

    input: bool


    quantitative_reference: bool
        Indicates whether the exchange is the quantitative reference of the
        process.

    base_uncertainty: float


    default_provider: ProcessRef
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

    def __init__(self):
        super(Exchange, self).__init__()
        self.internal_id = None  # type: int
        self.avoided_product = None  # type: bool
        self.flow = None  # type: FlowRef
        self.flow_property = None  # type: Ref
        self.input = None  # type: bool
        self.quantitative_reference = None  # type: bool
        self.base_uncertainty = None  # type: float
        self.default_provider = None  # type: ProcessRef
        self.amount = None  # type: float
        self.amount_formula = None  # type: str
        self.unit = None  # type: Ref
        self.dq_entry = None  # type: str
        self.uncertainty = None  # type: Uncertainty
        self.description = None  # type: str

    def to_json(self) -> dict:
        json = super(Exchange, self).to_json()  # type: dict
        if self.internal_id is not None:
            json['internalId'] = self.internal_id
        if self.avoided_product is not None:
            json['avoidedProduct'] = self.avoided_product
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

    def from_json(self, json: dict):
        super(Exchange, self).from_json(json)
        val = json.get('internalId')
        if val is not None:
            self.internal_id = val
        val = json.get('avoidedProduct')
        if val is not None:
            self.avoided_product = val
        val = json.get('flow')
        if val is not None:
            self.flow = FlowRef()
            self.flow.from_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.from_json(val)
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
            self.default_provider = ProcessRef()
            self.default_provider.from_json(val)
        val = json.get('amount')
        if val is not None:
            self.amount = val
        val = json.get('amountFormula')
        if val is not None:
            self.amount_formula = val
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.from_json(val)
        val = json.get('dqEntry')
        if val is not None:
            self.dq_entry = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)
        val = json.get('description')
        if val is not None:
            self.description = val


class FlowMapRef(Entity):
    """
    Describes a the source or target flow of a flow mapping in a `FlowMap`. 
    Such a flow reference can also optionally specify the unit and flow 
    property (quantity) for which the mapping is valid. If the unit and 
    quantity are not given, the mapping is based on the reference unit of the 
    reference flow property of the respective flow. 

    Attributes
    ----------
    flow: FlowRef
        The reference to the flow data set.

    flow_property: Ref
        An optional reference to a flow property of the flow for which the
        mapping is valid.

    unit: Ref
        An optional reference to a unit of the flow for which the mapping is
        valid


    """

    def __init__(self):
        super(FlowMapRef, self).__init__()
        self.flow = None  # type: FlowRef
        self.flow_property = None  # type: Ref
        self.unit = None  # type: Ref

    def to_json(self) -> dict:
        json = super(FlowMapRef, self).to_json()  # type: dict
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        if self.unit is not None:
            json['unit'] = self.unit.to_json()
        return json

    def from_json(self, json: dict):
        super(FlowMapRef, self).from_json(json)
        val = json.get('flow')
        if val is not None:
            self.flow = FlowRef()
            self.flow.from_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.from_json(val)
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.from_json(val)


class FlowPropertyFactor(Entity):
    """
    A FlowPropertyFactor is a conversion factor between flow properties 
    (quantities) of a flow. As an example the amount of the flow 'water' in a 
    process could be expressed in 'kg' mass or 'm3' volume. In this case the 
    flow water would have two flow property factors: one for the flow property 
    'mass' and one for 'volume'. Each of these flow properties has a reference 
    to a unit group which again has a reference unit. In the example the flow 
    property 'mass' could reference the unit group 'units of mass' with 'kg' as 
    reference unit and volume could reference the unit group 'units of volume' 
    with 'm3' as reference unit. The flow property factor is now the conversion 
    factor between these two reference units where the factor of the reference 
    flow property of the flow is 1. If the reference flow property of 'water' 
    in the example would be 'mass' the respective flow property factor would be 
    1 and the factor for 'volume' would be 0.001 (as 1 kg water is 0.001 m3). 
    The amount of water in a process can now be also given in liter, tons, 
    grams etc. For this, the unit conversion factor of the respective unit 
    group can be used to convert into the reference unit (which then can be 
    used to convert to the reference unit of another flow property). Another 
    thing to note is that different flow properties can refer to the same unit 
    group (e.g. MJ upper calorific value and MJ lower calorific value.) 

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

    def __init__(self):
        super(FlowPropertyFactor, self).__init__()
        self.flow_property = None  # type: Ref
        self.conversion_factor = None  # type: float
        self.reference_flow_property = None  # type: bool

    def to_json(self) -> dict:
        json = super(FlowPropertyFactor, self).to_json()  # type: dict
        if self.flow_property is not None:
            json['flowProperty'] = self.flow_property.to_json()
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        if self.reference_flow_property is not None:
            json['referenceFlowProperty'] = self.reference_flow_property
        return json

    def from_json(self, json: dict):
        super(FlowPropertyFactor, self).from_json(json)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.from_json(val)
        val = json.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val
        val = json.get('referenceFlowProperty')
        if val is not None:
            self.reference_flow_property = val


class FlowResult(Entity):
    """A result value for a flow; given in the reference unit of the flow.


    Attributes
    ----------
    flow: FlowRef
        The flow reference.

    input: bool
        Indicates whether the flow is an input or not.

    value: float
        The value of the flow amount.


    """

    def __init__(self):
        super(FlowResult, self).__init__()
        self.flow = None  # type: FlowRef
        self.input = None  # type: bool
        self.value = None  # type: float

    def to_json(self) -> dict:
        json = super(FlowResult, self).to_json()  # type: dict
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.input is not None:
            json['input'] = self.input
        if self.value is not None:
            json['value'] = self.value
        return json

    def from_json(self, json: dict):
        super(FlowResult, self).from_json(json)
        val = json.get('flow')
        if val is not None:
            self.flow = FlowRef()
            self.flow.from_json(val)
        val = json.get('input')
        if val is not None:
            self.input = val
        val = json.get('value')
        if val is not None:
            self.value = val


class ImpactFactor(Entity):
    """A single characterisation factor of a LCIA category for a flow.

    Attributes
    ----------
    flow: FlowRef
        The [Flow] of the impact assessment factor.

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

    def __init__(self):
        super(ImpactFactor, self).__init__()
        self.flow = None  # type: FlowRef
        self.flow_property = None  # type: Ref
        self.unit = None  # type: Ref
        self.value = None  # type: float
        self.formula = None  # type: str
        self.uncertainty = None  # type: Uncertainty

    def to_json(self) -> dict:
        json = super(ImpactFactor, self).to_json()  # type: dict
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
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

    def from_json(self, json: dict):
        super(ImpactFactor, self).from_json(json)
        val = json.get('flow')
        if val is not None:
            self.flow = FlowRef()
            self.flow.from_json(val)
        val = json.get('flowProperty')
        if val is not None:
            self.flow_property = Ref()
            self.flow_property.from_json(val)
        val = json.get('unit')
        if val is not None:
            self.unit = Ref()
            self.unit.from_json(val)
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('formula')
        if val is not None:
            self.formula = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)


class ImpactResult(Entity):
    """A result value for an impact assessment category.


    Attributes
    ----------
    impact_category: ImpactCategoryRef
        The reference to the impact assessment category.

    value: float
        The value of the flow amount.


    """

    def __init__(self):
        super(ImpactResult, self).__init__()
        self.impact_category = None  # type: ImpactCategoryRef
        self.value = None  # type: float

    def to_json(self) -> dict:
        json = super(ImpactResult, self).to_json()  # type: dict
        if self.impact_category is not None:
            json['impactCategory'] = self.impact_category.to_json()
        if self.value is not None:
            json['value'] = self.value
        return json

    def from_json(self, json: dict):
        super(ImpactResult, self).from_json(json)
        val = json.get('impactCategory')
        if val is not None:
            self.impact_category = ImpactCategoryRef()
            self.impact_category.from_json(val)
        val = json.get('value')
        if val is not None:
            self.value = val


class Parameter(Entity):

    def __init__(self):
        super(Parameter, self).__init__()
        self.name = None  # type: str
        self.description = None  # type: str
        self.parameter_scope = None  # type: ParameterScope
        self.input_parameter = None  # type: bool
        self.value = None  # type: float
        self.formula = None  # type: str
        self.external_source = None  # type: str
        self.source_type = None  # type: str
        self.uncertainty = None  # type: Uncertainty

    def to_json(self) -> dict:
        json = super(Parameter, self).to_json()  # type: dict
        if self.name is not None:
            json['name'] = self.name
        if self.description is not None:
            json['description'] = self.description
        if self.parameter_scope is not None:
            json['parameterScope'] = self.parameter_scope.value
        if self.input_parameter is not None:
            json['inputParameter'] = self.input_parameter
        if self.value is not None:
            json['value'] = self.value
        if self.formula is not None:
            json['formula'] = self.formula
        if self.external_source is not None:
            json['externalSource'] = self.external_source
        if self.source_type is not None:
            json['sourceType'] = self.source_type
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty.to_json()
        return json

    def from_json(self, json: dict):
        super(Parameter, self).from_json(json)
        val = json.get('name')
        if val is not None:
            self.name = val
        val = json.get('description')
        if val is not None:
            self.description = val
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
        val = json.get('externalSource')
        if val is not None:
            self.external_source = val
        val = json.get('sourceType')
        if val is not None:
            self.source_type = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)


class ParameterRedef(Entity):
    """A redefinition of a parameter in a product system.

    Attributes
    ----------
    name: str
        The parameter name.

    value: float
        The (new) value of the parameter.

    context: Ref
        The context of the paramater (a process or LCIA method). If no context
        is provided it is assumed that this is a redefinition of a global
        parameter.


    """

    def __init__(self):
        super(ParameterRedef, self).__init__()
        self.name = None  # type: str
        self.value = None  # type: float
        self.context = None  # type: Ref

    def to_json(self) -> dict:
        json = super(ParameterRedef, self).to_json()  # type: dict
        if self.name is not None:
            json['name'] = self.name
        if self.value is not None:
            json['value'] = self.value
        if self.context is not None:
            json['context'] = self.context.to_json()
        return json

    def from_json(self, json: dict):
        super(ParameterRedef, self).from_json(json)
        val = json.get('name')
        if val is not None:
            self.name = val
        val = json.get('value')
        if val is not None:
            self.value = val
        val = json.get('context')
        if val is not None:
            self.context = Ref()
            self.context.from_json(val)


class ProcessDocumentation(Entity):

    def __init__(self):
        super(ProcessDocumentation, self).__init__()
        self.time_description = None  # type: str
        self.valid_until = None  # type: str
        self.valid_from = None  # type: str
        self.technology_description = None  # type: str
        self.data_collection_description = None  # type: str
        self.completeness_description = None  # type: str
        self.data_selection_description = None  # type: str
        self.review_details = None  # type: str
        self.data_treatment_description = None  # type: str
        self.inventory_method_description = None  # type: str
        self.modeling_constants_description = None  # type: str
        self.reviewer = None  # type: Ref
        self.sampling_description = None  # type: str
        self.sources = None  # type: List[Ref]
        self.restrictions_description = None  # type: str
        self.copyright = None  # type: bool
        self.creation_date = None  # type: str
        self.data_documentor = None  # type: Ref
        self.data_generator = None  # type: Ref
        self.data_set_owner = None  # type: Ref
        self.intended_application = None  # type: str
        self.project_description = None  # type: str
        self.publication = None  # type: Ref
        self.geography_description = None  # type: str

    def to_json(self) -> dict:
        json = super(ProcessDocumentation, self).to_json()  # type: dict
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

    def from_json(self, json: dict):
        super(ProcessDocumentation, self).from_json(json)
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
            self.reviewer.from_json(val)
        val = json.get('samplingDescription')
        if val is not None:
            self.sampling_description = val
        val = json.get('sources')
        if val is not None:
            self.sources = []
            for d in val:
                e = Ref()
                e.from_json(d)
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
            self.data_documentor.from_json(val)
        val = json.get('dataGenerator')
        if val is not None:
            self.data_generator = Ref()
            self.data_generator.from_json(val)
        val = json.get('dataSetOwner')
        if val is not None:
            self.data_set_owner = Ref()
            self.data_set_owner.from_json(val)
        val = json.get('intendedApplication')
        if val is not None:
            self.intended_application = val
        val = json.get('projectDescription')
        if val is not None:
            self.project_description = val
        val = json.get('publication')
        if val is not None:
            self.publication = Ref()
            self.publication.from_json(val)
        val = json.get('geographyDescription')
        if val is not None:
            self.geography_description = val


class ProcessLink(Entity):
    """A process link is a connection between two processes in a product system.

    Attributes
    ----------
    provider: Ref
        The descriptor of the process that provides a product or a waste
        treatment.

    flow: Ref
        The descriptor of the flow that is exchanged between the two processes.

    process: Ref
        The descriptor of the process that is linked to the provider.

    exchange: Exchange
        The exchange of the linked process (this is useful if the linked
        process has multiple exchanges with the same flow that are linked to
        different provides, e.g. in an electricity mix).


    """

    def __init__(self):
        super(ProcessLink, self).__init__()
        self.provider = None  # type: Ref
        self.flow = None  # type: Ref
        self.process = None  # type: Ref
        self.exchange = None  # type: Exchange

    def to_json(self) -> dict:
        json = super(ProcessLink, self).to_json()  # type: dict
        if self.provider is not None:
            json['provider'] = self.provider.to_json()
        if self.flow is not None:
            json['flow'] = self.flow.to_json()
        if self.process is not None:
            json['process'] = self.process.to_json()
        if self.exchange is not None:
            json['exchange'] = self.exchange.to_json()
        return json

    def from_json(self, json: dict):
        super(ProcessLink, self).from_json(json)
        val = json.get('provider')
        if val is not None:
            self.provider = Ref()
            self.provider.from_json(val)
        val = json.get('flow')
        if val is not None:
            self.flow = Ref()
            self.flow.from_json(val)
        val = json.get('process')
        if val is not None:
            self.process = Ref()
            self.process.from_json(val)
        val = json.get('exchange')
        if val is not None:
            self.exchange = Exchange()
            self.exchange.from_json(val)


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

    def __init__(self):
        super(RootEntity, self).__init__()
        self.name = None  # type: str
        self.description = None  # type: str
        self.version = None  # type: str
        self.last_change = None  # type: str

    def to_json(self) -> dict:
        json = super(RootEntity, self).to_json()  # type: dict
        if self.name is not None:
            json['name'] = self.name
        if self.description is not None:
            json['description'] = self.description
        if self.version is not None:
            json['version'] = self.version
        if self.last_change is not None:
            json['lastChange'] = self.last_change
        return json

    def from_json(self, json: dict):
        super(RootEntity, self).from_json(json)
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


class SimpleResult(Entity):

    def __init__(self):
        super(SimpleResult, self).__init__()
        self.flow_results = None  # type: List[FlowResult]
        self.impact_results = None  # type: List[ImpactResult]

    def to_json(self) -> dict:
        json = super(SimpleResult, self).to_json()  # type: dict
        if self.flow_results is not None:
            json['flowResults'] = []
            for e in self.flow_results:
                json['flowResults'].append(e.to_json())
        if self.impact_results is not None:
            json['impactResults'] = []
            for e in self.impact_results:
                json['impactResults'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(SimpleResult, self).from_json(json)
        val = json.get('flowResults')
        if val is not None:
            self.flow_results = []
            for d in val:
                e = FlowResult()
                e.from_json(d)
                self.flow_results.append(e)
        val = json.get('impactResults')
        if val is not None:
            self.impact_results = []
            for d in val:
                e = ImpactResult()
                e.from_json(d)
                self.impact_results.append(e)


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

    def __init__(self):
        super(Uncertainty, self).__init__()
        self.distribution_type = None  # type: UncertaintyType
        self.mean = None  # type: float
        self.mean_formula = None  # type: str
        self.geom_mean = None  # type: float
        self.geom_mean_formula = None  # type: str
        self.minimum = None  # type: float
        self.minimum_formula = None  # type: str
        self.sd = None  # type: float
        self.sd_formula = None  # type: str
        self.geom_sd = None  # type: float
        self.geom_sd_formula = None  # type: str
        self.mode = None  # type: float
        self.mode_formula = None  # type: str
        self.maximum = None  # type: float
        self.maximum_formula = None  # type: str

    def to_json(self) -> dict:
        json = super(Uncertainty, self).to_json()  # type: dict
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

    def from_json(self, json: dict):
        super(Uncertainty, self).from_json(json)
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


class CategorizedEntity(RootEntity):
    """A root entity which can have a category.

    Attributes
    ----------
    category: Ref
        The category of the entity.


    """

    def __init__(self):
        super(CategorizedEntity, self).__init__()
        self.category = None  # type: Ref

    def to_json(self) -> dict:
        json = super(CategorizedEntity, self).to_json()  # type: dict
        if self.category is not None:
            json['category'] = self.category.to_json()
        return json

    def from_json(self, json: dict):
        super(CategorizedEntity, self).from_json(json)
        val = json.get('category')
        if val is not None:
            self.category = Ref()
            self.category.from_json(val)


class FlowMap(RootEntity):
    """A crosswalk of flows from a source flow list to a target flow list.

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

    def __init__(self):
        super(FlowMap, self).__init__()
        self.source = None  # type: Ref
        self.target = None  # type: Ref
        self.mappings = None  # type: List[FlowMapEntry]

    def to_json(self) -> dict:
        json = super(FlowMap, self).to_json()  # type: dict
        if self.source is not None:
            json['source'] = self.source.to_json()
        if self.target is not None:
            json['target'] = self.target.to_json()
        if self.mappings is not None:
            json['mappings'] = []
            for e in self.mappings:
                json['mappings'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(FlowMap, self).from_json(json)
        val = json.get('source')
        if val is not None:
            self.source = Ref()
            self.source.from_json(val)
        val = json.get('target')
        if val is not None:
            self.target = Ref()
            self.target.from_json(val)
        val = json.get('mappings')
        if val is not None:
            self.mappings = []
            for d in val:
                e = FlowMapEntry()
                e.from_json(d)
                self.mappings.append(e)


class FlowMapEntry(RootEntity):
    """A mapping from one flow to another.

    Attributes
    ----------
    from_: FlowMapRef
        The flow, flow property, and unit of the source flow.

    to: FlowMapRef
        The flow, flow property, and unit of the target flow.

    conversion_factor: float
        The factor to convert the original source flow to the target flow.


    """

    def __init__(self):
        super(FlowMapEntry, self).__init__()
        self.from_ = None  # type: FlowMapRef
        self.to = None  # type: FlowMapRef
        self.conversion_factor = None  # type: float

    def to_json(self) -> dict:
        json = super(FlowMapEntry, self).to_json()  # type: dict
        if self.from_ is not None:
            json['from'] = self.from_.to_json()
        if self.to is not None:
            json['to'] = self.to.to_json()
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        return json

    def from_json(self, json: dict):
        super(FlowMapEntry, self).from_json(json)
        val = json.get('from')
        if val is not None:
            self.from_ = FlowMapRef()
            self.from_.from_json(val)
        val = json.get('to')
        if val is not None:
            self.to = FlowMapRef()
            self.to.from_json(val)
        val = json.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val


class ImpactCategory(RootEntity):
    """
    A LCIA category of a LCIA method (see ImpactMethod) which groups a set of 
    characterisation factors 

    Attributes
    ----------
    reference_unit_name: str
        The name of the reference unit of the LCIA category (e.g. kg CO2-eq.).

    impact_factors: List[ImpactFactor]
        The characterisation factors of the LCIA category.


    """

    def __init__(self):
        super(ImpactCategory, self).__init__()
        self.reference_unit_name = None  # type: str
        self.impact_factors = None  # type: List[ImpactFactor]

    def to_json(self) -> dict:
        json = super(ImpactCategory, self).to_json()  # type: dict
        if self.reference_unit_name is not None:
            json['referenceUnitName'] = self.reference_unit_name
        if self.impact_factors is not None:
            json['impactFactors'] = []
            for e in self.impact_factors:
                json['impactFactors'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(ImpactCategory, self).from_json(json)
        val = json.get('referenceUnitName')
        if val is not None:
            self.reference_unit_name = val
        val = json.get('impactFactors')
        if val is not None:
            self.impact_factors = []
            for d in val:
                e = ImpactFactor()
                e.from_json(d)
                self.impact_factors.append(e)


class Location(RootEntity):
    """A location like a country, state, city, etc.

    Attributes
    ----------
    code: str
        The code of the location (e.g. an ISO 2-letter country code).

    latitude: float
        The average latitude of the location.

    longitude: float
        The average longitude of the location.

    kml: str
        KML data of the location.


    """

    def __init__(self):
        super(Location, self).__init__()
        self.code = None  # type: str
        self.latitude = None  # type: float
        self.longitude = None  # type: float
        self.kml = None  # type: str

    def to_json(self) -> dict:
        json = super(Location, self).to_json()  # type: dict
        if self.code is not None:
            json['code'] = self.code
        if self.latitude is not None:
            json['latitude'] = self.latitude
        if self.longitude is not None:
            json['longitude'] = self.longitude
        if self.kml is not None:
            json['kml'] = self.kml
        return json

    def from_json(self, json: dict):
        super(Location, self).from_json(json)
        val = json.get('code')
        if val is not None:
            self.code = val
        val = json.get('latitude')
        if val is not None:
            self.latitude = val
        val = json.get('longitude')
        if val is not None:
            self.longitude = val
        val = json.get('kml')
        if val is not None:
            self.kml = val


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


    """

    def __init__(self):
        super(Ref, self).__init__()
        self.category_path = None  # type: List[str]

    def to_json(self) -> dict:
        json = super(Ref, self).to_json()  # type: dict
        if self.category_path is not None:
            json['categoryPath'] = []
            for e in self.category_path:
                json['categoryPath'].append(e)
        return json

    def from_json(self, json: dict):
        super(Ref, self).from_json(json)
        val = json.get('categoryPath')
        if val is not None:
            self.category_path = []
            for d in val:
                e = d
                self.category_path.append(e)


class Unit(RootEntity):
    """An unit of measure

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

    def __init__(self):
        super(Unit, self).__init__()
        self.conversion_factor = None  # type: float
        self.reference_unit = None  # type: bool
        self.synonyms = None  # type: List[str]

    def to_json(self) -> dict:
        json = super(Unit, self).to_json()  # type: dict
        if self.conversion_factor is not None:
            json['conversionFactor'] = self.conversion_factor
        if self.reference_unit is not None:
            json['referenceUnit'] = self.reference_unit
        if self.synonyms is not None:
            json['synonyms'] = []
            for e in self.synonyms:
                json['synonyms'].append(e)
        return json

    def from_json(self, json: dict):
        super(Unit, self).from_json(json)
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


class Actor(CategorizedEntity):
    """An actor is a person or organisation."""

    def __init__(self):
        super(Actor, self).__init__()
        self.address = None  # type: str
        self.city = None  # type: str
        self.country = None  # type: str
        self.email = None  # type: str
        self.telefax = None  # type: str
        self.telephone = None  # type: str
        self.website = None  # type: str
        self.zip_code = None  # type: str

    def to_json(self) -> dict:
        json = super(Actor, self).to_json()  # type: dict
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

    def from_json(self, json: dict):
        super(Actor, self).from_json(json)
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

    def __init__(self):
        super(Category, self).__init__()
        self.model_type = None  # type: ModelType

    def to_json(self) -> dict:
        json = super(Category, self).to_json()  # type: dict
        if self.model_type is not None:
            json['modelType'] = self.model_type.value
        return json

    def from_json(self, json: dict):
        super(Category, self).from_json(json)
        val = json.get('modelType')
        if val is not None:
            self.model_type = ModelType(val)


class DqSystem(CategorizedEntity):
    """A data quality system."""

    def __init__(self):
        super(DqSystem, self).__init__()
        self.has_uncertainties = None  # type: bool
        self.source = None  # type: Ref
        self.indicators = None  # type: List[DqIndicator]

    def to_json(self) -> dict:
        json = super(DqSystem, self).to_json()  # type: dict
        if self.has_uncertainties is not None:
            json['hasUncertainties'] = self.has_uncertainties
        if self.source is not None:
            json['source'] = self.source.to_json()
        if self.indicators is not None:
            json['indicators'] = []
            for e in self.indicators:
                json['indicators'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(DqSystem, self).from_json(json)
        val = json.get('hasUncertainties')
        if val is not None:
            self.has_uncertainties = val
        val = json.get('source')
        if val is not None:
            self.source = Ref()
            self.source.from_json(val)
        val = json.get('indicators')
        if val is not None:
            self.indicators = []
            for d in val:
                e = DqIndicator()
                e.from_json(d)
                self.indicators.append(e)


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


    """

    def __init__(self):
        super(Flow, self).__init__()
        self.flow_type = None  # type: FlowType
        self.cas = None  # type: str
        self.formula = None  # type: str
        self.flow_properties = None  # type: List[FlowPropertyFactor]
        self.location = None  # type: Ref

    def to_json(self) -> dict:
        json = super(Flow, self).to_json()  # type: dict
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
        return json

    def from_json(self, json: dict):
        super(Flow, self).from_json(json)
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
                e.from_json(d)
                self.flow_properties.append(e)
        val = json.get('location')
        if val is not None:
            self.location = Ref()
            self.location.from_json(val)


class FlowProperty(CategorizedEntity):
    """A flow property is a quantity that can be used to express amounts of a flow.

    Attributes
    ----------
    flow_property_type: FlowPropertyType
        The type of the flow property

    unit_group: Ref
        The units of measure that can be used to express quantities of the flow
        property.


    """

    def __init__(self):
        super(FlowProperty, self).__init__()
        self.flow_property_type = None  # type: FlowPropertyType
        self.unit_group = None  # type: Ref

    def to_json(self) -> dict:
        json = super(FlowProperty, self).to_json()  # type: dict
        if self.flow_property_type is not None:
            json['flowPropertyType'] = self.flow_property_type.value
        if self.unit_group is not None:
            json['unitGroup'] = self.unit_group.to_json()
        return json

    def from_json(self, json: dict):
        super(FlowProperty, self).from_json(json)
        val = json.get('flowPropertyType')
        if val is not None:
            self.flow_property_type = FlowPropertyType(val)
        val = json.get('unitGroup')
        if val is not None:
            self.unit_group = Ref()
            self.unit_group.from_json(val)


class FlowRef(Ref):
    """A reference to a [Flow] data set.

    Attributes
    ----------
    ref_unit: str
        The name (symbol) of the reference unit of the flow.

    location: str
        The location name or code of the flow. Typically, this is only used for
        product flows in databases like ecoinvent.

    flow_type: FlowType
        The type of the flow.


    """

    def __init__(self):
        super(FlowRef, self).__init__()
        self.ref_unit = None  # type: str
        self.location = None  # type: str
        self.flow_type = None  # type: FlowType

    def to_json(self) -> dict:
        json = super(FlowRef, self).to_json()  # type: dict
        if self.ref_unit is not None:
            json['refUnit'] = self.ref_unit
        if self.location is not None:
            json['location'] = self.location
        if self.flow_type is not None:
            json['flowType'] = self.flow_type.value
        return json

    def from_json(self, json: dict):
        super(FlowRef, self).from_json(json)
        val = json.get('refUnit')
        if val is not None:
            self.ref_unit = val
        val = json.get('location')
        if val is not None:
            self.location = val
        val = json.get('flowType')
        if val is not None:
            self.flow_type = FlowType(val)


class ImpactCategoryRef(Ref):
    """A reference to a [ImpactCategory] data set.

    Attributes
    ----------
    ref_unit: str
        The name (symbol) of the reference unit of the impact category.


    """

    def __init__(self):
        super(ImpactCategoryRef, self).__init__()
        self.ref_unit = None  # type: str

    def to_json(self) -> dict:
        json = super(ImpactCategoryRef, self).to_json()  # type: dict
        if self.ref_unit is not None:
            json['refUnit'] = self.ref_unit
        return json

    def from_json(self, json: dict):
        super(ImpactCategoryRef, self).from_json(json)
        val = json.get('refUnit')
        if val is not None:
            self.ref_unit = val


class ImpactMethod(CategorizedEntity):
    """A impact assessment method.

    Attributes
    ----------
    impact_categories: List[ImpactCategoryRef]
        The LCIA categories of the method.

    parameters: List[Parameter]
        A set of method specific parameters which can be used in formulas of
        the characterisation factors in this method.


    """

    def __init__(self):
        super(ImpactMethod, self).__init__()
        self.impact_categories = None  # type: List[ImpactCategoryRef]
        self.parameters = None  # type: List[Parameter]

    def to_json(self) -> dict:
        json = super(ImpactMethod, self).to_json()  # type: dict
        if self.impact_categories is not None:
            json['impactCategories'] = []
            for e in self.impact_categories:
                json['impactCategories'].append(e.to_json())
        if self.parameters is not None:
            json['parameters'] = []
            for e in self.parameters:
                json['parameters'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(ImpactMethod, self).from_json(json)
        val = json.get('impactCategories')
        if val is not None:
            self.impact_categories = []
            for d in val:
                e = ImpactCategoryRef()
                e.from_json(d)
                self.impact_categories.append(e)
        val = json.get('parameters')
        if val is not None:
            self.parameters = []
            for d in val:
                e = Parameter()
                e.from_json(d)
                self.parameters.append(e)


class Process(CategorizedEntity):

    def __init__(self):
        super(Process, self).__init__()
        self.default_allocation_method = None  # type: AllocationType
        self.allocation_factors = None  # type: List[AllocationFactor]
        self.exchanges = None  # type: List[Exchange]
        self.location = None  # type: Location
        self.parameters = None  # type: List[Parameter]
        self.process_documentation = None  # type: ProcessDocumentation
        self.process_type = None  # type: ProcessType
        self.dq_system = None  # type: Ref
        self.exchange_dq_system = None  # type: Ref
        self.social_dq_system = None  # type: Ref
        self.dq_entry = None  # type: str

    def to_json(self) -> dict:
        json = super(Process, self).to_json()  # type: dict
        if self.default_allocation_method is not None:
            json['defaultAllocationMethod'] = self.default_allocation_method.value
        if self.allocation_factors is not None:
            json['allocationFactors'] = []
            for e in self.allocation_factors:
                json['allocationFactors'].append(e.to_json())
        if self.exchanges is not None:
            json['exchanges'] = []
            for e in self.exchanges:
                json['exchanges'].append(e.to_json())
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
        return json

    def from_json(self, json: dict):
        super(Process, self).from_json(json)
        val = json.get('defaultAllocationMethod')
        if val is not None:
            self.default_allocation_method = AllocationType(val)
        val = json.get('allocationFactors')
        if val is not None:
            self.allocation_factors = []
            for d in val:
                e = AllocationFactor()
                e.from_json(d)
                self.allocation_factors.append(e)
        val = json.get('exchanges')
        if val is not None:
            self.exchanges = []
            for d in val:
                e = Exchange()
                e.from_json(d)
                self.exchanges.append(e)
        val = json.get('location')
        if val is not None:
            self.location = Location()
            self.location.from_json(val)
        val = json.get('parameters')
        if val is not None:
            self.parameters = []
            for d in val:
                e = Parameter()
                e.from_json(d)
                self.parameters.append(e)
        val = json.get('processDocumentation')
        if val is not None:
            self.process_documentation = ProcessDocumentation()
            self.process_documentation.from_json(val)
        val = json.get('processType')
        if val is not None:
            self.process_type = ProcessType(val)
        val = json.get('dqSystem')
        if val is not None:
            self.dq_system = Ref()
            self.dq_system.from_json(val)
        val = json.get('exchangeDqSystem')
        if val is not None:
            self.exchange_dq_system = Ref()
            self.exchange_dq_system.from_json(val)
        val = json.get('socialDqSystem')
        if val is not None:
            self.social_dq_system = Ref()
            self.social_dq_system.from_json(val)
        val = json.get('dqEntry')
        if val is not None:
            self.dq_entry = val


class ProcessRef(Ref):
    """A reference to a [Process] data set.

    Attributes
    ----------
    location: str
        The location name or code of the process.

    process_type: ProcessType
        The type of the process.


    """

    def __init__(self):
        super(ProcessRef, self).__init__()
        self.location = None  # type: str
        self.process_type = None  # type: ProcessType

    def to_json(self) -> dict:
        json = super(ProcessRef, self).to_json()  # type: dict
        if self.location is not None:
            json['location'] = self.location
        if self.process_type is not None:
            json['processType'] = self.process_type.value
        return json

    def from_json(self, json: dict):
        super(ProcessRef, self).from_json(json)
        val = json.get('location')
        if val is not None:
            self.location = val
        val = json.get('processType')
        if val is not None:
            self.process_type = ProcessType(val)


class ProductSystem(CategorizedEntity):
    """
    A product system describes the supply chain of a product (the functional 
    unit) ... 

    Attributes
    ----------
    processes: List[ProcessRef]
        The descriptors of all processes that are contained in the product
        system.

    reference_process: ProcessRef
        The descriptor of the process that provides the flow of the functional
        unit of the product system.

    reference_exchange: Exchange
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


    """

    def __init__(self):
        super(ProductSystem, self).__init__()
        self.processes = None  # type: List[ProcessRef]
        self.reference_process = None  # type: ProcessRef
        self.reference_exchange = None  # type: Exchange
        self.target_amount = None  # type: float
        self.target_unit = None  # type: Ref
        self.target_flow_property = None  # type: Ref
        self.process_links = None  # type: List[ProcessLink]

    def to_json(self) -> dict:
        json = super(ProductSystem, self).to_json()  # type: dict
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
        return json

    def from_json(self, json: dict):
        super(ProductSystem, self).from_json(json)
        val = json.get('processes')
        if val is not None:
            self.processes = []
            for d in val:
                e = ProcessRef()
                e.from_json(d)
                self.processes.append(e)
        val = json.get('referenceProcess')
        if val is not None:
            self.reference_process = ProcessRef()
            self.reference_process.from_json(val)
        val = json.get('referenceExchange')
        if val is not None:
            self.reference_exchange = Exchange()
            self.reference_exchange.from_json(val)
        val = json.get('targetAmount')
        if val is not None:
            self.target_amount = val
        val = json.get('targetUnit')
        if val is not None:
            self.target_unit = Ref()
            self.target_unit.from_json(val)
        val = json.get('targetFlowProperty')
        if val is not None:
            self.target_flow_property = Ref()
            self.target_flow_property.from_json(val)
        val = json.get('processLinks')
        if val is not None:
            self.process_links = []
            for d in val:
                e = ProcessLink()
                e.from_json(d)
                self.process_links.append(e)


class SocialIndicator(CategorizedEntity):

    def __init__(self):
        super(SocialIndicator, self).__init__()
        self.activity_variable = None  # type: str
        self.activity_quantity = None  # type: Ref
        self.activity_unit = None  # type: Ref
        self.unit_of_measurement = None  # type: str
        self.evaluation_scheme = None  # type: str

    def to_json(self) -> dict:
        json = super(SocialIndicator, self).to_json()  # type: dict
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

    def from_json(self, json: dict):
        super(SocialIndicator, self).from_json(json)
        val = json.get('activityVariable')
        if val is not None:
            self.activity_variable = val
        val = json.get('activityQuantity')
        if val is not None:
            self.activity_quantity = Ref()
            self.activity_quantity.from_json(val)
        val = json.get('activityUnit')
        if val is not None:
            self.activity_unit = Ref()
            self.activity_unit.from_json(val)
        val = json.get('unitOfMeasurement')
        if val is not None:
            self.unit_of_measurement = val
        val = json.get('evaluationScheme')
        if val is not None:
            self.evaluation_scheme = val


class Source(CategorizedEntity):
    """A source is a literature reference.

    Attributes
    ----------
    doi: str
        The digital object identifier of the source (see
        http://en.wikipedia.org/wiki/Digital_object_identifier).

    text_reference: str
        The full text reference of the source.

    year: int
        The publication year of the source.

    external_file: str
        A direct link (relative or absolute URL) to the source file.


    """

    def __init__(self):
        super(Source, self).__init__()
        self.doi = None  # type: str
        self.text_reference = None  # type: str
        self.year = None  # type: int
        self.external_file = None  # type: str

    def to_json(self) -> dict:
        json = super(Source, self).to_json()  # type: dict
        if self.doi is not None:
            json['doi'] = self.doi
        if self.text_reference is not None:
            json['textReference'] = self.text_reference
        if self.year is not None:
            json['year'] = self.year
        if self.external_file is not None:
            json['externalFile'] = self.external_file
        return json

    def from_json(self, json: dict):
        super(Source, self).from_json(json)
        val = json.get('doi')
        if val is not None:
            self.doi = val
        val = json.get('textReference')
        if val is not None:
            self.text_reference = val
        val = json.get('year')
        if val is not None:
            self.year = val
        val = json.get('externalFile')
        if val is not None:
            self.external_file = val


class UnitGroup(CategorizedEntity):
    """A group of units that can be converted into each other.

    Attributes
    ----------
    default_flow_property: Ref
        Some LCA data formats do not have the concept of flow properties or
        quantities. This field provides a default link to a flow property for
        units that are contained in this group.

    units: List[Unit]
        The units of the unit group.


    """

    def __init__(self):
        super(UnitGroup, self).__init__()
        self.default_flow_property = None  # type: Ref
        self.units = None  # type: List[Unit]

    def to_json(self) -> dict:
        json = super(UnitGroup, self).to_json()  # type: dict
        if self.default_flow_property is not None:
            json['defaultFlowProperty'] = self.default_flow_property.to_json()
        if self.units is not None:
            json['units'] = []
            for e in self.units:
                json['units'].append(e.to_json())
        return json

    def from_json(self, json: dict):
        super(UnitGroup, self).from_json(json)
        val = json.get('defaultFlowProperty')
        if val is not None:
            self.default_flow_property = Ref()
            self.default_flow_property.from_json(val)
        val = json.get('units')
        if val is not None:
            self.units = []
            for d in val:
                e = Unit()
                e.from_json(d)
                self.units.append(e)
