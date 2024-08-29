import olca_schema as o
from .protocol import IpcResult

from typing import Literal

_Ref = o.Ref | o.EnviFlow | Literal["costs"]


class Node:

    def __init__(
        self,
        result: IpcResult,
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
        return self._node.result

    @property
    def provider(self) -> o.Ref:
        return self._node.tech_flow.provider

    @property
    def product(self) -> o.Ref:
        return self._node.tech_flow.flow

    @property
    def direct_contribution(self) -> float:
        return self._node.direct_contribution

    @property
    def required_amount(self) -> float:
        return self._node.required_amount

    @property
    def childs(self) -> list["Node"]:
        if self._childs is not None:
            return self._childs
        self._childs = []
        for u in _fetch_next(self._result, self._ref, self._path):
            self._childs.append(
                Node(self._result, self._ref, u, self._path + [u.tech_flow])
            )
        return self._childs


def of(result: IpcResult, ref: _Ref) -> Node:
    [root] = _fetch_next(result, ref, [])
    return Node(result, ref, root, [root.tech_flow])


def _fetch_next(
    result: IpcResult, ref: _Ref, path: list[o.TechFlow]
) -> list[o.UpstreamNode]:
    if ref == "costs":
        return result.get_upstream_cost_of(path)
    if isinstance(ref, o.EnviFlow):
        return result.get_upstream_interventions_of(ref, path)
    if isinstance(ref, o.Ref):
        return result.get_upstream_impacts_of(ref, path)
    raise ValueError("unsupported reference type for upstream results: " + ref)
