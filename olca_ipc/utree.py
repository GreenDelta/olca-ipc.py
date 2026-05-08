import olca_schema as o
from .protocol import ProtoResult

from typing import Literal, cast

_Ref = o.Ref | o.EnviFlow | Literal["costs"]


class Node:
    def __init__(
        self,
        result: ProtoResult,
        ref: _Ref,
        node: o.UpstreamNode,
        path: list[o.TechFlow],
    ):
        self._result = result
        self._ref = ref
        self._node = node
        self._path = path
        self._childs: list["Node"] | None = None

    @property
    def result(self) -> float:
        return cast(float, self._node.result)

    @property
    def provider(self) -> o.Ref:
        return cast(o.Ref, self._node.tech_flow.provider)

    @property
    def product(self) -> o.Ref:
        return cast(o.Ref, self._node.tech_flow.flow)

    @property
    def direct_contribution(self) -> float:
        return cast(float, self._node.direct_contribution)

    @property
    def required_amount(self) -> float:
        return cast(float, self._node.required_amount)

    @property
    def childs(self) -> list["Node"]:
        if self._childs is not None:
            return self._childs
        self._childs = []
        ref = self._ref
        for u in _fetch_next(self._result, ref, self._path):
            self._childs.append(
                Node(
                    self._result,
                    ref,
                    u,
                    self._path + [cast(o.TechFlow, u.tech_flow)],
                )
            )
        return self._childs


def of(result: ProtoResult, ref: _Ref) -> Node:
    [root] = _fetch_next(result, ref, [])
    return Node(result, ref, root, [cast(o.TechFlow, root.tech_flow)])


def _fetch_next(
    result: ProtoResult, ref: _Ref, path: list[o.TechFlow]
) -> list[o.UpstreamNode]:
    if ref == "costs":
        return result.get_upstream_costs_of(path)
    if isinstance(ref, o.EnviFlow):
        return result.get_upstream_interventions_of(ref, path)
    if isinstance(ref, o.Ref):
        return result.get_upstream_impacts_of(ref, path)
    raise ValueError("unsupported reference type for upstream results: " + ref)
