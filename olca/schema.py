# This module contains a Python API of the JSON-LD based
# openLCA data exchange model.package schema.
# For more information see http://greendelta.github.io/olca-schema/

from enum import Enum


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
        pass

    def to_json(self) -> dict:
        return {}

    def from_json(self, jdict: dict):
        pass


class AllocationFactor(Entity):

    def __init__(self):
        super(AllocationFactor, self).__init__()
        self.product_exchange = None  # type: Exchange
        self.allocation_type = None  # type: AllocationType
        self.value = None  # type: float
        self.allocated_exchange = None  # type: Exchange

    def to_json(self) -> dict:
        jdict = super(AllocationFactor, self).to_json()  # type: dict
        if self.product_exchange is not None:
            jdict['productExchange'] = self.product_exchange.to_json()
        if self.allocation_type is not None:
            jdict['allocationType'] = self.allocation_type.value
        if self.value is not None:
            jdict['value'] = self.value
        if self.allocated_exchange is not None:
            jdict['allocatedExchange'] = self.allocated_exchange.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(AllocationFactor, self).from_json(jdict)
        val = jdict.get('productExchange')
        if val is not None:
            self.product_exchange = Exchange()
            self.product_exchange.from_json(val)
        val = jdict.get('allocationType')
        if val is not None:
            self.allocation_type = AllocationType(val)
        val = jdict.get('value')
        if val is not None:
            self.value = val
        val = jdict.get('allocatedExchange')
        if val is not None:
            self.allocated_exchange = Exchange()
            self.allocated_exchange.from_json(val)


class Exchange(Entity):

    def __init__(self):
        super(Exchange, self).__init__()
        self.internal_id = None  # type: int
        self.avoided_product = None  # type: bool
        self.flow = None  # type: Flow
        self.flow_property = None  # type: FlowProperty
        self.input = None  # type: bool
        self.quantitative_reference = None  # type: bool
        self.base_uncertainty = None  # type: float
        self.provider = None  # type: Process
        self.amount = None  # type: float
        self.amount_formula = None  # type: str
        self.unit = None  # type: Unit
        self.pedigree_uncertainty = None  # type: str
        self.uncertainty = None  # type: Uncertainty
        self.comment = None  # type: str

    def to_json(self) -> dict:
        jdict = super(Exchange, self).to_json()  # type: dict
        if self.internal_id is not None:
            jdict['internalId'] = self.internal_id
        if self.avoided_product is not None:
            jdict['avoidedProduct'] = self.avoided_product
        if self.flow is not None:
            jdict['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            jdict['flowProperty'] = self.flow_property.to_json()
        if self.input is not None:
            jdict['input'] = self.input
        if self.quantitative_reference is not None:
            jdict['quantitativeReference'] = self.quantitative_reference
        if self.base_uncertainty is not None:
            jdict['baseUncertainty'] = self.base_uncertainty
        if self.provider is not None:
            jdict['provider'] = self.provider.to_json()
        if self.amount is not None:
            jdict['amount'] = self.amount
        if self.amount_formula is not None:
            jdict['amountFormula'] = self.amount_formula
        if self.unit is not None:
            jdict['unit'] = self.unit.to_json()
        if self.pedigree_uncertainty is not None:
            jdict['pedigreeUncertainty'] = self.pedigree_uncertainty
        if self.uncertainty is not None:
            jdict['uncertainty'] = self.uncertainty.to_json()
        if self.comment is not None:
            jdict['comment'] = self.comment
        return jdict

    def from_json(self, jdict: dict):
        super(Exchange, self).from_json(jdict)
        val = jdict.get('internalId')
        if val is not None:
            self.internal_id = val
        val = jdict.get('avoidedProduct')
        if val is not None:
            self.avoided_product = val
        val = jdict.get('flow')
        if val is not None:
            self.flow = Flow()
            self.flow.from_json(val)
        val = jdict.get('flowProperty')
        if val is not None:
            self.flow_property = FlowProperty()
            self.flow_property.from_json(val)
        val = jdict.get('input')
        if val is not None:
            self.input = val
        val = jdict.get('quantitativeReference')
        if val is not None:
            self.quantitative_reference = val
        val = jdict.get('baseUncertainty')
        if val is not None:
            self.base_uncertainty = val
        val = jdict.get('provider')
        if val is not None:
            self.provider = Process()
            self.provider.from_json(val)
        val = jdict.get('amount')
        if val is not None:
            self.amount = val
        val = jdict.get('amountFormula')
        if val is not None:
            self.amount_formula = val
        val = jdict.get('unit')
        if val is not None:
            self.unit = Unit()
            self.unit.from_json(val)
        val = jdict.get('pedigreeUncertainty')
        if val is not None:
            self.pedigree_uncertainty = val
        val = jdict.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)
        val = jdict.get('comment')
        if val is not None:
            self.comment = val


