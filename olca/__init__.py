from .ipc import *
from .schema import *

from typing import Optional, TypeVar

T = TypeVar('T')


def ref(model_type: T, id: str, name: Optional[str] = None) -> Ref:
    """
    Creates a new reference object for the given type and ID.

    In the openLCA data format, references are used to point to another
    data set. A references must have a type and an ID. Other attributes like
    name, description etc. are optional but often useful when inspecting a
    data set.

    Parameters
    ----------

    model_type: T
        The class of the model type of the reference, e.g. olca.schema.Flow

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
