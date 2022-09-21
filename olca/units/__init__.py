import csv
import os.path as path
from typing import Dict, Optional

import olca_schema as schema

_unit_refs: Optional[Dict[str, schema.Ref]] = None
_group_refs: Optional[Dict[str, schema.Ref]] = None
_prop_refs: Optional[Dict[str, schema.Ref]] = None


def _init():
    global _unit_refs, _group_refs, _prop_refs
    _unit_refs = {}
    _group_refs = {}
    _prop_refs = {}

    fpath = path.join(path.dirname(__file__), 'units.csv')
    with open(fpath, 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            unit = row[0]
            _unit_refs[unit] = schema.Ref(
                model_type='Unit', id=row[1], name=unit)
            _group_refs[unit] = schema.Ref(
                model_type='UnitGroup', id=row[3], name=row[2])
            _prop_refs[unit] = schema.Ref(
                model_type='FlowProperty', id=row[5], name=row[4])


def unit_ref(symbol: str) -> Optional[schema.Ref]:
    """Get the unit reference (an instance of olca.Ref) for the given unit
       symbol (a string like 'kg'). Returns `None` if the given unit is
       unknown."""
    if _unit_refs is None:
        _init()
    return _unit_refs.get(symbol)


def group_ref(symbol: str) -> Optional[schema.Ref]:
    """Get the unit group reference (an instance of olca.Ref) for the given
       unit symbol (a string like 'kg'). Returns `None` if the given unit is
       unknown."""
    if _group_refs is None:
        _init()
    return _group_refs.get(symbol)


def property_ref(symbol: str) -> Optional[schema.Ref]:
    """Get the reference (an instance of olca.Ref) to the default flow property
       (quantity) for the given unit symbol (a string like 'kg'). Returns
       `None` if the given unit is unknown."""
    if _prop_refs is None:
        _init()
    return _prop_refs.get(symbol)