class FlowPropertyFactor(Entity):

    def __init__(self):
        super(FlowPropertyFactor, self).__init__()
        self.flow_property = None  # type: FlowProperty
        self.conversion_factor = None  # type: float
        self.reference_flow_property = None  # type: bool

    def to_json(self) -> dict:
        jdict = super(FlowPropertyFactor, self).to_json()  # type: dict
        if self.flow_property is not None:
            jdict['flowProperty'] = self.flow_property.to_json()
        if self.conversion_factor is not None:
            jdict['conversionFactor'] = self.conversion_factor
        if self.reference_flow_property is not None:
            jdict['referenceFlowProperty'] = self.reference_flow_property
        return jdict

    def from_json(self, jdict: dict):
        super(FlowPropertyFactor, self).from_json(jdict)
        val = jdict.get('flowProperty')
        if val is not None:
            self.flow_property = FlowProperty()
            self.flow_property.from_json(val)
        val = jdict.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val
        val = jdict.get('referenceFlowProperty')
        if val is not None:
            self.reference_flow_property = val


class ImpactFactor(Entity):

    def __init__(self):
        super(ImpactFactor, self).__init__()
        self.flow = None  # type: Flow
        self.flow_property = None  # type: FlowProperty
        self.unit = None  # type: Unit
        self.value = None  # type: float
        self.formula = None  # type: str
        self.uncertainty = None  # type: Uncertainty

    def to_json(self) -> dict:
        jdict = super(ImpactFactor, self).to_json()  # type: dict
        if self.flow is not None:
            jdict['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            jdict['flowProperty'] = self.flow_property.to_json()
        if self.unit is not None:
            jdict['unit'] = self.unit.to_json()
        if self.value is not None:
            jdict['value'] = self.value
        if self.formula is not None:
            jdict['formula'] = self.formula
        if self.uncertainty is not None:
            jdict['uncertainty'] = self.uncertainty.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(ImpactFactor, self).from_json(jdict)
        val = jdict.get('flow')
        if val is not None:
            self.flow = Flow()
            self.flow.from_json(val)
        val = jdict.get('flowProperty')
        if val is not None:
            self.flow_property = FlowProperty()
            self.flow_property.from_json(val)
        val = jdict.get('unit')
        if val is not None:
            self.unit = Unit()
            self.unit.from_json(val)
        val = jdict.get('value')
        if val is not None:
            self.value = val
        val = jdict.get('formula')
        if val is not None:
            self.formula = val
        val = jdict.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)


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
        jdict = super(Parameter, self).to_json()  # type: dict
        if self.name is not None:
            jdict['name'] = self.name
        if self.description is not None:
            jdict['description'] = self.description
        if self.parameter_scope is not None:
            jdict['parameterScope'] = self.parameter_scope.value
        if self.input_parameter is not None:
            jdict['inputParameter'] = self.input_parameter
        if self.value is not None:
            jdict['value'] = self.value
        if self.formula is not None:
            jdict['formula'] = self.formula
        if self.external_source is not None:
            jdict['externalSource'] = self.external_source
        if self.source_type is not None:
            jdict['sourceType'] = self.source_type
        if self.uncertainty is not None:
            jdict['uncertainty'] = self.uncertainty.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(Parameter, self).from_json(jdict)
        val = jdict.get('name')
        if val is not None:
            self.name = val
        val = jdict.get('description')
        if val is not None:
            self.description = val
        val = jdict.get('parameterScope')
        if val is not None:
            self.parameter_scope = ParameterScope(val)
        val = jdict.get('inputParameter')
        if val is not None:
            self.input_parameter = val
        val = jdict.get('value')
        if val is not None:
            self.value = val
        val = jdict.get('formula')
        if val is not None:
            self.formula = val
        val = jdict.get('externalSource')
        if val is not None:
            self.external_source = val
        val = jdict.get('sourceType')
        if val is not None:
            self.source_type = val
        val = jdict.get('uncertainty')
        if val is not None:
            self.uncertainty = Uncertainty()
            self.uncertainty.from_json(val)


