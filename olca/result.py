import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from .ipc import Client


@dataclass
class Result:
    uid: str
    client: 'Client'
