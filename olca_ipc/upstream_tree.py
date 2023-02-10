from dataclasses import dataclass

import olca_schema as o
from .protocol import IpcResult


_vec = dict[str, float]


class UpstreamTree:
    def __init__(
        self,
        result: IpcResult,
        envi_flow: o.EnviFlow | None = None,
        impact_category: o.Ref | None = None,
        is_for_costs: bool = False,
    ):
        self.result = result

        if envi_flow is not None:
            self._envi_flow = envi_flow
            cons = result.get_flow_contributions_of(envi_flow)
        elif impact_category is not None:
            self._impact_category = impact_category
            cons = result.get_impact_contributions_of(impact_category)
        elif is_for_costs:
            self._is_for_costs = is_for_costs
            cons = result.get_cost_contributions()
        else:
            raise AssertionError(
                "an intervention flow, impact "
                + "category, cost flag must be provided"
            )

        (self._diag, self._direct) = _unscaled_vecs(result, cons)
        d = result.get_demand()
        self.root = self._node_of(d.tech_flow, d.amount)

    def _node_of(self, provider: o.TechFlow, required_amount: float):
        key = _key(provider)
        diag_j = self._diag.get(key, 0.0)
        if required_amount == 0 or diag_j == 0:
            return UpstreamNode(
                tree=self,
                provider=provider,
                required_amount=0,
                total=0,
                direct=0,
                scaling=0,
            )
        ij = self._intensity_of(provider)
        sj = required_amount / diag_j
        direct = sj * self._direct.get(key, 0)
        return UpstreamNode(
            tree=self,
            provider=provider,
            required_amount=required_amount,
            total=ij * required_amount,
            direct=direct,
            scaling=sj,
        )

    def _intensity_of(self, provider: o.TechFlow) -> float:
        def _v(
            v: o.EnviFlowValue | o.ImpactValue | o.CostValue | None,
        ) -> float:
            if v is None or v.amount is None:
                return 0
            return v.amount

        if self._envi_flow is not None:
            return _v(
                self.result.get_flow_intensity_of(self._envi_flow, provider)
            )
        if self._impact_category is not None:
            return _v(
                self.result.get_impact_intensity_of(
                    self._impact_category, provider
                )
            )
        if self._is_for_costs:
            return _v(self.result.get_cost_intensities_of(provider))
        return 0


@dataclass
class UpstreamNode:
    tree: UpstreamTree
    provider: o.TechFlow
    scaling: float
    required_amount: float
    total: float
    direct: float
    _childs: list["UpstreamNode"] | None = None

    @property
    def childs(self) -> list["UpstreamNode"]:
        if self._childs is not None:
            return self._childs
        childs = []
        for ai in self.tree.result.get_unscaled_tech_flows_of(self.provider):
            if (
                ai.tech_flow is None
                or _eq(ai.tech_flow, self.provider)
                or ai.amount is None
                or ai.amount == 0
            ):
                continue
            val = -self.scaling * ai.amount
            childs.append(self.tree._node_of(ai.tech_flow, val))
        self._childs = childs
        return childs


def _unscaled_vecs(
    result: IpcResult, cons: list[o.TechFlowValue]
) -> tuple[_vec, _vec]:
    s: _vec = {}
    t: _vec = {}
    d: _vec = {}
    for sf in result.get_scaling_factors():
        s[_key(sf.tech_flow)] = sf.amount or 0
    for ti in result.get_total_requirements():
        t[_key(ti.tech_flow)] = ti.amount or 0
    for ci in cons:
        d[_key(ci.tech_flow)] = ci.amount or 0

    diag: _vec = {}
    direct: _vec = {}
    for (key, ti) in t.items():
        si = s.get(key, 0.0)
        di = d.get(key, 0.0)
        if si == 0 or ti == 0:
            diag[key] = 0
        else:
            diag[key] = ti / si
            direct[key] = di / si
    return (diag, direct)


def _key(tech_flow: o.TechFlow | None) -> str:
    if (
        tech_flow is None
        or tech_flow.provider is None
        or tech_flow.flow is None
    ):
        return ""
    return f"{tech_flow.provider.id}/{tech_flow.flow.id}"


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