class ProcessDocumentation(Entity):

    def __init__(self):
        super(ProcessDocumentation, self).__init__()
        self.time_description = None  # type: str
        self.valid_until = None  # type: date
        self.valid_from = None  # type: date
        self.technology_description = None  # type: str
        self.data_collection_description = None  # type: str
        self.completeness_description = None  # type: str
        self.data_selection_description = None  # type: str
        self.review_details = None  # type: str
        self.data_treatment_description = None  # type: str
        self.inventory_method_description = None  # type: str
        self.modeling_constants_description = None  # type: str
        self.reviewer = None  # type: Actor
        self.sampling_description = None  # type: str
        self.sources = None  # type: List[Source]
        self.restrictions_description = None  # type: str
        self.copyright = None  # type: bool
        self.creation_date = None  # type: str
        self.data_documentor = None  # type: Actor
        self.data_generator = None  # type: Actor
        self.data_set_owner = None  # type: Actor
        self.intended_application = None  # type: str
        self.project_description = None  # type: str
        self.publication = None  # type: Source
        self.geography_description = None  # type: str

    def to_json(self) -> dict:
        jdict = super(ProcessDocumentation, self).to_json()  # type: dict
        if self.time_description is not None:
            jdict['timeDescription'] = self.time_description
        if self.valid_until is not None:
            jdict['validUntil'] = self.valid_until
        if self.valid_from is not None:
            jdict['validFrom'] = self.valid_from
        if self.technology_description is not None:
            jdict['technologyDescription'] = self.technology_description
        if self.data_collection_description is not None:
            jdict['dataCollectionDescription'] = self.data_collection_description
        if self.completeness_description is not None:
            jdict['completenessDescription'] = self.completeness_description
        if self.data_selection_description is not None:
            jdict['dataSelectionDescription'] = self.data_selection_description
        if self.review_details is not None:
            jdict['reviewDetails'] = self.review_details
        if self.data_treatment_description is not None:
            jdict['dataTreatmentDescription'] = self.data_treatment_description
        if self.inventory_method_description is not None:
            jdict['inventoryMethodDescription'] = self.inventory_method_description
        if self.modeling_constants_description is not None:
            jdict['modelingConstantsDescription'] = self.modeling_constants_description
        if self.reviewer is not None:
            jdict['reviewer'] = self.reviewer.to_json()
        if self.sampling_description is not None:
            jdict['samplingDescription'] = self.sampling_description
        if self.sources is not None:
            jdict['sources'] = []
            for e in sources:
                jdict['sources'].append(e.to_json())
        if self.restrictions_description is not None:
            jdict['restrictionsDescription'] = self.restrictions_description
        if self.copyright is not None:
            jdict['copyright'] = self.copyright
        if self.creation_date is not None:
            jdict['creationDate'] = self.creation_date
        if self.data_documentor is not None:
            jdict['dataDocumentor'] = self.data_documentor.to_json()
        if self.data_generator is not None:
            jdict['dataGenerator'] = self.data_generator.to_json()
        if self.data_set_owner is not None:
            jdict['dataSetOwner'] = self.data_set_owner.to_json()
        if self.intended_application is not None:
            jdict['intendedApplication'] = self.intended_application
        if self.project_description is not None:
            jdict['projectDescription'] = self.project_description
        if self.publication is not None:
            jdict['publication'] = self.publication.to_json()
        if self.geography_description is not None:
            jdict['geographyDescription'] = self.geography_description
        return jdict

    def from_json(self, jdict: dict):
        super(ProcessDocumentation, self).from_json(jdict)
        val = jdict.get('timeDescription')
        if val is not None:
            self.time_description = val
        val = jdict.get('validUntil')
        if val is not None:
            self.valid_until = val
        val = jdict.get('validFrom')
        if val is not None:
            self.valid_from = val
        val = jdict.get('technologyDescription')
        if val is not None:
            self.technology_description = val
        val = jdict.get('dataCollectionDescription')
        if val is not None:
            self.data_collection_description = val
        val = jdict.get('completenessDescription')
        if val is not None:
            self.completeness_description = val
        val = jdict.get('dataSelectionDescription')
        if val is not None:
            self.data_selection_description = val
        val = jdict.get('reviewDetails')
        if val is not None:
            self.review_details = val
        val = jdict.get('dataTreatmentDescription')
        if val is not None:
            self.data_treatment_description = val
        val = jdict.get('inventoryMethodDescription')
        if val is not None:
            self.inventory_method_description = val
        val = jdict.get('modelingConstantsDescription')
        if val is not None:
            self.modeling_constants_description = val
        val = jdict.get('reviewer')
        if val is not None:
            self.reviewer = Actor()
            self.reviewer.from_json(val)
        val = jdict.get('samplingDescription')
        if val is not None:
            self.sampling_description = val
        val = jdict.get('sources')
        if val is not None:
            self.sources = []
            for d in val:
                e = Source()
                e.from_json(d)
                self.sources.append(e)
        val = jdict.get('restrictionsDescription')
        if val is not None:
            self.restrictions_description = val
        val = jdict.get('copyright')
        if val is not None:
            self.copyright = val
        val = jdict.get('creationDate')
        if val is not None:
            self.creation_date = val
        val = jdict.get('dataDocumentor')
        if val is not None:
            self.data_documentor = Actor()
            self.data_documentor.from_json(val)
        val = jdict.get('dataGenerator')
        if val is not None:
            self.data_generator = Actor()
            self.data_generator.from_json(val)
        val = jdict.get('dataSetOwner')
        if val is not None:
            self.data_set_owner = Actor()
            self.data_set_owner.from_json(val)
        val = jdict.get('intendedApplication')
        if val is not None:
            self.intended_application = val
        val = jdict.get('projectDescription')
        if val is not None:
            self.project_description = val
        val = jdict.get('publication')
        if val is not None:
            self.publication = Source()
            self.publication.from_json(val)
        val = jdict.get('geographyDescription')
        if val is not None:
            self.geography_description = val


