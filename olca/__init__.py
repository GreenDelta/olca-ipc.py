import datetime
import uuid

from .ipc import *
from .schema import *

from typing import Optional, TypeVar, Union

T = TypeVar('T')


def ref(model_type: T, id: str, name: Optional[str] = None) -> Ref:
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

    model_type: T
        The class of the model type of the reference, e.g. olca.Flow

    id: str
        The ID (UUID) of the model / data set this reference points to.

    name: Optional[str]
        The name of the model / data set this reference points to.

    Example
    -------
    ```
    mass_ref = olca.ref(
        olca.FlowProperty,
        '93a60a56-a3c8-11da-a746-0800200b9a66',
        'Mass')
    ```
    """
    r = Ref()
    r.olca_type = model_type.__name__
    r.id = id
    if name is not None:
        r.name = name
    return r


def unit_of(name='', conversion_factor=1.0) -> Unit:
    """
    Creates a new unit with the given name.

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

    ```py
    import olca
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
    Creates a new unit group with the given name and reference unit.

    Parameters
    ----------
    name: str
        The name of the new unit group.

    unit: Union[str, Unit]
        The reference unit or the name of the reference unit of
        the new unit group.

    Example
    -------
    ```py
    import olca
    units = olca.unit_group_of('Units of mass', 'kg')
    ```
    """
    u: Unit = unit if isinstance(unit, Unit) else unit_of(unit)
    u.reference_unit = True
    group = UnitGroup()
    _set_base_attributes(group, name)
    group.units = [u]
    return group


def _set_base_attributes(entity: RootEntity, name: str):
    entity.id = str(uuid.uuid4())
    entity.name = name
    entity.version = '00.00.000'
    entity.last_change = datetime.datetime.utcnow().isoformat() + 'Z'
