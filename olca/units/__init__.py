import csv
import os.path as path

from typing import Optional

import olca

_unit_refs = None
_group_refs = None
_prop_refs = None


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
            _unit_refs[unit] = olca.ref(olca.Unit, row[1], unit)
            _group_refs[unit] = olca.ref(olca.UnitGroup, row[3], row[2])
            _prop_refs[unit] = olca.ref(olca.FlowProperty, row[5], row[4])


def unit_ref(symbol: str) -> Optional[olca.Ref]:
    """Get the unit reference (an instance of olca.Ref) for the given unit
       symbol (a string like 'kg'). Returns `None` if the given unit is
       unknown."""
    if _unit_refs is None:
        _init()
    return _unit_refs.get(symbol)


def group_ref(symbol: str) -> Optional[olca.Ref]:
    """Get the unit group reference (an instance of olca.Ref) for the given
       unit symbol (a string like 'kg'). Returns `None` if the given unit is
       unknown."""
    if _group_refs is None:
        _init()
    return _group_refs.get(symbol)


def property_ref(symbol: str) -> Optional[olca.Ref]:
    """Get the reference (an instance of olca.Ref) to the default flow property
       (quantity) for the given unit symbol (a string like 'kg'). Returns
       `None` if the given unit is unknown."""
    if _prop_refs is None:
        _init()
    return _prop_refs.get(symbol)