class ProcessLink(Entity):

    def __init__(self):
        super(ProcessLink, self).__init__()
        self.provider = None  # type: Process
        self.flow = None  # type: Flow
        self.process = None  # type: Process
        self.exchange = None  # type: Exchange

    def to_json(self) -> dict:
        jdict = super(ProcessLink, self).to_json()  # type: dict
        if self.provider is not None:
            jdict['provider'] = self.provider.to_json()
        if self.flow is not None:
            jdict['flow'] = self.flow.to_json()
        if self.process is not None:
            jdict['process'] = self.process.to_json()
        if self.exchange is not None:
            jdict['exchange'] = self.exchange.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(ProcessLink, self).from_json(jdict)
        val = jdict.get('provider')
        if val is not None:
            self.provider = Process()
            self.provider.from_json(val)
        val = jdict.get('flow')
        if val is not None:
            self.flow = Flow()
            self.flow.from_json(val)
        val = jdict.get('process')
        if val is not None:
            self.process = Process()
            self.process.from_json(val)
        val = jdict.get('exchange')
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
        jdict = super(RootEntity, self).to_json()  # type: dict
        if self.name is not None:
            jdict['name'] = self.name
        if self.description is not None:
            jdict['description'] = self.description
        if self.version is not None:
            jdict['version'] = self.version
        if self.last_change is not None:
            jdict['lastChange'] = self.last_change
        return jdict

    def from_json(self, jdict: dict):
        super(RootEntity, self).from_json(jdict)
        val = jdict.get('name')
        if val is not None:
            self.name = val
        val = jdict.get('description')
        if val is not None:
            self.description = val
        val = jdict.get('version')
        if val is not None:
            self.version = val
        val = jdict.get('lastChange')
        if val is not None:
            self.last_change = val


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
        jdict = super(Uncertainty, self).to_json()  # type: dict
        if self.distribution_type is not None:
            jdict['distributionType'] = self.distribution_type.value
        if self.mean is not None:
            jdict['mean'] = self.mean
        if self.mean_formula is not None:
            jdict['meanFormula'] = self.mean_formula
        if self.geom_mean is not None:
            jdict['geomMean'] = self.geom_mean
        if self.geom_mean_formula is not None:
            jdict['geomMeanFormula'] = self.geom_mean_formula
        if self.minimum is not None:
            jdict['minimum'] = self.minimum
        if self.minimum_formula is not None:
            jdict['minimumFormula'] = self.minimum_formula
        if self.sd is not None:
            jdict['sd'] = self.sd
        if self.sd_formula is not None:
            jdict['sdFormula'] = self.sd_formula
        if self.geom_sd is not None:
            jdict['geomSd'] = self.geom_sd
        if self.geom_sd_formula is not None:
            jdict['geomSdFormula'] = self.geom_sd_formula
        if self.mode is not None:
            jdict['mode'] = self.mode
        if self.mode_formula is not None:
            jdict['modeFormula'] = self.mode_formula
        if self.maximum is not None:
            jdict['maximum'] = self.maximum
        if self.maximum_formula is not None:
            jdict['maximumFormula'] = self.maximum_formula
        return jdict

    def from_json(self, jdict: dict):
        super(Uncertainty, self).from_json(jdict)
        val = jdict.get('distributionType')
        if val is not None:
            self.distribution_type = UncertaintyType(val)
        val = jdict.get('mean')
        if val is not None:
            self.mean = val
        val = jdict.get('meanFormula')
        if val is not None:
            self.mean_formula = val
        val = jdict.get('geomMean')
        if val is not None:
            self.geom_mean = val
        val = jdict.get('geomMeanFormula')
        if val is not None:
            self.geom_mean_formula = val
        val = jdict.get('minimum')
        if val is not None:
            self.minimum = val
        val = jdict.get('minimumFormula')
        if val is not None:
            self.minimum_formula = val
        val = jdict.get('sd')
        if val is not None:
            self.sd = val
        val = jdict.get('sdFormula')
        if val is not None:
            self.sd_formula = val
        val = jdict.get('geomSd')
        if val is not None:
            self.geom_sd = val
        val = jdict.get('geomSdFormula')
        if val is not None:
            self.geom_sd_formula = val
        val = jdict.get('mode')
        if val is not None:
            self.mode = val
        val = jdict.get('modeFormula')
        if val is not None:
            self.mode_formula = val
        val = jdict.get('maximum')
        if val is not None:
            self.maximum = val
        val = jdict.get('maximumFormula')
        if val is not None:
            self.maximum_formula = val


class CategorizedEntity(RootEntity):

    def __init__(self):
        super(CategorizedEntity, self).__init__()
        self.category = None  # type: Category

    def to_json(self) -> dict:
        jdict = super(CategorizedEntity, self).to_json()  # type: dict
        if self.category is not None:
            jdict['category'] = self.category.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(CategorizedEntity, self).from_json(jdict)
        val = jdict.get('category')
        if val is not None:
            self.category = Category()
            self.category.from_json(val)


class ImpactCategory(RootEntity):

    def __init__(self):
        super(ImpactCategory, self).__init__()
        self.reference_unit_name = None  # type: str
        self.impact_factors = None  # type: List[ImpactFactor]

    def to_json(self) -> dict:
        jdict = super(ImpactCategory, self).to_json()  # type: dict
        if self.reference_unit_name is not None:
            jdict['referenceUnitName'] = self.reference_unit_name
        if self.impact_factors is not None:
            jdict['impactFactors'] = []
            for e in impact_factors:
                jdict['impactFactors'].append(e.to_json())
        return jdict

    def from_json(self, jdict: dict):
        super(ImpactCategory, self).from_json(jdict)
        val = jdict.get('referenceUnitName')
        if val is not None:
            self.reference_unit_name = val
        val = jdict.get('impactFactors')
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
        jdict = super(Location, self).to_json()  # type: dict
        if self.code is not None:
            jdict['code'] = self.code
        if self.latitude is not None:
            jdict['latitude'] = self.latitude
        if self.longitude is not None:
            jdict['longitude'] = self.longitude
        if self.kml is not None:
            jdict['kml'] = self.kml
        return jdict

    def from_json(self, jdict: dict):
        super(Location, self).from_json(jdict)
        val = jdict.get('code')
        if val is not None:
            self.code = val
        val = jdict.get('latitude')
        if val is not None:
            self.latitude = val
        val = jdict.get('longitude')
        if val is not None:
            self.longitude = val
        val = jdict.get('kml')
        if val is not None:
            self.kml = val


