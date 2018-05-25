# This module contains a Python API of the JSON-LD based
# openLCA data exchange model.package schema.
# For more information see http://greendelta.github.io/olca-schema/

from enum import Enum
from typing import List


class AllocationType(Enum):
    PHYSICAL_ALLOCATION = 'PHYSICAL_ALLOCATION'
    ECONOMIC_ALLOCATION = 'ECONOMIC_ALLOCATION'
    CAUSAL_ALLOCATION = 'CAUSAL_ALLOCATION'


class FlowPropertyType(Enum):
    ECONOMIC_QUANTITY = 'ECONOMIC_QUANTITY'
    PHYSICAL_QUANTITY = 'PHYSICAL_QUANTITY'


class FlowType(Enum):
    ELEMENTARY_FLOW = 'ELEMENTARY_FLOW'
    PRODUCT_FLOW = 'PRODUCT_FLOW'
    WASTE_FLOW = 'WASTE_FLOW'


class ModelType(Enum):
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
    PROCESS_SCOPE = 'PROCESS_SCOPE'
    LCIA_METHOD_SCOPE = 'LCIA_METHOD_SCOPE'
    GLOBAL_SCOPE = 'GLOBAL_SCOPE'


class ProcessType(Enum):
    LCI_RESULT = 'LCI_RESULT'
    UNIT_PROCESS = 'UNIT_PROCESS'


class UncertaintyType(Enum):
    LOG_NORMAL_DISTRIBUTION = 'LOG_NORMAL_DISTRIBUTION'
    NORMAL_DISTRIBUTION = 'NORMAL_DISTRIBUTION'
    TRIANGLE_DISTRIBUTION = 'TRIANGLE_DISTRIBUTION'
    UNIFORM_DISTRIBUTION = 'UNIFORM_DISTRIBUTION'


class Entity(object):

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

    def __init__(self):
        super(CalculationSetup, self).__init__()
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


class Exchange(Entity):

    def __init__(self):
        super(Exchange, self).__init__()
        self.internal_id = None  # type: int
        self.avoided_product = None  # type: bool
        self.flow = None  # type: FlowRef
        self.flow_property = None  # type: Ref
        self.input = None  # type: bool
        self.quantitative_reference = None  # type: bool
        self.base_uncertainty = None  # type: float
        self.provider = None  # type: ProcessRef
        self.amount = None  # type: float
        self.amount_formula = None  # type: str
        self.unit = None  # type: Unit
        self.pedigree_uncertainty = None  # type: str
        self.uncertainty = None  # type: Uncertainty
        self.comment = None  # type: str

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
        if self.provider is not None:
            json['provider'] = self.provider.to_json()
        if self.amount is not None:
            json['amount'] = self.amount
        if self.amount_formula is not None:
            json['amountFormula'] = self.amount_formula
        if self.unit is not None:
            json['unit'] = self.unit.to_json()
        if self.pedigree_uncertainty is not None:
            json['pedigreeUncertainty'] = self.pedigree_uncertainty
        if self.uncertainty is not None:
            json['uncertainty'] = self.uncertainty.to_json()
        if self.comment is not None:
            json['comment'] = self.comment
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
        val = json.get('provider')
        if val is not None:
            self.provider = ProcessRef()
            self.provider.from_json(val)
        val = json.get('amount')
        if val is not None:
            self.amount = val
        val = json.get('amountFormula')
        if val is not None:
            self.amount_formula = val
        val = json.get('unit')
        if val is not None:
            self.unit = Unit()
            self.unit.from_json(val)
        val = json.get('pedigreeUncertainty')
        if val is not None:
            self.pedigree_uncertainty = val
        val = json.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)
        val = json.get('comment')
        if val is not None:
            self.comment = val


class FlowPropertyFactor(Entity):

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


class ImpactCategory(RootEntity):

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


class Flow(CategorizedEntity):

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


class ProcessRef(Ref):

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
