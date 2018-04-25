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


class AllocationFactor(Entity):

    def __init__(self):
        self.product_exchange = None  # type: Exchange
        self.allocation_type = None  # type: AllocationType
        self.value = None  # type: float
        self.allocated_exchange = None  # type: Exchange


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


class FlowPropertyFactor(Entity):

    def __init__(self):
        self.flow_property = None  # type: FlowProperty
        self.conversion_factor = None  # type: float
        self.reference_flow_property = None  # type: bool


class ImpactFactor(Entity):

    def __init__(self):
        self.flow = None  # type: Flow
        self.flow_property = None  # type: FlowProperty
        self.unit = None  # type: Unit
        self.value = None  # type: float
        self.formula = None  # type: str
        self.uncertainty = None  # type: Uncertainty


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
        self.creation_date = None  # type: dateTime
        self.data_documentor = None  # type: Actor
        self.data_generator = None  # type: Actor
        self.data_set_owner = None  # type: Actor
        self.intended_application = None  # type: str
        self.project_description = None  # type: str
        self.publication = None  # type: Source
        self.geography_description = None  # type: str


class ProcessLink(Entity):

    def __init__(self):
        self.provider = None  # type: Process
        self.flow = None  # type: Flow
        self.process = None  # type: Process
        self.exchange = None  # type: Exchange


class RootEntity(Entity):

    def __init__(self):
        self.name = None  # type: str
        self.description = None  # type: str
        self.version = None  # type: str
        self.last_change = None  # type: dateTime


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


class CategorizedEntity(RootEntity):

    def __init__(self):
        self.category = None  # type: Category


class ImpactCategory(RootEntity):

    def __init__(self):
        self.reference_unit_name = None  # type: str
        self.impact_factors = None  # type: List[ImpactFactor]


class Location(RootEntity):

    def __init__(self):
        self.code = None  # type: str
        self.latitude = None  # type: float
        self.longitude = None  # type: float
        self.kml = None  # type: str


class Unit(RootEntity):

    def __init__(self):
        self.conversion_factor = None  # type: float
        self.reference_unit = None  # type: bool
        self.synonyms = None  # type: List[string]


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


class Category(CategorizedEntity):

    def __init__(self):
        self.model_type = None  # type: ModelType


class Flow(CategorizedEntity):

    def __init__(self):
        self.flow_type = None  # type: FlowType
        self.cas = None  # type: str
        self.formula = None  # type: str
        self.flow_properties = None  # type: List[FlowPropertyFactor]
        self.location = None  # type: Location


class FlowProperty(CategorizedEntity):

    def __init__(self):
        self.flow_property_type = None  # type: FlowPropertyType
        self.unit_group = None  # type: UnitGroup


class ImpactMethod(CategorizedEntity):

    def __init__(self):
        self.impact_categories = None  # type: List[ImpactCategory]
        self.parameters = None  # type: List[Parameter]


class Process(CategorizedEntity):

    def __init__(self):
        self.default_allocation_method = None  # type: AllocationType
        self.allocation_factors = None  # type: List[AllocationFactor]
        self.exchanges = None  # type: List[Exchange]
        self.location = None  # type: Location
        self.parameters = None  # type: List[Parameter]
        self.process_documentation = None  # type: ProcessDocumentation
        self.process_type = None  # type: ProcessType


class ProductSystem(CategorizedEntity):

    def __init__(self):
        self.processes = None  # type: List[Process]
        self.reference_process = None  # type: Process
        self.reference_exchange = None  # type: Exchange
        self.target_amount = None  # type: float
        self.target_unit = None  # type: Unit
        self.target_flow_property = None  # type: FlowProperty
        self.process_links = None  # type: List[ProcessLink]


class SocialIndicator(CategorizedEntity):

    def __init__(self):
        self.activity_variable = None  # type: str
        self.activity_quantity = None  # type: FlowProperty
        self.activity_unit = None  # type: Unit
        self.unit_of_measurement = None  # type: str
        self.evaluation_scheme = None  # type: str


class Source(CategorizedEntity):

    def __init__(self):
        self.doi = None  # type: str
        self.text_reference = None  # type: str
        self.year = None  # type: int
        self.external_file = None  # type: str


class UnitGroup(CategorizedEntity):

    def __init__(self):
        self.default_flow_property = None  # type: FlowProperty
        self.units = None  # type: List[Unit]


