import logging as log
from typing import cast, Any, Callable, Type, TypeVar

import olca_schema as o
import requests

from .protocol import E, IpcProtocol, IpcResult

T = TypeVar("T")


class RestClient(IpcProtocol):
    def __init__(self, endpoint: str, **kwargs):
        self.endpoint = endpoint if endpoint.endswith("/") else endpoint + "/"
        self.req_args = kwargs

    def _get(self, path, transform: Callable[[Any], T]) -> T | None:
        resp = requests.get(self.endpoint + path, **self.req_args)
        if _not_ok(resp):
            log.error("ERROR: GET %s failed: %s", path, resp.text)
            return None
        return transform(resp.json())

    def _get_each(self, path, transform: Callable[[Any], T]) -> list[T]:
        resp = requests.get(self.endpoint + path, **self.req_args)
        if _not_ok(resp):
            log.error("ERROR: GET %s failed: %s", path, resp.text)
            return []
        return [transform(x) for x in resp.json()]

    def _post(
        self, path, transform: Callable[[Any], T], data: Any | None = None
    ) -> T | None:
        resp = requests.post(self.endpoint + path, json=data, **self.req_args)
        if _not_ok(resp):
            log.error("ERROR: POST %s failed: %s", path, resp.text)
            return None
        return transform(resp.json())

    def _post_each(
        self, path, transform: Callable[[Any], T], data: Any | None = None
    ) -> list[T]:
        resp = requests.post(self.endpoint + path, json=data, **self.req_args)
        if _not_ok(resp):
            log.error("ERROR: POST %s failed: %s", path, resp.text)
            return []
        return [transform(x) for x in resp.json()]

    def get(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> E | None:
        if not uid and not name:
            log.error("no ID or name given")
            return None
        if uid:
            path = f"data/{_path_of(model_type)}/{uid}"
        else:
            path = f"data/{_path_of(model_type)}/name/{name}"
        return cast(E, self._get(path, model_type.from_dict))

    def get_all(self, model_type: Type[E]) -> list[E]:
        xs = self._get_each(
            f"data/{_path_of(model_type)}/all",
            model_type.from_dict,
        )
        return cast(list[E], xs)

    def get_descriptors(self, model_type: Type[E]) -> list[o.Ref]:
        return self._get_each(
            f"data/{_path_of(model_type)}",
            o.Ref.from_dict,
        )

    def get_descriptor(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> o.Ref | None:
        if uid is None and name is None:
            log.error("error: no uuid or name given")
            return None
        if uid is not None:
            return self._get(
                f"data/{_path_of(model_type)}/{uid}/info", o.Ref.from_dict
            )
        if name is not None:
            return self._get(
                f"data/{_path_of(model_type)}/name/{name}/info",
                o.Ref.from_dict,
            )

    def get_providers(
        self, flow: o.Ref | o.Flow | None = None
    ) -> list[o.TechFlow]:
        if flow is not None:
            path = f"data/providers/{flow.id}"
        else:
            path = "data/providers"
        return self._get_each(path, o.TechFlow.from_dict)

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[o.Parameter] | list[o.ParameterRedef]:
        path = f"data/{_path_of(model_type)}/{uid}/parameters"
        if model_type in (o.ProductSystem, o.Project):
            return self._get_each(path, o.ParameterRedef.from_dict)
        else:
            return self._get_each(path, o.Parameter.from_dict)

    def put(self, model: o.RootEntity) -> o.Ref | None:
        resp = requests.put(
            f"{self.endpoint}data/{_path_of(model.__class__)}",
            json=model.to_dict(),
            **self.req_args,
        )
        if _not_ok(resp):
            log.error("failed to upload entity: %s", resp.text)
            return None
        return o.Ref.from_dict(resp.json())

    def create_product_system(
        self,
        process: o.Ref | o.Process,
        config: o.LinkingConfig | None = None,
    ) -> o.Ref | None:
        params: dict[str, Any] = {"process": o.as_ref(process).to_dict()}
        if config is not None:
            params["config"] = config.to_dict()
        return self._post("data/create-system", o.Ref.from_dict, params)

    def delete(self, model: o.RootEntity | o.Ref) -> o.Ref | None:
        if isinstance(model, o.Ref):
            t = model.model_type
        else:
            t = model.__class__.__name__
        path = ""
        for char in t:
            if char.isupper() and len(path) > 0:
                path += "-"
            path += char
        url = f"{self.endpoint}data/{path.lower()}/{model.id}"
        resp = requests.delete(url, **self.req_args)
        if _not_ok(resp):
            log.error("failed to delete model: %s", resp.text)
            return None
        return o.Ref.from_dict(resp.json())

    def calculate(self, setup: o.CalculationSetup) -> IpcResult | None:
        state = self._post(
            "result/calculate", o.ResultState.from_dict, setup.to_dict()
        )
        if state is None:
            return None
        return Result(self, state)

    def simulate(self, setup: o.CalculationSetup) -> IpcResult | None:
        state = self._post(
            "result/simulate", o.ResultState.from_dict, setup.to_dict()
        )
        if state is None:
            return None
        return Result(self, state)


class Result(IpcResult):
    def __init__(self, client: RestClient, state: o.ResultState):
        self.client = client
        self.uid = state.id
        self.error: o.ResultState | None = None
        if state.error:
            self.error = state

    def get_state(self) -> o.ResultState:
        if self.error is not None:
            return self.error
        state = self._get("state", o.ResultState.from_dict)
        if state is None:
            self.error = o.ResultState(
                id=self.uid,
                error="no result state could be retreived from server",
            )
            return self.error
        if state.error:
            self.error = state
        return state

    def simulate_next(self) -> o.ResultState:
        if self.error is not None:
            return self.error
        state = self._post("simulate/next", o.ResultState.from_dict)
        if state is None:
            self.err = o.ResultState(
                id=self.uid, error="failed to run simulation"
            )
            return self.err
        return state

    def dispose(self) -> o.ResultState:
        if self.error:
            return self.error
        state = self._post("dispose", o.ResultState.from_dict)
        if state is None:
            self.error = o.ResultState(
                id=self.uid, error="dispose did not return state"
            )
            return self.error
        return state

    def get_demand(self) -> o.TechFlowValue | None:
        return self._get("demand", o.TechFlowValue.from_dict)

    def get_tech_flows(self) -> list[o.TechFlow]:
        return self._get_each("tech-flows", o.TechFlow.from_dict)

    def get_envi_flows(self) -> list[o.EnviFlow]:
        return self._get_each("envi-flows", o.EnviFlow.from_dict)

    def get_impact_categories(self) -> list[o.Ref]:
        return self._get_each("impact-categories", o.Ref.from_dict)

    # region: tech-flows

    def get_total_requirements(self) -> list[o.TechFlowValue]:
        return self._get_each("total-requirements", o.TechFlowValue.from_dict)

    def get_total_requirements_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        return self._get_each(
            f"total-requirements-of/{_tech_id(tech_flow)}",
            o.TechFlowValue.from_dict,
        )

    def get_scaling_factors(self) -> list[o.TechFlowValue]:
        return self._get_each("scaling-factors", o.TechFlowValue.from_dict)

    def get_scaled_tech_flows_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        return self._get_each(
            f"scaled-tech-flows-of/{_tech_id(tech_flow)}",
            o.TechFlowValue.from_dict,
        )

    def get_unscaled_tech_flows_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        return self._get_each(
            f"unscaled-tech-flows-of/{_tech_id(tech_flow)}",
            o.TechFlowValue.from_dict,
        )

    # endregion

    # region: inventory results

    def get_total_flows(self) -> list[o.EnviFlowValue]:
        return self._get_each("total-flows", o.EnviFlowValue.from_dict)

    def get_total_flow_value_of(
        self, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue | None:
        return self._get(
            f"total-flow-value-of/{_envi_id(envi_flow)}",
            o.EnviFlowValue.from_dict,
        )

    def get_flow_contributions_of(
        self, envi_flow: o.EnviFlow
    ) -> list[o.TechFlowValue]:
        return self._get_each(
            f"flow-contributions-of/{_envi_id(envi_flow)}",
            o.TechFlowValue.from_dict,
        )

    def get_direct_interventions_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        return self._get_each(
            f"direct-interventions-of/{_tech_id(tech_flow)}",
            o.EnviFlowValue.from_dict,
        )

    def get_direct_intervention_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        val = self._get(
            f"direct-intervention-of/{_envi_id(envi_flow)}/{_tech_id(tech_flow)}",
            o.EnviFlowValue.from_dict,
        )
        if val is None:
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_flow_intensities_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlow]:
        return self._get_each(
            f"flow-intensities-of/{_tech_id(tech_flow)}", o.EnviFlow.from_dict
        )

    def get_flow_intensity_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        val = self._get(
            f"flow-intensity-of/{_envi_id(envi_flow)}/{_tech_id(tech_flow)}",
            o.EnviFlowValue.from_dict,
        )
        if val is None:
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_total_interventions_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        return self._get_each(
            f"total-interventions-of/{_tech_id(tech_flow)}",
            o.EnviFlowValue.from_dict,
        )

    def get_total_intervention_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        val = self._get(
            f"total-intervention-of/{_envi_id(envi_flow)}/{_tech_id(tech_flow)}",
            o.EnviFlowValue.from_dict,
        )
        if val is None:
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_upstream_interventions_of(
        self, envi_flow: o.EnviFlow, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        params: dict[str, Any] = {
            "path": _encode_path(path),
        }
        return self._post_each(
            f"upstream-interventions-of/{_envi_id(envi_flow)}",
            o.UpstreamNode.from_dict,
            params,
        )

    # endregion

    # region: impact results

    def get_total_impacts(self) -> list[o.ImpactValue]:
        return self._get_each(f"total-impacts", o.ImpactValue.from_dict)

    def get_total_impact_value_of(
        self, impact_category: o.Ref
    ) -> o.ImpactValue:
        val = self._get(
            f"total-impact-value-of/{impact_category.id}",
            o.ImpactValue.from_dict,
        )
        if val is None:
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_normalized_impacts(self) -> list[o.ImpactValue]:
        return self._get_each(f"normalized-impacts", o.ImpactValue.from_dict)

    def get_weighted_impacts(self) -> list[o.ImpactValue]:
        return self._get_each(f"weighted-impacts", o.ImpactValue.from_dict)

    def get_impact_contributions_of(
        self, impact_category: o.Ref
    ) -> list[o.TechFlowValue]:
        return self._get_each(
            f"impact-contributions-of/{impact_category.id}",
            o.TechFlowValue.from_dict,
        )

    def get_direct_impacts_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        return self._get_each(
            f"direct-impacts-of/{_tech_id(tech_flow)}",
            o.ImpactValue.from_dict,
        )

    def get_direct_impact_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        val = self._get(
            f"direct-impact-of/{impact_category.id}/{_tech_id(tech_flow)}",
            o.ImpactValue.from_dict,
        )
        if val is None:
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_impact_intensities_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        return self._get_each(
            f"impact-intensities-of/{_tech_id(tech_flow)}",
            o.ImpactValue.from_dict,
        )

    def get_impact_intensity_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        val = self._get(
            f"impact-intensity-of/{impact_category.id}/{_tech_id(tech_flow)}",
            o.ImpactValue.from_dict,
        )
        if val is None:
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_total_impacts_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        return self._get_each(
            f"total-impacts-of/{_tech_id(tech_flow)}", o.ImpactValue.from_dict
        )

    def get_total_impact_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        val = self._get(
            f"total-impact-of/{impact_category.id}/{_tech_id(tech_flow)}",
            o.ImpactValue.from_dict,
        )
        if val is None:
            return o.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_impact_factors_of(
        self, impact_category: o.Ref
    ) -> list[o.EnviFlowValue]:
        return self._get_each(
            f"impact-factors-of/{impact_category.id}",
            o.EnviFlowValue.from_dict,
        )

    def get_impact_factor_of(
        self, impact_category: o.Ref, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue:
        val = self._get(
            f"impact-factor-of/{impact_category.id}/{_envi_id(envi_flow)}",
            o.EnviFlowValue.from_dict,
        )
        if val is None:
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_flow_impacts_of(
        self, impact_category: o.Ref
    ) -> list[o.EnviFlowValue]:
        return self._get_each(
            f"flow-impacts-of/{impact_category.id}", o.EnviFlowValue.from_dict
        )

    def get_flow_impact_of(
        self, impact_category: o.Ref, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue:
        val = self._get(
            f"flow-impact-of/{impact_category.id}/{_envi_id(envi_flow)}",
            o.EnviFlowValue.from_dict,
        )
        if val is None:
            return o.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_upstream_impacts_of(
        self, impact_category: o.Ref, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        params: dict[str, Any] = {
            "path": _encode_path(path),
        }
        return self._post_each(
            f"upstream-impacts-of/{impact_category.id}",
            o.UpstreamNode.from_dict,
            params,
        )

    # endregion

    # region: cost results

    def get_total_costs(self) -> o.CostValue:
        val = self._get(f"total-costs", o.CostValue.from_dict)
        if val is None:
            return o.CostValue(amount=0)
        return val

    def get_cost_contributions(self) -> list[o.TechFlowValue]:
        return self._get_each(f"cost-contributions", o.TechFlowValue.from_dict)

    def get_direct_costs_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        val = self._get(
            f"direct-costs-of/{_tech_id(tech_flow)}", o.CostValue.from_dict
        )
        if val is None:
            return o.CostValue(amount=0)
        return val

    def get_cost_intensities_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        val = self._get(
            f"cost-intensities-of/{_tech_id(tech_flow)}",
            o.CostValue.from_dict,
        )
        if val is None:
            return o.CostValue(amount=0)
        return val

    def get_total_costs_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        val = self._get(
            f"total-costs-of/{_tech_id(tech_flow)}", o.CostValue.from_dict
        )
        if val is None:
            return o.CostValue(amount=0)
        return val

    def get_upstream_costs_of(
        self, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        params: dict[str, Any] = {
            "path": _encode_path(path),
        }
        return self._post_each(
            "upstream-costs-of", o.UpstreamNode.from_dict, params
        )

    # endregion

    def get_sankey_graph(self, config: o.SankeyRequest) -> o.SankeyGraph | None:
        return self._post("sankey", o.SankeyGraph.from_dict, config.to_dict())

    def _get(self, path: str, transform: Callable[[Any], T]) -> T | None:
        return self.client._get(f"result/{self.uid}/{path}", transform)

    def _get_each(self, path: str, transform: Callable[[Any], T]) -> list[T]:
        return self.client._get_each(f"result/{self.uid}/{path}", transform)

    def _post(
        self, path, transform: Callable[[Any], T], data: Any | None = None
    ) -> T | None:
        return self.client._post(f"result/{self.uid}/{path}", transform, data)

    def _post_each(
        self, path, transform: Callable[[Any], T], data: Any | None = None
    ) -> list[T]:
        return self.client._post_each(
            f"result/{self.uid}/{path}", transform, data
        )


def _not_ok(resp: requests.Response) -> bool:
    if resp.status_code == 200:
        return False
    log.error("response status != 200; message=%s", resp.text)
    return True


def _tech_id(tech_flow: o.TechFlow) -> str:
    tech_id = ""
    if tech_flow.provider and tech_flow.provider.id:
        tech_id = tech_flow.provider.id
    if tech_flow.flow and tech_flow.flow.id:
        tech_id += "::" + tech_flow.flow.id
    return tech_id


def _envi_id(envi_flow: o.EnviFlow) -> str:
    envi_id = ""
    if envi_flow.flow and envi_flow.flow.id:
        envi_id = envi_flow.flow.id
    if envi_flow.location and envi_flow.location.id:
        envi_id += "::" + envi_flow.location.id
    return envi_id


def _path_of(model_type: Type[E]) -> str | None:
    if model_type is None:
        log.error("no model type given")
        return None
    match model_type:
        case o.Actor:
            return "actors"
        case o.Currency:
            return "currencies"
        case o.DQSystem:
            return "dq-systems"
        case o.Epd:
            return "epds"
        case o.Flow:
            return "flows"
        case o.FlowProperty:
            return "flow-properties"
        case o.ImpactCategory:
            return "impact-categories"
        case o.ImpactMethod:
            return "impact-methods"
        case o.Location:
            return "locations"
        case o.Parameter:
            return "parameters"
        case o.Process:
            return "processes"
        case o.ProductSystem:
            return "product-systems"
        case o.Project:
            return "projects"
        case o.Result:
            return "results"
        case o.SocialIndicator:
            return "social-indicators"
        case o.Source:
            return "sources"
        case o.UnitGroup:
            return "unit-groups"
        case _:
            log.error("unknown root entity type: %s", model_type)
            return None


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
