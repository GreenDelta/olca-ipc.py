# This module contains a Python API of the JSON-LD based
# openLCA data exchange model.package schema.
# For more information see http://greendelta.github.io/olca-schema/


class Entity(object):

    def __init__(self):
        pass


class AllocationFactor(Entity):

    def __init__(self):
        self.product_exchange = None  # type: Exchange
        self.allocation_type = None  # type: AllocationType
        self.value = None  # type: double
        self.allocated_exchange = None  # type: Exchange


class Exchange(Entity):

    def __init__(self):
        self.internal_id = None  # type: int
        self.avoided_product = None  # type: boolean
        self.flow = None  # type: Flow
        self.flow_property = None  # type: FlowProperty
        self.input = None  # type: boolean
        self.quantitative_reference = None  # type: boolean
        self.base_uncertainty = None  # type: double
        self.provider = None  # type: Process
        self.amount = None  # type: double
        self.amount_formula = None  # type: string
        self.unit = None  # type: Unit
        self.pedigree_uncertainty = None  # type: string
        self.uncertainty = None  # type: Uncertainty
        self.comment = None  # type: string


class FlowPropertyFactor(Entity):

    def __init__(self):
        self.flow_property = None  # type: FlowProperty
        self.conversion_factor = None  # type: double
        self.reference_flow_property = None  # type: boolean


class ImpactFactor(Entity):

    def __init__(self):
        self.flow = None  # type: Flow
        self.flow_property = None  # type: FlowProperty
        self.unit = None  # type: Unit
        self.value = None  # type: double
        self.formula = None  # type: string
        self.uncertainty = None  # type: Uncertainty


class Parameter(Entity):

    def __init__(self):
        self.name = None  # type: string
        self.description = None  # type: string
        self.parameter_scope = None  # type: ParameterScope
        self.input_parameter = None  # type: boolean
        self.value = None  # type: double
        self.formula = None  # type: string
        self.external_source = None  # type: string
        self.source_type = None  # type: string
        self.uncertainty = None  # type: Uncertainty


class ProcessDocumentation(Entity):

    def __init__(self):
        self.time_description = None  # type: string
        self.valid_until = None  # type: date
        self.valid_from = None  # type: date
        self.technology_description = None  # type: string
        self.data_collection_description = None  # type: string
        self.completeness_description = None  # type: string
        self.data_selection_description = None  # type: string
        self.review_details = None  # type: string
        self.data_treatment_description = None  # type: string
        self.inventory_method_description = None  # type: string
        self.modeling_constants_description = None  # type: string
        self.reviewer = None  # type: Actor
        self.sampling_description = None  # type: string
        self.sources = None  # type: List[Source]
        self.restrictions_description = None  # type: string
        self.copyright = None  # type: boolean
        self.creation_date = None  # type: dateTime
        self.data_documentor = None  # type: Actor
        self.data_generator = None  # type: Actor
        self.data_set_owner = None  # type: Actor
        self.intended_application = None  # type: string
        self.project_description = None  # type: string
        self.publication = None  # type: Source
        self.geography_description = None  # type: string


class ProcessLink(Entity):

    def __init__(self):
        self.provider = None  # type: Process
        self.flow = None  # type: Flow
        self.process = None  # type: Process
        self.exchange = None  # type: Exchange


class RootEntity(Entity):

    def __init__(self):
        self.name = None  # type: string
        self.description = None  # type: string
        self.version = None  # type: string
        self.last_change = None  # type: dateTime


class Uncertainty(Entity):

    def __init__(self):
        self.distribution_type = None  # type: UncertaintyType
        self.mean = None  # type: double
        self.mean_formula = None  # type: string
        self.geom_mean = None  # type: double
        self.geom_mean_formula = None  # type: string
        self.minimum = None  # type: double
        self.minimum_formula = None  # type: string
        self.sd = None  # type: double
        self.sd_formula = None  # type: string
        self.geom_sd = None  # type: double
        self.geom_sd_formula = None  # type: string
        self.mode = None  # type: double
        self.mode_formula = None  # type: string
        self.maximum = None  # type: double
        self.maximum_formula = None  # type: string


class CategorizedEntity(RootEntity):

    def __init__(self):
        self.category = None  # type: Category


class ImpactCategory(RootEntity):

    def __init__(self):
        self.reference_unit_name = None  # type: string
        self.impact_factors = None  # type: List[ImpactFactor]


class Location(RootEntity):

    def __init__(self):
        self.code = None  # type: string
        self.latitude = None  # type: double
        self.longitude = None  # type: double
        self.kml = None  # type: string


class Unit(RootEntity):

    def __init__(self):
        self.conversion_factor = None  # type: double
        self.reference_unit = None  # type: boolean
        self.synonyms = None  # type: List[string]


class Actor(CategorizedEntity):

    def __init__(self):
        self.address = None  # type: string
        self.city = None  # type: string
        self.country = None  # type: string
        self.email = None  # type: string
        self.telefax = None  # type: string
        self.telephone = None  # type: string
        self.website = None  # type: string
        self.zip_code = None  # type: string


class Category(CategorizedEntity):

    def __init__(self):
        self.model_type = None  # type: ModelType


class Flow(CategorizedEntity):

    def __init__(self):
        self.flow_type = None  # type: FlowType
        self.cas = None  # type: string
        self.formula = None  # type: string
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
        self.target_amount = None  # type: double
        self.target_unit = None  # type: Unit
        self.target_flow_property = None  # type: FlowProperty
        self.process_links = None  # type: List[ProcessLink]


class SocialIndicator(CategorizedEntity):

    def __init__(self):
        self.activity_variable = None  # type: string
        self.activity_quantity = None  # type: FlowProperty
        self.activity_unit = None  # type: Unit
        self.unit_of_measurement = None  # type: string
        self.evaluation_scheme = None  # type: string


class Source(CategorizedEntity):

    def __init__(self):
        self.doi = None  # type: string
        self.text_reference = None  # type: string
        self.year = None  # type: integer
        self.external_file = None  # type: string


class UnitGroup(CategorizedEntity):

    def __init__(self):
        self.default_flow_property = None  # type: FlowProperty
        self.units = None  # type: List[Unit]