class Unit(RootEntity):

    def __init__(self):
        super(Unit, self).__init__()
        self.conversion_factor = None  # type: float
        self.reference_unit = None  # type: bool
        self.synonyms = None  # type: List[string]

    def to_json(self) -> dict:
        jdict = super(Unit, self).to_json()  # type: dict
        if self.conversion_factor is not None:
            jdict['conversionFactor'] = self.conversion_factor
        if self.reference_unit is not None:
            jdict['referenceUnit'] = self.reference_unit
        if self.synonyms is not None:
            jdict['synonyms'] = []
            for e in synonyms:
                jdict['synonyms'].append(e.to_json())
        return jdict

    def from_json(self, jdict: dict):
        super(Unit, self).from_json(jdict)
        val = jdict.get('conversionFactor')
        if val is not None:
            self.conversion_factor = val
        val = jdict.get('referenceUnit')
        if val is not None:
            self.reference_unit = val
        val = jdict.get('synonyms')
        if val is not None:
            self.synonyms = []
            for d in val:
                e = string()
                e.from_json(d)
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
        jdict = super(Actor, self).to_json()  # type: dict
        if self.address is not None:
            jdict['address'] = self.address
        if self.city is not None:
            jdict['city'] = self.city
        if self.country is not None:
            jdict['country'] = self.country
        if self.email is not None:
            jdict['email'] = self.email
        if self.telefax is not None:
            jdict['telefax'] = self.telefax
        if self.telephone is not None:
            jdict['telephone'] = self.telephone
        if self.website is not None:
            jdict['website'] = self.website
        if self.zip_code is not None:
            jdict['zipCode'] = self.zip_code
        return jdict

    def from_json(self, jdict: dict):
        super(Actor, self).from_json(jdict)
        val = jdict.get('address')
        if val is not None:
            self.address = val
        val = jdict.get('city')
        if val is not None:
            self.city = val
        val = jdict.get('country')
        if val is not None:
            self.country = val
        val = jdict.get('email')
        if val is not None:
            self.email = val
        val = jdict.get('telefax')
        if val is not None:
            self.telefax = val
        val = jdict.get('telephone')
        if val is not None:
            self.telephone = val
        val = jdict.get('website')
        if val is not None:
            self.website = val
        val = jdict.get('zipCode')
        if val is not None:
            self.zip_code = val


class Category(CategorizedEntity):

    def __init__(self):
        super(Category, self).__init__()
        self.model_type = None  # type: ModelType

    def to_json(self) -> dict:
        jdict = super(Category, self).to_json()  # type: dict
        if self.model_type is not None:
            jdict['modelType'] = self.model_type.value
        return jdict

    def from_json(self, jdict: dict):
        super(Category, self).from_json(jdict)
        val = jdict.get('modelType')
        if val is not None:
            self.model_type = ModelType(val)


class Flow(CategorizedEntity):

    def __init__(self):
        super(Flow, self).__init__()
        self.flow_type = None  # type: FlowType
        self.cas = None  # type: str
        self.formula = None  # type: str
        self.flow_properties = None  # type: List[FlowPropertyFactor]
        self.location = None  # type: Location

    def to_json(self) -> dict:
        jdict = super(Flow, self).to_json()  # type: dict
        if self.flow_type is not None:
            jdict['flowType'] = self.flow_type.value
        if self.cas is not None:
            jdict['cas'] = self.cas
        if self.formula is not None:
            jdict['formula'] = self.formula
        if self.flow_properties is not None:
            jdict['flowProperties'] = []
            for e in flow_properties:
                jdict['flowProperties'].append(e.to_json())
        if self.location is not None:
            jdict['location'] = self.location.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(Flow, self).from_json(jdict)
        val = jdict.get('flowType')
        if val is not None:
            self.flow_type = FlowType(val)
        val = jdict.get('cas')
        if val is not None:
            self.cas = val
        val = jdict.get('formula')
        if val is not None:
            self.formula = val
        val = jdict.get('flowProperties')
        if val is not None:
            self.flow_properties = []
            for d in val:
                e = FlowPropertyFactor()
                e.from_json(d)
                self.flow_properties.append(e)
        val = jdict.get('location')
        if val is not None:
            self.location = Location()
            self.location.from_json(val)


class FlowProperty(CategorizedEntity):

    def __init__(self):
        super(FlowProperty, self).__init__()
        self.flow_property_type = None  # type: FlowPropertyType
        self.unit_group = None  # type: UnitGroup

    def to_json(self) -> dict:
        jdict = super(FlowProperty, self).to_json()  # type: dict
        if self.flow_property_type is not None:
            jdict['flowPropertyType'] = self.flow_property_type.value
        if self.unit_group is not None:
            jdict['unitGroup'] = self.unit_group.to_json()
        return jdict

    def from_json(self, jdict: dict):
        super(FlowProperty, self).from_json(jdict)
        val = jdict.get('flowPropertyType')
        if val is not None:
            self.flow_property_type = FlowPropertyType(val)
        val = jdict.get('unitGroup')
        if val is not None:
            self.unit_group = UnitGroup()
            self.unit_group.from_json(val)


