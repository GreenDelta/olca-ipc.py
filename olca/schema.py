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


class AllocationFactor(Entity):

    def __init__(self):
        self.product_exchange = None  # type: Exchange
        self.allocation_type = None  # type: AllocationType
        self.value = None  # type: float
        self.allocated_exchange = None  # type: Exchange

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.product_exchange is not None:
            jdict['productExchange'] = self.product_exchange.to_json()
        if self.allocation_type is not None:
            jdict['allocationType'] = self.allocation_type.value
        if self.value is not None:
            jdict['value'] = self.value
            jdict['value'] = self.value.to_json()
        if self.allocated_exchange is not None:
            jdict['allocatedExchange'] = self.allocated_exchange.to_json()
        return jdict


class Exchange(Entity):

    def __init__(self):
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
        jdict = super.to_json()  # type: dict
        if self.internal_id is not None:
            jdict['internalId'] = self.internal_id
            jdict['internalId'] = self.internal_id.to_json()
        if self.avoided_product is not None:
            jdict['avoidedProduct'] = self.avoided_product
            jdict['avoidedProduct'] = self.avoided_product.to_json()
        if self.flow is not None:
            jdict['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            jdict['flowProperty'] = self.flow_property.to_json()
        if self.input is not None:
            jdict['input'] = self.input
            jdict['input'] = self.input.to_json()
        if self.quantitative_reference is not None:
            jdict['quantitativeReference'] = self.quantitative_reference
            jdict['quantitativeReference'] = self.quantitative_reference.to_json()
        if self.base_uncertainty is not None:
            jdict['baseUncertainty'] = self.base_uncertainty
            jdict['baseUncertainty'] = self.base_uncertainty.to_json()
        if self.provider is not None:
            jdict['provider'] = self.provider.to_json()
        if self.amount is not None:
            jdict['amount'] = self.amount
            jdict['amount'] = self.amount.to_json()
        if self.amount_formula is not None:
            jdict['amountFormula'] = self.amount_formula
            jdict['amountFormula'] = self.amount_formula.to_json()
        if self.unit is not None:
            jdict['unit'] = self.unit.to_json()
        if self.pedigree_uncertainty is not None:
            jdict['pedigreeUncertainty'] = self.pedigree_uncertainty
            jdict['pedigreeUncertainty'] = self.pedigree_uncertainty.to_json()
        if self.uncertainty is not None:
            jdict['uncertainty'] = self.uncertainty.to_json()
        if self.comment is not None:
            jdict['comment'] = self.comment
            jdict['comment'] = self.comment.to_json()
        return jdict


class FlowPropertyFactor(Entity):

    def __init__(self):
        self.flow_property = None  # type: FlowProperty
        self.conversion_factor = None  # type: float
        self.reference_flow_property = None  # type: bool

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.flow_property is not None:
            jdict['flowProperty'] = self.flow_property.to_json()
        if self.conversion_factor is not None:
            jdict['conversionFactor'] = self.conversion_factor
            jdict['conversionFactor'] = self.conversion_factor.to_json()
        if self.reference_flow_property is not None:
            jdict['referenceFlowProperty'] = self.reference_flow_property
            jdict['referenceFlowProperty'] = self.reference_flow_property.to_json()
        return jdict


class ImpactFactor(Entity):

    def __init__(self):
        self.flow = None  # type: Flow
        self.flow_property = None  # type: FlowProperty
        self.unit = None  # type: Unit
        self.value = None  # type: float
        self.formula = None  # type: str
        self.uncertainty = None  # type: Uncertainty

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.flow is not None:
            jdict['flow'] = self.flow.to_json()
        if self.flow_property is not None:
            jdict['flowProperty'] = self.flow_property.to_json()
        if self.unit is not None:
            jdict['unit'] = self.unit.to_json()
        if self.value is not None:
            jdict['value'] = self.value
            jdict['value'] = self.value.to_json()
        if self.formula is not None:
            jdict['formula'] = self.formula
            jdict['formula'] = self.formula.to_json()
        if self.uncertainty is not None:
            jdict['uncertainty'] = self.uncertainty.to_json()
        return jdict


class Parameter(Entity):

    def __init__(self):
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
        jdict = super.to_json()  # type: dict
        if self.name is not None:
            jdict['name'] = self.name
            jdict['name'] = self.name.to_json()
        if self.description is not None:
            jdict['description'] = self.description
            jdict['description'] = self.description.to_json()
        if self.parameter_scope is not None:
            jdict['parameterScope'] = self.parameter_scope.value
        if self.input_parameter is not None:
            jdict['inputParameter'] = self.input_parameter
            jdict['inputParameter'] = self.input_parameter.to_json()
        if self.value is not None:
            jdict['value'] = self.value
            jdict['value'] = self.value.to_json()
        if self.formula is not None:
            jdict['formula'] = self.formula
            jdict['formula'] = self.formula.to_json()
        if self.external_source is not None:
            jdict['externalSource'] = self.external_source
            jdict['externalSource'] = self.external_source.to_json()
        if self.source_type is not None:
            jdict['sourceType'] = self.source_type
            jdict['sourceType'] = self.source_type.to_json()
        if self.uncertainty is not None:
            jdict['uncertainty'] = self.uncertainty.to_json()
        return jdict


class ProcessDocumentation(Entity):

    def __init__(self):
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
        jdict = super.to_json()  # type: dict
        if self.time_description is not None:
            jdict['timeDescription'] = self.time_description
            jdict['timeDescription'] = self.time_description.to_json()
        if self.valid_until is not None:
            jdict['validUntil'] = self.valid_until
            jdict['validUntil'] = self.valid_until.to_json()
        if self.valid_from is not None:
            jdict['validFrom'] = self.valid_from
            jdict['validFrom'] = self.valid_from.to_json()
        if self.technology_description is not None:
            jdict['technologyDescription'] = self.technology_description
            jdict['technologyDescription'] = self.technology_description.to_json()
        if self.data_collection_description is not None:
            jdict['dataCollectionDescription'] = self.data_collection_description
            jdict['dataCollectionDescription'] = self.data_collection_description.to_json()
        if self.completeness_description is not None:
            jdict['completenessDescription'] = self.completeness_description
            jdict['completenessDescription'] = self.completeness_description.to_json()
        if self.data_selection_description is not None:
            jdict['dataSelectionDescription'] = self.data_selection_description
            jdict['dataSelectionDescription'] = self.data_selection_description.to_json()
        if self.review_details is not None:
            jdict['reviewDetails'] = self.review_details
            jdict['reviewDetails'] = self.review_details.to_json()
        if self.data_treatment_description is not None:
            jdict['dataTreatmentDescription'] = self.data_treatment_description
            jdict['dataTreatmentDescription'] = self.data_treatment_description.to_json()
        if self.inventory_method_description is not None:
            jdict['inventoryMethodDescription'] = self.inventory_method_description
            jdict['inventoryMethodDescription'] = self.inventory_method_description.to_json()
        if self.modeling_constants_description is not None:
            jdict['modelingConstantsDescription'] = self.modeling_constants_description
            jdict['modelingConstantsDescription'] = self.modeling_constants_description.to_json()
        if self.reviewer is not None:
            jdict['reviewer'] = self.reviewer.to_json()
        if self.sampling_description is not None:
            jdict['samplingDescription'] = self.sampling_description
            jdict['samplingDescription'] = self.sampling_description.to_json()
        if self.sources is not None:
            jdict['sources'] = []
            for e in sources:
                jdict['sources'].append(e.to_json())
        if self.restrictions_description is not None:
            jdict['restrictionsDescription'] = self.restrictions_description
            jdict['restrictionsDescription'] = self.restrictions_description.to_json()
        if self.copyright is not None:
            jdict['copyright'] = self.copyright
            jdict['copyright'] = self.copyright.to_json()
        if self.creation_date is not None:
            jdict['creationDate'] = self.creation_date
            jdict['creationDate'] = self.creation_date.to_json()
        if self.data_documentor is not None:
            jdict['dataDocumentor'] = self.data_documentor.to_json()
        if self.data_generator is not None:
            jdict['dataGenerator'] = self.data_generator.to_json()
        if self.data_set_owner is not None:
            jdict['dataSetOwner'] = self.data_set_owner.to_json()
        if self.intended_application is not None:
            jdict['intendedApplication'] = self.intended_application
            jdict['intendedApplication'] = self.intended_application.to_json()
        if self.project_description is not None:
            jdict['projectDescription'] = self.project_description
            jdict['projectDescription'] = self.project_description.to_json()
        if self.publication is not None:
            jdict['publication'] = self.publication.to_json()
        if self.geography_description is not None:
            jdict['geographyDescription'] = self.geography_description
            jdict['geographyDescription'] = self.geography_description.to_json()
        return jdict


class ProcessLink(Entity):

    def __init__(self):
        self.provider = None  # type: Process
        self.flow = None  # type: Flow
        self.process = None  # type: Process
        self.exchange = None  # type: Exchange

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.provider is not None:
            jdict['provider'] = self.provider.to_json()
        if self.flow is not None:
            jdict['flow'] = self.flow.to_json()
        if self.process is not None:
            jdict['process'] = self.process.to_json()
        if self.exchange is not None:
            jdict['exchange'] = self.exchange.to_json()
        return jdict


class RootEntity(Entity):

    def __init__(self):
        self.name = None  # type: str
        self.description = None  # type: str
        self.version = None  # type: str
        self.last_change = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.name is not None:
            jdict['name'] = self.name
            jdict['name'] = self.name.to_json()
        if self.description is not None:
            jdict['description'] = self.description
            jdict['description'] = self.description.to_json()
        if self.version is not None:
            jdict['version'] = self.version
            jdict['version'] = self.version.to_json()
        if self.last_change is not None:
            jdict['lastChange'] = self.last_change
            jdict['lastChange'] = self.last_change.to_json()
        return jdict


class Uncertainty(Entity):

    def __init__(self):
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
        jdict = super.to_json()  # type: dict
        if self.distribution_type is not None:
            jdict['distributionType'] = self.distribution_type.value
        if self.mean is not None:
            jdict['mean'] = self.mean
            jdict['mean'] = self.mean.to_json()
        if self.mean_formula is not None:
            jdict['meanFormula'] = self.mean_formula
            jdict['meanFormula'] = self.mean_formula.to_json()
        if self.geom_mean is not None:
            jdict['geomMean'] = self.geom_mean
            jdict['geomMean'] = self.geom_mean.to_json()
        if self.geom_mean_formula is not None:
            jdict['geomMeanFormula'] = self.geom_mean_formula
            jdict['geomMeanFormula'] = self.geom_mean_formula.to_json()
        if self.minimum is not None:
            jdict['minimum'] = self.minimum
            jdict['minimum'] = self.minimum.to_json()
        if self.minimum_formula is not None:
            jdict['minimumFormula'] = self.minimum_formula
            jdict['minimumFormula'] = self.minimum_formula.to_json()
        if self.sd is not None:
            jdict['sd'] = self.sd
            jdict['sd'] = self.sd.to_json()
        if self.sd_formula is not None:
            jdict['sdFormula'] = self.sd_formula
            jdict['sdFormula'] = self.sd_formula.to_json()
        if self.geom_sd is not None:
            jdict['geomSd'] = self.geom_sd
            jdict['geomSd'] = self.geom_sd.to_json()
        if self.geom_sd_formula is not None:
            jdict['geomSdFormula'] = self.geom_sd_formula
            jdict['geomSdFormula'] = self.geom_sd_formula.to_json()
        if self.mode is not None:
            jdict['mode'] = self.mode
            jdict['mode'] = self.mode.to_json()
        if self.mode_formula is not None:
            jdict['modeFormula'] = self.mode_formula
            jdict['modeFormula'] = self.mode_formula.to_json()
        if self.maximum is not None:
            jdict['maximum'] = self.maximum
            jdict['maximum'] = self.maximum.to_json()
        if self.maximum_formula is not None:
            jdict['maximumFormula'] = self.maximum_formula
            jdict['maximumFormula'] = self.maximum_formula.to_json()
        return jdict


class CategorizedEntity(RootEntity):

    def __init__(self):
        self.category = None  # type: Category

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.category is not None:
            jdict['category'] = self.category.to_json()
        return jdict


class ImpactCategory(RootEntity):

    def __init__(self):
        self.reference_unit_name = None  # type: str
        self.impact_factors = None  # type: List[ImpactFactor]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.reference_unit_name is not None:
            jdict['referenceUnitName'] = self.reference_unit_name
            jdict['referenceUnitName'] = self.reference_unit_name.to_json()
        if self.impact_factors is not None:
            jdict['impactFactors'] = []
            for e in impact_factors:
                jdict['impactFactors'].append(e.to_json())
        return jdict


class Location(RootEntity):

    def __init__(self):
        self.code = None  # type: str
        self.latitude = None  # type: float
        self.longitude = None  # type: float
        self.kml = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.code is not None:
            jdict['code'] = self.code
            jdict['code'] = self.code.to_json()
        if self.latitude is not None:
            jdict['latitude'] = self.latitude
            jdict['latitude'] = self.latitude.to_json()
        if self.longitude is not None:
            jdict['longitude'] = self.longitude
            jdict['longitude'] = self.longitude.to_json()
        if self.kml is not None:
            jdict['kml'] = self.kml
            jdict['kml'] = self.kml.to_json()
        return jdict


class Unit(RootEntity):

    def __init__(self):
        self.conversion_factor = None  # type: float
        self.reference_unit = None  # type: bool
        self.synonyms = None  # type: List[string]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.conversion_factor is not None:
            jdict['conversionFactor'] = self.conversion_factor
            jdict['conversionFactor'] = self.conversion_factor.to_json()
        if self.reference_unit is not None:
            jdict['referenceUnit'] = self.reference_unit
            jdict['referenceUnit'] = self.reference_unit.to_json()
        if self.synonyms is not None:
            jdict['synonyms'] = []
            for e in synonyms:
                jdict['synonyms'].append(e.to_json())
        return jdict


class Actor(CategorizedEntity):

    def __init__(self):
        self.address = None  # type: str
        self.city = None  # type: str
        self.country = None  # type: str
        self.email = None  # type: str
        self.telefax = None  # type: str
        self.telephone = None  # type: str
        self.website = None  # type: str
        self.zip_code = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.address is not None:
            jdict['address'] = self.address
            jdict['address'] = self.address.to_json()
        if self.city is not None:
            jdict['city'] = self.city
            jdict['city'] = self.city.to_json()
        if self.country is not None:
            jdict['country'] = self.country
            jdict['country'] = self.country.to_json()
        if self.email is not None:
            jdict['email'] = self.email
            jdict['email'] = self.email.to_json()
        if self.telefax is not None:
            jdict['telefax'] = self.telefax
            jdict['telefax'] = self.telefax.to_json()
        if self.telephone is not None:
            jdict['telephone'] = self.telephone
            jdict['telephone'] = self.telephone.to_json()
        if self.website is not None:
            jdict['website'] = self.website
            jdict['website'] = self.website.to_json()
        if self.zip_code is not None:
            jdict['zipCode'] = self.zip_code
            jdict['zipCode'] = self.zip_code.to_json()
        return jdict


class Category(CategorizedEntity):

    def __init__(self):
        self.model_type = None  # type: ModelType

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.model_type is not None:
            jdict['modelType'] = self.model_type.value
        return jdict


class Flow(CategorizedEntity):

    def __init__(self):
        self.flow_type = None  # type: FlowType
        self.cas = None  # type: str
        self.formula = None  # type: str
        self.flow_properties = None  # type: List[FlowPropertyFactor]
        self.location = None  # type: Location

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.flow_type is not None:
            jdict['flowType'] = self.flow_type.value
        if self.cas is not None:
            jdict['cas'] = self.cas
            jdict['cas'] = self.cas.to_json()
        if self.formula is not None:
            jdict['formula'] = self.formula
            jdict['formula'] = self.formula.to_json()
        if self.flow_properties is not None:
            jdict['flowProperties'] = []
            for e in flow_properties:
                jdict['flowProperties'].append(e.to_json())
        if self.location is not None:
            jdict['location'] = self.location.to_json()
        return jdict


class FlowProperty(CategorizedEntity):

    def __init__(self):
        self.flow_property_type = None  # type: FlowPropertyType
        self.unit_group = None  # type: UnitGroup

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.flow_property_type is not None:
            jdict['flowPropertyType'] = self.flow_property_type.value
        if self.unit_group is not None:
            jdict['unitGroup'] = self.unit_group.to_json()
        return jdict


class ImpactMethod(CategorizedEntity):

    def __init__(self):
        self.impact_categories = None  # type: List[ImpactCategory]
        self.parameters = None  # type: List[Parameter]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.impact_categories is not None:
            jdict['impactCategories'] = []
            for e in impact_categories:
                jdict['impactCategories'].append(e.to_json())
        if self.parameters is not None:
            jdict['parameters'] = []
            for e in parameters:
                jdict['parameters'].append(e.to_json())
        return jdict


class Process(CategorizedEntity):

    def __init__(self):
        self.default_allocation_method = None  # type: AllocationType
        self.allocation_factors = None  # type: List[AllocationFactor]
        self.exchanges = None  # type: List[Exchange]
        self.location = None  # type: Location
        self.parameters = None  # type: List[Parameter]
        self.process_documentation = None  # type: ProcessDocumentation
        self.process_type = None  # type: ProcessType

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
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


class ProductSystem(CategorizedEntity):

    def __init__(self):
        self.processes = None  # type: List[Process]
        self.reference_process = None  # type: Process
        self.reference_exchange = None  # type: Exchange
        self.target_amount = None  # type: float
        self.target_unit = None  # type: Unit
        self.target_flow_property = None  # type: FlowProperty
        self.process_links = None  # type: List[ProcessLink]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
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
            jdict['targetAmount'] = self.target_amount.to_json()
        if self.target_unit is not None:
            jdict['targetUnit'] = self.target_unit.to_json()
        if self.target_flow_property is not None:
            jdict['targetFlowProperty'] = self.target_flow_property.to_json()
        if self.process_links is not None:
            jdict['processLinks'] = []
            for e in process_links:
                jdict['processLinks'].append(e.to_json())
        return jdict


class SocialIndicator(CategorizedEntity):

    def __init__(self):
        self.activity_variable = None  # type: str
        self.activity_quantity = None  # type: FlowProperty
        self.activity_unit = None  # type: Unit
        self.unit_of_measurement = None  # type: str
        self.evaluation_scheme = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.activity_variable is not None:
            jdict['activityVariable'] = self.activity_variable
            jdict['activityVariable'] = self.activity_variable.to_json()
        if self.activity_quantity is not None:
            jdict['activityQuantity'] = self.activity_quantity.to_json()
        if self.activity_unit is not None:
            jdict['activityUnit'] = self.activity_unit.to_json()
        if self.unit_of_measurement is not None:
            jdict['unitOfMeasurement'] = self.unit_of_measurement
            jdict['unitOfMeasurement'] = self.unit_of_measurement.to_json()
        if self.evaluation_scheme is not None:
            jdict['evaluationScheme'] = self.evaluation_scheme
            jdict['evaluationScheme'] = self.evaluation_scheme.to_json()
        return jdict


class Source(CategorizedEntity):

    def __init__(self):
        self.doi = None  # type: str
        self.text_reference = None  # type: str
        self.year = None  # type: int
        self.external_file = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.doi is not None:
            jdict['doi'] = self.doi
            jdict['doi'] = self.doi.to_json()
        if self.text_reference is not None:
            jdict['textReference'] = self.text_reference
            jdict['textReference'] = self.text_reference.to_json()
        if self.year is not None:
            jdict['year'] = self.year
            jdict['year'] = self.year.to_json()
        if self.external_file is not None:
            jdict['externalFile'] = self.external_file
            jdict['externalFile'] = self.external_file.to_json()
        return jdict


class UnitGroup(CategorizedEntity):

    def __init__(self):
        self.default_flow_property = None  # type: FlowProperty
        self.units = None  # type: List[Unit]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if self.default_flow_property is not None:
            jdict['defaultFlowProperty'] = self.default_flow_property.to_json()
        if self.units is not None:
            jdict['units'] = []
            for e in units:
                jdict['units'].append(e.to_json())
        return jdict
