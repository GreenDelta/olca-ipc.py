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

    def get_direct_flow_values_of(self, envi_flow: res.EnviFlow) \
            -> List[res.TechFlowValue]:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-flow-values-of', args)
        if err:
            log.error('request direct-flow-values-of failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_flow_values_of(self, envi_flow: res.EnviFlow) \
            -> List[res.TechFlowValue]:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-flow-values-of', args)
        if err:
            log.error('request total-flow-values-of failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_direct_flows_of(self, tech_flow: res.TechFlow) \
            -> List[res.EnviFlowValue]:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-flows-of', args)
        if err:
            log.error('request direct-flows-of failed: %s', err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_direct_flow_of(self, envi_flow: res.EnviFlow,
                           tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict(),
                'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-flow-of', args)
        if err:
            log.error('request direct-flow-of failed: %s', err)
            return 0
        return r

    def get_total_flows_of_one(self, tech_flow: res.TechFlow) \
            -> List[res.EnviFlowValue]:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-flows-of-one', args)
        if err:
            log.error('request total-flows-of-one failed: %s', err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_flow_of_one(self, envi_flow: res.EnviFlow,
                              tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict(),
                'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-flow-of-one', args)
        if err:
            log.error('request total-flow-of-one failed: %s', err)
            return 0
        return r

    def get_total_flows_of(self, tech_flow: res.TechFlow) \
            -> List[res.EnviFlowValue]:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-flows-of', args)
        if err:
            log.error('request total-flows-of failed: %s', err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_flow_of(self, envi_flow: res.EnviFlow,
                          tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict(),
                'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-flow-of', args)
        if err:
            log.error('request total-flow-of failed: %s', err)
            return 0
        return r

    def get_total_impacts(self) -> List[res.ImpactValue]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/total-impacts', args)
        if err:
            log.error('request total-impacts failed: %s', err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_value_of(self, impact_category: schema.Ref) -> float:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict()}
        (r, err) = self.client.rpc_call('result/total-impact-value-of', args)
        if err:
            log.error('request total-impact-value-of failed: %s', err)
            return 0
        return r

    def get_direct_impact_values_of(self, impact_category: schema.Ref) \
            -> List[res.TechFlowValue]:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-impact-values-of', args)
        if err:
            log.error('request direct-impact-values-of failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_impact_values_of(self, impact_category: schema.Ref) \
            -> List[res.TechFlowValue]:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict()}
        (r, err) = self.client.rpc_call('result/total-impact-values-of', args)
        if err:
            log.error('request total-impact-values-of failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_direct_impacts_of(self, tech_flow: res.TechFlow) \
            -> List[res.ImpactValue]:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-impacts-of', args)
        if err:
            log.error('request direct-impacts-of failed: %s', err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_direct_impact_of(self, impact_category: schema.Ref,
                             tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict(),
                'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-impact-of', args)
        if err:
            log.error('request direct-impact-of failed: %s', err)
            return 0
        return r

    def get_total_impacts_of_one(self, tech_flow: res.TechFlow) \
            -> List[res.ImpactValue]:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-impacts-of-one', args)
        if err:
            log.error('request total-impacts-of-one failed: %s', err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_of_one(self, impact_category: schema.Ref,
                                tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict(),
                'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-impact-of-one', args)
        if err:
            log.error('request total-impact-of-one failed: %s', err)
            return 0
        return r

    def get_total_impacts_of(self, tech_flow: res.TechFlow) \
            -> List[res.ImpactValue]:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-impacts-of', args)
        if err:
            log.error('request total-impacts-of failed: %s', err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_of(self, impact_category: schema.Ref,
                            tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict(),
                'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-impact-of', args)
        if err:
            log.error('request total-impact-of failed: %s', err)
            return 0
        return r

    def get_impact_factors_of(self, impact_category: schema.Ref) \
            -> List[res.EnviFlowValue]:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict()}
        (r, err) = self.client.rpc_call('result/impact-factors-of', args)
        if err:
            log.error('request impact-factors-of failed: %s', err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_impact_factor_of(self, impact_category: schema.Ref,
                             envi_flow: res.EnviFlow) -> float:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict(),
                'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/impact-factor-of', args)
        if err:
            log.error('request impact-factor-of failed: %s', err)
            return 0
        return r

    def get_flow_impacts_of_one(self, envi_flow: res.EnviFlow) \
            -> List[res.ImpactValue]:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/flow-impacts-of-one', args)
        if err:
            log.error('request flow-impacts-of-one failed: %s', err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_flow_impacts_of(self, envi_flow: res.EnviFlow) \
            -> List[res.ImpactValue]:
        args = {'@id': self.uid, 'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/flow-impacts-of', args)
        if err:
            log.error('request flow-impacts-of failed: %s', err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_flow_impact_of(self, impact_category: schema.Ref,
                           envi_flow: res.EnviFlow) -> float:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict(),
                'enviFlow': envi_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/flow-impact-of', args)
        if err:
            log.error('request flow-impact-of failed: %s', err)
            return 0
        return 0

    def get_flow_impact_values_of(self, impact_category: schema.Ref) \
            -> List[res.EnviFlowValue]:
        args = {'@id': self.uid, 'impactCategory': impact_category.to_dict()}
        (r, err) = self.client.rpc_call('result/flow-impact-values-of', args)
        if err:
            log.error('request flow-impact-values-of failed: %s', err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_costs(self) -> float:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/total-costs', args)
        if err:
            log.error('request total-costs failed: %s', err)
            return 0
        return r

    def get_direct_cost_values(self) -> List[res.TechFlowValue]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/direct-cost-values', args)
        if err:
            log.error('request direct-cost-values failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_cost_values(self) -> List[res.TechFlowValue]:
        args = {'@id': self.uid}
        (r, err) = self.client.rpc_call('result/total-cost-values', args)
        if err:
            log.error('request total-cost-values failed: %s', err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_direct_costs_of(self, tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/direct-costs-of', args)
        if err:
            log.error('request direct-costs-of failed: %s', err)
            return 0
        return r

    def get_total_costs_of_one(self, tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-costs-of-one', args)
        if err:
            log.error('request total-costs-of-one failed: %s', err)
            return 0
        return r

    def get_total_costs_of(self, tech_flow: res.TechFlow) -> float:
        args = {'@id': self.uid, 'techFlow': tech_flow.to_dict()}
        (r, err) = self.client.rpc_call('result/total-costs-of', args)
        if err:
            log.error('request total-costs-of failed: %s', err)
            return 0
        return r