class ImpactMethod(CategorizedEntity):

    def __init__(self):
        super(ImpactMethod, self).__init__()
        self.impact_categories = None  # type: List[ImpactCategory]
        self.parameters = None  # type: List[Parameter]

    def to_json(self) -> dict:
        jdict = super(ImpactMethod, self).to_json()  # type: dict
        if self.impact_categories is not None:
            jdict['impactCategories'] = []
            for e in impact_categories:
                jdict['impactCategories'].append(e.to_json())
        if self.parameters is not None:
            jdict['parameters'] = []
            for e in parameters:
                jdict['parameters'].append(e.to_json())
        return jdict

    def from_json(self, jdict: dict):
        super(ImpactMethod, self).from_json(jdict)
        val = jdict.get('impactCategories')
        if val is not None:
            self.impact_categories = []
            for d in val:
                e = ImpactCategory()
                e.from_json(d)
                self.impact_categories.append(e)
        val = jdict.get('parameters')
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
        jdict = super(Process, self).to_json()  # type: dict
        if self.default_allocation_method is not None:
            jdict['defaultAllocationMethod'] = self.default_allocation_method.value
        if self.allocation_factors is not None:
            jdict['allocationFactors'] = []
            for e in allocation_factors:
                jdict['allocationFactors'].append(e.to_json())
        if self.exchanges is not None:
            jdict['exchanges'] = []
            for e in exchanges:
                jdict['exchanges'].append(e.to_json())
        if self.location is not None:
            jdict['location'] = self.location.to_json()
        if self.parameters is not None:
            jdict['parameters'] = []
            for e in parameters:
                jdict['parameters'].append(e.to_json())
        if self.process_documentation is not None:
            jdict['processDocumentation'] = self.process_documentation.to_json()
        if self.process_type is not None:
            jdict['processType'] = self.process_type.value
        return jdict

    def from_json(self, jdict: dict):
        super(Process, self).from_json(jdict)
        val = jdict.get('defaultAllocationMethod')
        if val is not None:
            self.default_allocation_method = AllocationType(val)
        val = jdict.get('allocationFactors')
        if val is not None:
            self.allocation_factors = []
            for d in val:
                e = AllocationFactor()
                e.from_json(d)
                self.allocation_factors.append(e)
        val = jdict.get('exchanges')
        if val is not None:
            self.exchanges = []
            for d in val:
                e = Exchange()
                e.from_json(d)
                self.exchanges.append(e)
        val = jdict.get('location')
        if val is not None:
            self.location = Location()
            self.location.from_json(val)
        val = jdict.get('parameters')
        if val is not None:
            self.parameters = []
            for d in val:
                e = Parameter()
                e.from_json(d)
                self.parameters.append(e)
        val = jdict.get('processDocumentation')
        if val is not None:
            self.process_documentation = ProcessDocumentation()
            self.process_documentation.from_json(val)
        val = jdict.get('processType')
        if val is not None:
            self.process_type = ProcessType(val)


