import logging as log
import olca_schema as schema
import olca_schema.results as res
import time
import typing

from dataclasses import dataclass
from typing import List, Optional

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

    def get_tech_flows(self) -> List[res.TechFlow]:
        (data, err) = self.client.rpc_call(
            'result/tech-flows', {'@id': self.uid})
        if err:
            log.error('failed to query /tech-flows: %s', err)
            return []
        return [res.TechFlow.from_dict(d) for d in data]

    def get_envi_flows(self) -> List[res.EnviFlow]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/envi-flows', args)
        if err:
            log.error('request envi-flows failed: %s', err)
            return []
        return [res.EnviFlow.from_dict(d) for d in r]

    def get_impact_categories(self) -> List[schema.Ref]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/impact-categories', args)
        if err:
            log.error('request impact-categories failed: %s', err)
            return []
        return [schema.Ref.from_dict(d) for d in r]

    def get_total_requirements(self) -> List[res.TechFlowValue]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/total-requirements', args)
        if err:
            log.error('request total-requirements failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_requirements_of(self, tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-requirements-of', args)
        if err:
            log.error('request total-requirements-of failed: %s', err)
            return 0
        return r

    def get_total_flows(self) -> List[res.EnviFlowValue]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/total-flows', args)
        if err:
            log.error('request total-flows failed: %s', err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_flow_value_of(self, envi_flow: res.EnviFlow) -> float:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-flow-value-of', args)
        if err:
            log.error('request total-flow-value-of failed: %s', err)
            return 0
        return r
