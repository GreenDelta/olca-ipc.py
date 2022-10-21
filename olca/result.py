import olca_schema.results as res
import time
import typing

from dataclasses import dataclass
from typing import Optional

if typing.TYPE_CHECKING:
    from .ipc import Client


@dataclass
class Result:
    uid: str
    client: 'Client'
    error: Optional[res.ResultState]

    def get_state(self) -> res.ResultState:
        if self.error is not None:
            return self.error
        (state, err) = self.client.rpc_call('result/state', {'@id': self.uid})
        if err:
            return res.ResultState(id=self.uid, error=err)
        return res.ResultState.from_dict(state)

    def wait_until_ready(self) -> res.ResultState:
        state = self.get_state()
        if state.error:
            return state
        while state.is_scheduled:
            time.sleep(0.5)
            state = self.get_state()
            if not state.is_scheduled:
                return state

    def dispose(self):
        if self.error is not None:
            return
        self.client.rpc_call('result/dispose', {'@id': self.uid})