class ProductSystem(CategorizedEntity):

    def __init__(self):
        super(ProductSystem, self).__init__()
        self.processes = None  # type: List[Process]
        self.reference_process = None  # type: Process
        self.reference_exchange = None  # type: Exchange
        self.target_amount = None  # type: float
        self.target_unit = None  # type: Unit
        self.target_flow_property = None  # type: FlowProperty
        self.process_links = None  # type: List[ProcessLink]

    def to_json(self) -> dict:
        jdict = super(ProductSystem, self).to_json()  # type: dict
        if self.processes is not None:
            jdict['processes'] = []
            for e in processes:
                jdict['processes'].append(e.to_json())
        if self.reference_process is not None:
            jdict['referenceProcess'] = self.reference_process.to_json()
        if self.reference_exchange is not None:
            jdict['referenceExchange'] = self.reference_exchange.to_json()
        if self.target_amount is not None:
            jdict['targetAmount'] = self.target_amount
        if self.target_unit is not None:
            jdict['targetUnit'] = self.target_unit.to_json()
        if self.target_flow_property is not None:
            jdict['targetFlowProperty'] = self.target_flow_property.to_json()
        if self.process_links is not None:
            jdict['processLinks'] = []
            for e in process_links:
                jdict['processLinks'].append(e.to_json())
        return jdict

    def from_json(self, jdict: dict):
        super(ProductSystem, self).from_json(jdict)
        val = jdict.get('processes')
        if val is not None:
            self.processes = []
            for d in val:
                e = Process()
                e.from_json(d)
                self.processes.append(e)
        val = jdict.get('referenceProcess')
        if val is not None:
            self.reference_process = Process()
            self.reference_process.from_json(val)
        val = jdict.get('referenceExchange')
        if val is not None:
            self.reference_exchange = Exchange()
            self.reference_exchange.from_json(val)
        val = jdict.get('targetAmount')
        if val is not None:
            self.target_amount = val
        val = jdict.get('targetUnit')
        if val is not None:
            self.target_unit = Unit()
            self.target_unit.from_json(val)
        val = jdict.get('targetFlowProperty')
        if val is not None:
            self.target_flow_property = FlowProperty()
            self.target_flow_property.from_json(val)
        val = jdict.get('processLinks')
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
        self.activity_quantity = None  # type: FlowProperty
        self.activity_unit = None  # type: Unit
        self.unit_of_measurement = None  # type: str
        self.evaluation_scheme = None  # type: str

    def to_json(self) -> dict:
        jdict = super(SocialIndicator, self).to_json()  # type: dict
        if self.activity_variable is not None:
            jdict['activityVariable'] = self.activity_variable
        if self.activity_quantity is not None:
            jdict['activityQuantity'] = self.activity_quantity.to_json()
        if self.activity_unit is not None:
            jdict['activityUnit'] = self.activity_unit.to_json()
        if self.unit_of_measurement is not None:
            jdict['unitOfMeasurement'] = self.unit_of_measurement
        if self.evaluation_scheme is not None:
            jdict['evaluationScheme'] = self.evaluation_scheme
        return jdict

    def from_json(self, jdict: dict):
        super(SocialIndicator, self).from_json(jdict)
        val = jdict.get('activityVariable')
        if val is not None:
            self.activity_variable = val
        val = jdict.get('activityQuantity')
        if val is not None:
            self.activity_quantity = FlowProperty()
            self.activity_quantity.from_json(val)
        val = jdict.get('activityUnit')
        if val is not None:
            self.activity_unit = Unit()
            self.activity_unit.from_json(val)
        val = jdict.get('unitOfMeasurement')
        if val is not None:
            self.unit_of_measurement = val
        val = jdict.get('evaluationScheme')
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
        jdict = super(Source, self).to_json()  # type: dict
        if self.doi is not None:
            jdict['doi'] = self.doi
        if self.text_reference is not None:
            jdict['textReference'] = self.text_reference
        if self.year is not None:
            jdict['year'] = self.year
        if self.external_file is not None:
            jdict['externalFile'] = self.external_file
        return jdict

    def from_json(self, jdict: dict):
        super(Source, self).from_json(jdict)
        val = jdict.get('doi')
        if val is not None:
            self.doi = val
        val = jdict.get('textReference')
        if val is not None:
            self.text_reference = val
        val = jdict.get('year')
        if val is not None:
            self.year = val
        val = jdict.get('externalFile')
        if val is not None:
            self.external_file = val


class UnitGroup(CategorizedEntity):

    def __init__(self):
        super(UnitGroup, self).__init__()
        self.default_flow_property = None  # type: FlowProperty
        self.units = None  # type: List[Unit]

    def to_json(self) -> dict:
        jdict = super(UnitGroup, self).to_json()  # type: dict
        if self.default_flow_property is not None:
            jdict['defaultFlowProperty'] = self.default_flow_property.to_json()
        if self.units is not None:
            jdict['units'] = []
            for e in units:
                jdict['units'].append(e.to_json())
        return jdict

    def from_json(self, jdict: dict):
        super(UnitGroup, self).from_json(jdict)
        val = jdict.get('defaultFlowProperty')
        if val is not None:
            self.default_flow_property = FlowProperty()
            self.default_flow_property.from_json(val)
        val = jdict.get('units')
        if val is not None:
            self.units = []
            for d in val:
                e = Unit()
                e.from_json(d)
                self.units.append(e)
