import datetime
import uuid

import olca_schema as lca
from .ipc import *

from typing import Union


def ref_of(entity: Union[lca.RootEntity, lca.Ref]) -> lca.Ref:
    # TODO: we could copy more specific fields here
    if isinstance(entity, lca.Ref):
        return lca.Ref(
            model_type=entity.model_type,
            id=entity.id,
            name=entity.name)
    return lca.Ref(
        model_type=type(entity).__name__,
        id=entity.id,
        name=entity.name)


def new_unit(name: str, conversion_factor=1.0) -> lca.Unit:
    return lca.Unit(
        id=str(uuid.uuid4()),
        name=name,
        conversion_factor=1.0,
        is_ref_unit=conversion_factor == 1.0)


def new_unit_group(name: str, ref_unit: Union[str, lca.Unit]) -> lca.UnitGroup:
    unit: lca.Unit = new_unit(ref_unit) \
        if isinstance(ref_unit, str) else ref_unit
    group = lca.UnitGroup(name=name, units=[unit])
    _set_base_attributes(group)
    return group


def new_flow_property(name: str, unit_group: Union[lca.Ref, lca.UnitGroup]) \
        -> lca.FlowProperty:
    prop = lca.FlowProperty(name=name, unit_group=ref_of(unit_group))
    _set_base_attributes(prop)
    return prop


def new_flow(name: str, flow_type: lca.FlowType,
             flow_property: Union[lca.Ref, lca.FlowProperty]) -> lca.Flow:
    factor = lca.FlowPropertyFactor(
        flow_property=ref_of(flow_property),
        conversion_factor=1.0,
        is_ref_flow_property=True)
    flow = lca.Flow(
        name=name,
        flow_type=flow_type,
        flow_properties=[factor])
    _set_base_attributes(flow)
    return flow


def new_product(name: str, flow_property: Union[lca.Ref, lca.FlowProperty]) \
        -> lca.Flow:
    return new_flow(name, lca.FlowType.PRODUCT_FLOW, flow_property)


def new_waste(name: str, flow_property: Union[lca.Ref, lca.FlowProperty]) \
        -> lca.Flow:
    return new_flow(name, lca.FlowType.WASTE_FLOW, flow_property)


def new_elementary_flow(name: str,
                        flow_property: Union[lca.Ref, lca.FlowProperty]) \
        -> lca.Flow:
    return new_flow(name, lca.FlowType.ELEMENTARY_FLOW, flow_property)


def new_process(name: str) -> lca.Process:
    process = lca.Process(name=name, process_type=lca.ProcessType.UNIT_PROCESS)
    _set_base_attributes(process)
    return process


def new_exchange(process: lca.Process, flow: Union[lca.Ref, lca.Flow],
                 amount: Union[str, float] = 1.0,
                 unit: Optional[Union[lca.Ref, lca.Unit]] = None) \
        -> lca.Exchange:
    if process.last_internal_id is None:
        internal_id = 1
    else:
        internal_id = process.last_internal_id + 1
    process.last_internal_id = internal_id
    exchange = lca.Exchange(
        internal_id=internal_id,
        flow=ref_of(flow))
    if isinstance(amount, str):
        exchange.amount_formula = amount
    else:
        exchange.amount = amount
    if unit:
        exchange.unit = ref_of(unit)
    if process.exchanges is None:
        process.exchanges = [exchange]
    else:
        process.exchanges.append(exchange)
    return exchange


def new_input(process: lca.Process, flow: Union[lca.Ref, lca.Flow],
              amount: Union[str, float] = 1.0,
              unit: Optional[Union[lca.Ref, lca.Unit]] = None) \
        -> lca.Exchange:
    exchange = new_exchange(process, flow, amount, unit)
    exchange.is_input = True
    return exchange


def new_output(process: lca.Process, flow: Union[lca.Ref, lca.Flow],
               amount: Union[str, float] = 1.0,
               unit: Optional[Union[lca.Ref, lca.Unit]] = None) \
        -> lca.Exchange:
    exchange = new_exchange(process, flow, amount, unit)
    exchange.is_input = False
    return exchange


def new_location(name: str, code: Optional[str] = None) -> lca.Location:
    """Creates a new location.

    Parameters
    ----------
    name:
        The name of the new location.
    code:
        An optional location code.
    """
    location = lca.Location(name=name, code=code or name)
    _set_base_attributes(location)
    return location


def _set_base_attributes(entity: lca.RootEntity):
    entity.id = str(uuid.uuid4())
    entity.version = '00.00.000'
    entity.last_change = datetime.datetime.utcnow().isoformat() + 'Z'
