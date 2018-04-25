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
        if product_exchange is not None:
        if allocation_type is not None:
        if value is not None:
        if allocated_exchange is not None:

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
        if internal_id is not None:
        if avoided_product is not None:
        if flow is not None:
        if flow_property is not None:
        if input is not None:
        if quantitative_reference is not None:
        if base_uncertainty is not None:
        if provider is not None:
        if amount is not None:
        if amount_formula is not None:
        if unit is not None:
        if pedigree_uncertainty is not None:
        if uncertainty is not None:
        if comment is not None:

class FlowPropertyFactor(Entity):

    def __init__(self):
        self.flow_property = None  # type: FlowProperty
        self.conversion_factor = None  # type: float
        self.reference_flow_property = None  # type: bool

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if flow_property is not None:
        if conversion_factor is not None:
        if reference_flow_property is not None:

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
        if flow is not None:
        if flow_property is not None:
        if unit is not None:
        if value is not None:
        if formula is not None:
        if uncertainty is not None:

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
        if name is not None:
        if description is not None:
        if parameter_scope is not None:
        if input_parameter is not None:
        if value is not None:
        if formula is not None:
        if external_source is not None:
        if source_type is not None:
        if uncertainty is not None:

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
        if time_description is not None:
        if valid_until is not None:
        if valid_from is not None:
        if technology_description is not None:
        if data_collection_description is not None:
        if completeness_description is not None:
        if data_selection_description is not None:
        if review_details is not None:
        if data_treatment_description is not None:
        if inventory_method_description is not None:
        if modeling_constants_description is not None:
        if reviewer is not None:
        if sampling_description is not None:
        if sources is not None:
        if restrictions_description is not None:
        if copyright is not None:
        if creation_date is not None:
        if data_documentor is not None:
        if data_generator is not None:
        if data_set_owner is not None:
        if intended_application is not None:
        if project_description is not None:
        if publication is not None:
        if geography_description is not None:

class ProcessLink(Entity):

    def __init__(self):
        self.provider = None  # type: Process
        self.flow = None  # type: Flow
        self.process = None  # type: Process
        self.exchange = None  # type: Exchange

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if provider is not None:
        if flow is not None:
        if process is not None:
        if exchange is not None:

class RootEntity(Entity):

    def __init__(self):
        self.name = None  # type: str
        self.description = None  # type: str
        self.version = None  # type: str
        self.last_change = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if name is not None:
        if description is not None:
        if version is not None:
        if last_change is not None:

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
        if distribution_type is not None:
        if mean is not None:
        if mean_formula is not None:
        if geom_mean is not None:
        if geom_mean_formula is not None:
        if minimum is not None:
        if minimum_formula is not None:
        if sd is not None:
        if sd_formula is not None:
        if geom_sd is not None:
        if geom_sd_formula is not None:
        if mode is not None:
        if mode_formula is not None:
        if maximum is not None:
        if maximum_formula is not None:

class CategorizedEntity(RootEntity):

    def __init__(self):
        self.category = None  # type: Category

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if category is not None:

class ImpactCategory(RootEntity):

    def __init__(self):
        self.reference_unit_name = None  # type: str
        self.impact_factors = None  # type: List[ImpactFactor]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if reference_unit_name is not None:
        if impact_factors is not None:

class Location(RootEntity):

    def __init__(self):
        self.code = None  # type: str
        self.latitude = None  # type: float
        self.longitude = None  # type: float
        self.kml = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if code is not None:
        if latitude is not None:
        if longitude is not None:
        if kml is not None:

class Unit(RootEntity):

    def __init__(self):
        self.conversion_factor = None  # type: float
        self.reference_unit = None  # type: bool
        self.synonyms = None  # type: List[string]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if conversion_factor is not None:
        if reference_unit is not None:
        if synonyms is not None:

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
        if address is not None:
        if city is not None:
        if country is not None:
        if email is not None:
        if telefax is not None:
        if telephone is not None:
        if website is not None:
        if zip_code is not None:

class Category(CategorizedEntity):

    def __init__(self):
        self.model_type = None  # type: ModelType

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if model_type is not None:

class Flow(CategorizedEntity):

    def __init__(self):
        self.flow_type = None  # type: FlowType
        self.cas = None  # type: str
        self.formula = None  # type: str
        self.flow_properties = None  # type: List[FlowPropertyFactor]
        self.location = None  # type: Location

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if flow_type is not None:
        if cas is not None:
        if formula is not None:
        if flow_properties is not None:
        if location is not None:

class FlowProperty(CategorizedEntity):

    def __init__(self):
        self.flow_property_type = None  # type: FlowPropertyType
        self.unit_group = None  # type: UnitGroup

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if flow_property_type is not None:
        if unit_group is not None:

class ImpactMethod(CategorizedEntity):

    def __init__(self):
        self.impact_categories = None  # type: List[ImpactCategory]
        self.parameters = None  # type: List[Parameter]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if impact_categories is not None:
        if parameters is not None:

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
        if default_allocation_method is not None:
        if allocation_factors is not None:
        if exchanges is not None:
        if location is not None:
        if parameters is not None:
        if process_documentation is not None:
        if process_type is not None:

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
        if processes is not None:
        if reference_process is not None:
        if reference_exchange is not None:
        if target_amount is not None:
        if target_unit is not None:
        if target_flow_property is not None:
        if process_links is not None:

class SocialIndicator(CategorizedEntity):

    def __init__(self):
        self.activity_variable = None  # type: str
        self.activity_quantity = None  # type: FlowProperty
        self.activity_unit = None  # type: Unit
        self.unit_of_measurement = None  # type: str
        self.evaluation_scheme = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if activity_variable is not None:
        if activity_quantity is not None:
        if activity_unit is not None:
        if unit_of_measurement is not None:
        if evaluation_scheme is not None:

class Source(CategorizedEntity):

    def __init__(self):
        self.doi = None  # type: str
        self.text_reference = None  # type: str
        self.year = None  # type: int
        self.external_file = None  # type: str

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if doi is not None:
        if text_reference is not None:
        if year is not None:
        if external_file is not None:

class UnitGroup(CategorizedEntity):

    def __init__(self):
        self.default_flow_property = None  # type: FlowProperty
        self.units = None  # type: List[Unit]

    def to_json(self) -> dict:
        jdict = super.to_json()  # type: dict
        if default_flow_property is not None:
        if units is not None:

