from .ipc import *
from .schema import *


def ref(model_type, id: str, name=None) -> Ref:
    r = Ref()
    r.olca_type = model_type.__name__
    r.id = id
    if name is not None:
        r.name = name
    return r
