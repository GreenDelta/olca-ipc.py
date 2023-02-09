from dataclasses import dataclass
from typing import Optional

import olca_schema as o
from .protocol import IpcResult


class UpstreamTree:
    def __init__(
        self,
        result: IpcResult,
        envi_flow: o.EnviFlow | None = None,
        impact_category: o.Ref | None = None,
        is_for_costs: bool = False,
    ):
        self.result = result
        self.envi_flow = envi_flow
        self.impact_category = impact_category
        self.is_for_costs = is_for_costs

    def _make_root(self) -> Optional["UpstreamNode"]:
        r = self.result
        d = r.get_demand()
        if d is None:
            return None
        tech_values = r.get_unscaled_tech_flows_of(d.tech_flow)
        qref = next(
            filter(lambda ti: _eq(ti.tech_flow, d.tech_flow), tech_values),
            None,
        )
        if qref is None:
            return None
        s = d.amount / qref.amount
        i = self._intensity_of(d.tech_flow)
        r = d.amount * i



    def _intensity_of(self, provider: o.TechFlow) -> float:
        def _v(v: o.EnviFlowValue | o.ImpactValue | o.CostValue| None) -> float:
            if v is None or v.amount is None:
                return 0
            return v.amount
        if self.envi_flow is not None:
            return _v(self.result.get_flow_intensity_of(self.envi_flow, provider))
        if self.impact_category is not None:
            return _v(self.result.get_impact_intensity_of(self.impact_category, provider))
        if self.is_for_costs:
            return _v(self.result.get_cost_intensities_of(provider))
        return 0


@dataclass
class UpstreamNode:
    tree: UpstreamTree
    provider: o.TechFlow
    scaling: float




def _eq(t1: o.TechFlow | None, t2: o.TechFlow | None) -> bool:
    return (
        t1 is not None
        and t2 is not None
        and t1.provider is not None
        and t2.provider is not None
        and t1.provider.id == t2.provider.id
        and t1.flow is not None
        and t2.flow is not None
        and t1.flow.id == t2.flow.id
    )
