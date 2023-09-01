import logging as log
from dataclasses import dataclass
from typing import cast, Any, Callable, Optional, Tuple, Type, TypeVar

import requests
import olca_schema as o

from .protocol import E, IpcProtocol, IpcResult

_T = TypeVar("_T")


class Client(IpcProtocol):
    """
    A client to communicate with an openLCA IPC server over the JSON-RPC
    protocol.
    """

    def __init__(self, endpoint: str | int = 8080):
        self.url: str
        if isinstance(endpoint, str):
            self.url = endpoint
        else:
            self.url = "http://localhost:%i" % endpoint
        self.next_id = 1
        self._s = requests.Session()

    def get(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> E | None:
        if not uid and not name:
            log.error("no ID or name given")
            return None
        params = {"@type": model_type.__name__}
        if uid is not None:
            params["@id"] = uid
        if name is not None:
            params["name"] = name
        result, err = self.rpc_call("data/get", params)
        if err:
            log.warning("failed to get entity of type %s: %s", model_type, err)
            return None
        return cast(E, model_type.from_dict(result))

    def get_all(self, model_type: Type[E]) -> list[E]:
        params = {"@type": model_type.__name__}
        result, err = self.rpc_call("data/get/all", params)
        if err:
            log.error("failed to get all of type %s: %s", model_type, err)
        return cast(list[E], [model_type.from_dict(r) for r in result])

    def get_descriptors(self, model_type: Type[E]) -> list[o.Ref]:
        params = {"@type": model_type.__name__}
        result, err = self.rpc_call("data/get/descriptors", params)
        if err:
            log.error(
                "failed to get descriptors of type %s: %s", model_type, err
            )
            return []
        return [o.Ref.from_dict(r) for r in result]

    def get_descriptor(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> o.Ref | None:
        params = {"@type": model_type.__name__}
        if uid is not None:
            params["@id"] = uid
        if name is not None:
            params["name"] = name
        result, err = self.rpc_call("data/get/descriptor", params)
        if err:
            log.error("failed to get descriptor: %s", err)
            return None
        return o.Ref.from_dict(result)

    def get_providers(
        self, flow: o.Ref | o.Flow | None = None
    ) -> list[o.TechFlow]:
        if flow is None:
            params = {}
        else:
            params = {
                "@type": "Flow",
                "@id": flow.id,
                "name": flow.name,
            }
        providers, err = self.rpc_call("data/get/providers", params)
        if err:
            log.error("failed to get providers: %s", err)
            return []
        return [o.TechFlow.from_dict(d) for d in providers]

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[o.Parameter | o.ParameterRedef]:
        params = {"@type": model_type.__name__, "@id": uid}
        params, err = self.rpc_call("data/get/parameters", params)
        if err:
            log.error("failed to get parameters of %s id=%d", model_type, uid)
            return []
        if model_type in (o.Process, o.ImpactCategory):
            return [o.Parameter.from_dict(p) for p in params]
        else:
            return [o.ParameterRedef.from_dict(p) for p in params]

    def put(self, model: o.RootEntity) -> o.Ref | None:
        if model is None:
            return None
        resp, err = self.rpc_call("data/put", model.to_dict())
        if err:
            log.error("failed to insert model: %s", err)
            return None
        return o.Ref.from_dict(resp)

    def create_product_system(
        self,
        process: o.Ref | o.Process,
        config: o.LinkingConfig | None = None,
    ) -> o.Ref | None:
        conf = config
        if conf is None:
            conf = o.LinkingConfig(
                prefer_unit_processes=False,
                provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
            )
        r, err = self.rpc_call(
            "data/create/system",
            {
                "process": o.as_ref(process).to_dict(),
                "config": conf.to_dict(),
            },
        )
        if err:
            log.error("failed to create product system: %s", err)
            return None
        return o.Ref.from_dict(r)

    def delete(self, model: o.RootEntity | o.Ref) -> o.Ref | None:
        if model is None:
            return
        ref = o.as_ref(model).to_dict()
        resp, err = self.rpc_call("data/delete", ref)
        if err:
            log.error("failed to delete model: %s", err)
            return None
        return o.Ref.from_dict(resp)

    def calculate(self, setup: o.CalculationSetup) -> "Result":
        resp, err = self.rpc_call("result/calculate", setup.to_dict())
        if err:
            return Result(
                uid="", client=self, error=o.ResultState(id="", error=err)
            )
        state = o.ResultState.from_dict(resp)
        return Result(uid=state.id, client=self, error=None)

    def simulate(self, setup: o.CalculationSetup) -> "Result":
        resp, err = self.rpc_call("result/simulate", setup.to_dict())
        if err:
            return Result(
                uid="", client=self, error=o.ResultState(id="", error=err)
            )
        state = o.ResultState.from_dict(resp)
        return Result(uid=state.id, client=self, error=None)

    def rpc_call(
        self, method: str, params: Any = None
    ) -> Tuple[Any, Optional[str]]:
        """
        Performs a JSON-RPC request with the given parameters.

        It returns a tuple (result, error).
        """
        req = {
            "jsonrpc": "2.0",
            "id": self.next_id,
            "method": method,
        }
        if params is not None:
            req["params"] = params
        self.next_id += 1

        raw = self._s.post(self.url, json=req)
        resp: dict = raw.json()
        raw.close()
        err: dict | None = resp.get("error")
        if err is not None:
            err_msg = "%i: %s" % (err.get("code"), err.get("message"))
            return None, err_msg
        result = resp.get("result")
        if result is None:
            return None, "No error and no result: invalid JSON-RPC response"
        return result, None

    def _call(
        self, method: str, transform: Callable[[Any], _T], data: Any = None
    ) -> _T | None:
        (resp, err) = self.rpc_call(method, data)
        if err is not None:
            log.error("failed to call method %s: %s", method, err)
            return None
        return transform(resp)

    def _call_each(
        self, method: str, transform: Callable[[Any], _T], data: Any = None
    ) -> list[_T]:
        (resp, err) = self.rpc_call(method, data)
        if err is not None:
            log.error("failed to call method %s: %s", method, err)
            return []
        return [transform(r) for r in resp]


@dataclass
class Result(IpcResult):
    uid: str
    client: "Client"
    error: Optional[o.ResultState]

    def get_state(self) -> o.ResultState:
        if self.error is not None:
            return self.error
        (state, err) = self.client.rpc_call("result/state", {"@id": self.uid})
        if err:
            self.err = o.ResultState(id=self.uid, error=err)
            return self.err
        return o.ResultState.from_dict(state)

    def simulate_next(self) -> o.ResultState:
        if self.error is not None:
            return self.error
        (state, err) = self.client.rpc_call(
            "result/simulate/next", {"@id": self.uid}
        )
        if err:
            self.err = o.ResultState(id=self.uid, error=err)
            return self.err
        return o.ResultState.from_dict(state)

    def dispose(self):
        if self.error is not None:
            return
        self.client.rpc_call("result/dispose", {"@id": self.uid})

    def get_demand(self) -> o.TechFlowValue | None:
        (data, err) = self.client.rpc_call("result/demand", {"@id": self.uid})
        if err:
            log.error("failed to get demand: %s", err)
            return None
        return o.TechFlowValue.from_dict(data)

    def get_tech_flows(self) -> list[o.TechFlow]:
        (data, err) = self.client.rpc_call(
            "result/tech-flows", {"@id": self.uid}
        )
        if err:
            log.error("failed to query /tech-flows: %s", err)
            return []
        return [o.TechFlow.from_dict(d) for d in data]

    def get_envi_flows(self) -> list[o.EnviFlow]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/envi-flows", args)
        if err:
            log.error("request envi-flows failed: %s", err)
            return []
        return [o.EnviFlow.from_dict(d) for d in r]

    def get_impact_categories(self) -> list[o.Ref]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/impact-categories", args)
        if err:
            log.error("request impact-categories failed: %s", err)
            return []
        return [o.Ref.from_dict(d) for d in r]

    # region: tech-flows

    def get_total_requirements(self) -> list[o.TechFlowValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-requirements", args)
        if err:
            log.error("request total-requirements failed: %s", err)
            return []
        return [o.TechFlowValue.from_dict(d) for d in r]

    def get_total_requirements_of(
        self, tech_flow: o.TechFlow
    ) -> o.TechFlowValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-requirements-of", args)
        if err:
            log.error("request total-requirements-of failed: %s", err)
            return o.TechFlowValue(amount=0, tech_flow=tech_flow)
        return o.TechFlowValue.from_dict(r)

    def get_scaling_factors(self) -> list[o.TechFlowValue]:
        return self.client._call_each(
            "result/scaling-factors",
            o.TechFlowValue.from_dict,
            {"@id": self.uid},
        )

    def get_scaled_tech_flows_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        return self.client._call_each(
            "result/scaled-tech-flows-of",
            o.TechFlowValue.from_dict,
            {"@id": self.uid, "techFlow": tech_flow.to_dict()},
        )

    def get_unscaled_tech_flows_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        return self.client._call_each(
            "result/unscaled-tech-flows-of",
            o.TechFlowValue.from_dict,
            {"@id": self.uid, "techFlow": tech_flow.to_dict()},
        )

    # endregion

    # region: inventory results

    def get_total_flows(self) -> list[o.EnviFlowValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-flows", args)
        if err:
            log.error("request total-flows failed: %s", err)
            return []
        return [o.EnviFlowValue.from_dict(d) for d in r]

    def get_total_flow_value_of(self, envi_flow: o.EnviFlow) -> o.EnviFlowValue:
        args = {"@id": self.uid, "enviFlow": envi_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-flow-value-of", args)
        if err:
            log.error("request total-flow-value-of failed: %s", err)
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return o.EnviFlowValue.from_dict(r)

    def get_flow_contributions_of(
        self, envi_flow: o.EnviFlow
    ) -> list[o.TechFlowValue]:
        args = {"@id": self.uid, "enviFlow": envi_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/flow-contributions-of", args)
        if err:
            log.error("request direct-flow-values-of failed: %s", err)
            return []
        return [o.TechFlowValue.from_dict(d) for d in r]

    def get_direct_interventions_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/direct-interventions-of", args)
        if err:
            log.error("request direct-flows-of failed: %s", err)
            return []
        return [o.EnviFlowValue.from_dict(d) for d in r]

    def get_direct_intervention_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/direct-intervention-of", args)
        if err:
            log.error("request direct-flow-of failed: %s", err)
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return o.EnviFlowValue.from_dict(r)

    def get_flow_intensities_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/flow-intensities-of", args)
        if err:
            log.error("request total-flows-of-one failed: %s", err)
            return []
        return [o.EnviFlowValue.from_dict(d) for d in r]

    def get_flow_intensity_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/flow-intensity-of", args)
        if err:
            log.error("request total-flow-of-one failed: %s", err)
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return o.EnviFlowValue.from_dict(r)

    def get_total_interventions_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-interventions-of", args)
        if err:
            log.error("request total-flows-of failed: %s", err)
            return []
        return [o.EnviFlowValue.from_dict(d) for d in r]

    def get_total_intervention_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/total-intervention-of", args)
        if err:
            log.error("request total-flow-of failed: %s", err)
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return o.EnviFlowValue.from_dict(r)

    def get_upstream_interventions_of(
        self, envi_flow: o.EnviFlow, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "path": _encode_path(path),
        }
        (r, err) = self.client.rpc_call(
            "result/upstream-interventions-of", args
        )
        if err:
            log.error("request upstream-interventions-of failed: %s", err)
            return []
        return [o.UpstreamNode.from_dict(d) for d in r]

    # endregion

    # region: impact results

    def get_total_impacts(self) -> list[o.ImpactValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-impacts", args)
        if err:
            log.error("request total-impacts failed: %s", err)
            return []
        return [o.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_value_of(
        self, impact_category: o.Ref
    ) -> o.ImpactValue:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/total-impact-value-of", args)
        if err:
            log.error("request total-impact-value-of failed: %s", err)
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return o.ImpactValue.from_dict(r)

    def get_normalized_impacts(self) -> list[o.ImpactValue]:
        (r, err) = self.client.rpc_call(
            "result/total-impacts/normalized", {"@id": self.uid}
        )
        if err:
            log.error("failed to get normalized impacts: %s", err)
            return []
        return [o.ImpactValue.from_dict(d) for d in r]

    def get_weighted_impacts(self) -> list[o.ImpactValue]:
        (r, err) = self.client.rpc_call(
            "result/total-impacts/weighted", {"@id": self.uid}
        )
        if err:
            log.error("failed to get weighted impacts: %s", err)
            return []
        return [o.ImpactValue.from_dict(d) for d in r]

    def get_impact_contributions_of(
        self, impact_category: o.Ref
    ) -> list[o.TechFlowValue]:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/impact-contributions-of", args)
        if err:
            log.error("request direct-impact-values-of failed: %s", err)
            return []
        return [o.TechFlowValue.from_dict(d) for d in r]

    def get_direct_impacts_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/direct-impacts-of", args)
        if err:
            log.error("request direct-impacts-of failed: %s", err)
            return []
        return [o.ImpactValue.from_dict(d) for d in r]

    def get_direct_impact_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/direct-impact-of", args)
        if err:
            log.error("request direct-impact-of failed: %s", err)
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return o.ImpactValue.from_dict(r)

    def get_impact_intensities_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-impacts-of-one", args)
        if err:
            log.error("request total-impacts-of-one failed: %s", err)
            return []
        return [o.ImpactValue.from_dict(d) for d in r]

    def get_impact_intensity_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/impact-intensity-of", args)
        if err:
            log.error("request total-impact-of-one failed: %s", err)
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return o.ImpactValue.from_dict(r)

    def get_total_impacts_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-impacts-of", args)
        if err:
            log.error("request total-impacts-of failed: %s", err)
            return []
        return [o.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/total-impact-of", args)
        if err:
            log.error("request total-impact-of failed: %s", err)
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return o.ImpactValue.from_dict(r)

    def get_impact_factors_of(
        self, impact_category: o.Ref
    ) -> list[o.EnviFlowValue]:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/impact-factors-of", args)
        if err:
            log.error("request impact-factors-of failed: %s", err)
            return []
        return [o.EnviFlowValue.from_dict(d) for d in r]

    def get_impact_factor_of(
        self, impact_category: o.Ref, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "enviFlow": envi_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/impact-factor-of", args)
        if err:
            log.error("request impact-factor-of failed: %s", err)
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return o.EnviFlowValue.from_dict(r)

    def get_flow_impacts_of(
        self, impact_category: o.Ref
    ) -> list[o.EnviFlowValue]:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/flow-impacts-of", args)
        if err:
            log.error("request flow-impacts-of failed: %s", err)
            return []
        return [o.EnviFlowValue.from_dict(d) for d in r]

    def get_flow_impact_of(
        self, impact_category: o.Ref, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "enviFlow": envi_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/flow-impact-of", args)
        if err:
            log.error("request flow-impact-of failed: %s", err)
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return o.EnviFlowValue.from_dict(r)

    def get_upstream_impacts_of(
        self, impact_category: o.Ref, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "path": _encode_path(path),
        }
        (r, err) = self.client.rpc_call("result/upstream-impacts-of", args)
        if err:
            log.error("request upstream-impacts-of failed: %s", err)
            return []
        return [o.UpstreamNode.from_dict(d) for d in r]

    # endregion

    # region: cost results

    def get_total_costs(self) -> o.CostValue:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-costs", args)
        if err:
            log.error("request total-costs failed: %s", err)
            return o.CostValue(amount=0)
        return o.CostValue.from_dict(r)

    def get_cost_contributions(self) -> list[o.TechFlowValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/cost-contributions", args)
        if err:
            log.error("request direct-cost-values failed: %s", err)
            return []
        return [o.TechFlowValue.from_dict(d) for d in r]

    def get_direct_costs_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/direct-costs-of", args)
        if err:
            log.error("request direct-costs-of failed: %s", err)
            return o.CostValue(amount=0)
        return o.CostValue.from_dict(r)

    def get_cost_intensities_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/cost-intensities-of", args)
        if err:
            log.error("request total-costs-of-one failed: %s", err)
            return o.CostValue(amount=0)
        return o.CostValue.from_dict(r)

    def get_total_costs_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-costs-of", args)
        if err:
            log.error("request total-costs-of failed: %s", err)
            return o.CostValue(amount=0)
        return o.CostValue.from_dict(r)

    def get_upstream_costs_of(
        self, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        args = {
            "@id": self.uid,
            "path": _encode_path(path),
        }
        (r, err) = self.client.rpc_call("result/upstream-costs-of", args)
        if err:
            log.error("request upstream-costs-of failed: %s", err)
            return []
        return [o.UpstreamNode.from_dict(d) for d in r]

    # endregion

    def get_sankey_graph(self, config: o.SankeyRequest) -> o.SankeyGraph | None:
        args = {
            "@id": self.uid,
            "config": config.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/sankey", args)
        if err:
            log.error("request result/sankey failed: %s", err)
            return None
        return o.SankeyGraph.from_dict(r)


def _encode_path(path: list[o.TechFlow]) -> str | None:
    if path is None or len(path) == 0:
        return None
    p = None
    for tf in path:
        next = ""
        if tf.provider and tf.provider.id:
            next += tf.provider.id
        if tf.flow and tf.flow.id:
            next += "::" + tf.flow.id
        if p is None:
            p = next
        else:
            p += "/" + next
    return p
