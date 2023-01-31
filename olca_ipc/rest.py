import logging as log
from typing import cast, Any, Callable, Type, TypeVar

import olca_schema as schema
import requests
from olca_schema import results as res

from .protocol import E, IpcProtocol, IpcResult

T = TypeVar("T")


class RestClient(IpcProtocol):
    def __init__(self, endpoint: str, **kwargs):
        self.endpoint = endpoint if endpoint.endswith("/") else endpoint + "/"
        self.req_args = kwargs

    def _get(self, path, transform: Callable[[Any], T]) -> T | None:
        url = self.endpoint + path
        response = requests.get(url, self.req_args)
        if _not_ok(response):
            log.error("ERROR: GET %s failed: %s", path, response.text)
            return None
        return transform(response.json())

    def _get_each(self, path, transform: Callable[[Any], T]) -> list[T]:
        url = self.endpoint + path
        response = requests.get(url, self.req_args)
        if _not_ok(response):
            log.error("ERROR: GET %s failed: %s", path, response.text)
            return []
        return [transform(x) for x in response.json()]

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

    def get_descriptors(self, model_type: Type[E]) -> list[schema.Ref]:
        return self._get_each(
            f"data/{_path_of(model_type)}",
            schema.Ref.from_dict,
        )

    def get_descriptor(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> schema.Ref | None:
        if uid is None and name is None:
            log.error("error: no uuid or name given")
            return None
        if uid is not None:
            return self._get(
                f"data/{_path_of(model_type)}/{uid}/info", schema.Ref.from_dict
            )
        if name is not None:
            return self._get(
                f"data/{_path_of(model_type)}/name/{name}/info",
                schema.Ref.from_dict,
            )

    def get_providers(
        self, flow: schema.Ref | schema.Flow | None = None
    ) -> list[res.TechFlow]:
        if flow is not None:
            path = f"data/providers/{flow.id}"
        else:
            path = "data/providers"
        return self._get_each(path, res.TechFlow.from_dict)

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[schema.Parameter] | list[schema.ParameterRedef]:
        path = f"data/{_path_of(model_type)}/{uid}/parameters"
        if model_type in (schema.ProductSystem, schema.Project):
            return self._get_each(path, schema.ParameterRedef.from_dict)
        else:
            return self._get_each(path, schema.Parameter.from_dict)

    def put(self, model: schema.RootEntity) -> schema.Ref | None:
        resp = requests.put(
            f"{self.endpoint}data/{_path_of(model.__class__)}",
            json=model.to_dict(),
        )
        if _not_ok(resp):
            log.error("failed to upload entity: %s", resp.text)
            return None
        return schema.Ref.from_dict(resp.json())

    def create_product_system(
        self,
        process: schema.Ref | schema.Process,
        config: schema.LinkingConfig | None = None,
    ) -> schema.Ref | None:
        params: dict[str, Any] = {"process": schema.as_ref(process).to_dict()}
        if config is not None:
            params["config"] = config.to_dict()
        resp = requests.post(f"{self.endpoint}data/create-system", json=params)
        if _not_ok(resp):
            log.error("failed to create system: %s", resp.text)
            return None
        return schema.Ref.from_dict(resp.json())

    def delete(
        self, model: schema.RootEntity | schema.Ref
    ) -> schema.Ref | None:
        if isinstance(model, schema.Ref):
            t = model.model_type
        else:
            t = model.__class__.__name__
        path = ""
        for char in t:
            if char.isupper() and len(path) > 0:
                path += "-"
            path += char
        url = f"{self.endpoint}data/{path.lower()}/{model.id}"
        resp = requests.delete(url)
        if _not_ok(resp):
            log.error("failed to delete model: %s", resp.text)
            return None
        return schema.Ref.from_dict(resp.json())

    def calculate(self, setup: res.CalculationSetup) -> IpcResult | None:
        resp = requests.post(
            f"{self.endpoint}result/calculate", json=setup.to_dict()
        )
        if _not_ok(resp):
            log.error("calculation failed: %s", resp.text)
            return None
        state = res.ResultState.from_dict(resp.json())
        return Result(self, state)


class Result(IpcResult):
    def __init__(self, client: RestClient, state: res.ResultState):
        self.client = client
        self.uid = state.id
        self.error: res.ResultState | None = None
        if state.error:
            self.error = state

    def get_state(self) -> res.ResultState:
        if self.error is not None:
            return self.error
        state = self._get("state", res.ResultState.from_dict)
        if state is None:
            self.error = res.ResultState(
                id=self.uid,
                error="no result state could be retreived from server",
            )
            return self.error
        if state.error:
            self.error = state
        return state

    def dispose(self) -> res.ResultState:
        if self.error:
            return self.error
        r = requests.post(f"{self.client.endpoint}result/{self.uid}/dispose")
        if _not_ok(r):
            self.error = res.ResultState(
                id=self.uid, error="dispose did not return state"
            )
            return self.error
        return res.ResultState.from_dict(r.json())

    def get_demand(self) -> res.TechFlowValue | None:
        return self._get("demand", res.TechFlowValue.from_dict)

    def get_tech_flows(self) -> list[res.TechFlow]:
        return self._get_each("tech-flows", res.TechFlow.from_dict)

    def get_envi_flows(self) -> list[res.EnviFlow]:
        return self._get_each("envi-flows", res.EnviFlow.from_dict)

    def get_impact_categories(self) -> list[schema.Ref]:
        return self._get_each("impact-categories", schema.Ref.from_dict)

    def get_total_requirements(self) -> list[res.TechFlowValue]:
        return self._get_each("total-requirements", res.TechFlowValue.from_dict)

    def get_total_requirements_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.TechFlowValue]:
        return self._get_each(
            f"total-requirements-of/{_tech_id(tech_flow)}",
            res.TechFlowValue.from_dict,
        )

    def get_total_flows(self) -> list[res.EnviFlowValue]:
        return self._get_each("total-flows", res.EnviFlowValue.from_dict)

    def get_total_flow_value_of(
        self, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue | None:
        return self._get(
            f"total-flow-value-of/{_envi_id(envi_flow)}",
            res.EnviFlowValue.from_dict,
        )

    def get_flow_contributions_of(
        self, envi_flow: res.EnviFlow
    ) -> list[res.TechFlowValue]:
        return self._get_each(
            f"flow-contributions-of/{_envi_id(envi_flow)}",
            res.TechFlowValue.from_dict,
        )

    def get_direct_interventions_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        return self._get_each(
            f"direct-interventions-of/{_tech_id(tech_flow)}",
            res.EnviFlowValue.from_dict,
        )

    def get_direct_intervention_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        val = self._get(
            f"direct-intervention-of/{_envi_id(envi_flow)}/{_tech_id(tech_flow)}",
            res.EnviFlowValue.from_dict,
        )
        if val is None:
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_flow_intensities_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlow]:
        return self._get_each(
            f"flow-intensities-of/{_tech_id(tech_flow)}", res.EnviFlow.from_dict
        )

    def get_flow_intensity_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        val = self._get(
            f"flow-intensity-of/{_envi_id(envi_flow)}/{_tech_id(tech_flow)}",
            res.EnviFlowValue.from_dict,
        )
        if val is None:
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_total_interventions_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        return self._get_each(
            f"total-interventions-of/{_tech_id(tech_flow)}",
            res.EnviFlowValue.from_dict,
        )

    def get_total_intervention_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        val = self._get(
            f"total-intervention-of/{_envi_id(envi_flow)}/{_tech_id(tech_flow)}",
            res.EnviFlowValue.from_dict,
        )
        if val is None:
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_total_impacts(self) -> list[res.ImpactValue]:
        return self._get_each(f"total-impacts", res.ImpactValue.from_dict)

    def get_total_impact_value_of(
        self, impact_category: schema.Ref
    ) -> res.ImpactValue:
        val = self._get(
            f"total-impact-value-of/{impact_category.id}",
            res.ImpactValue.from_dict,
        )
        if val is None:
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_normalized_impacts(self) -> list[res.ImpactValue]:
        return self._get_each(f"normalized-impacts", res.ImpactValue.from_dict)

    def get_weighted_impacts(self) -> list[res.ImpactValue]:
        return self._get_each(f"weighted-impacts", res.ImpactValue.from_dict)

    def get_impact_contributions_of(
        self, impact_category: schema.Ref
    ) -> list[res.TechFlowValue]:
        return self._get_each(
            f"impact-contributions-of/{impact_category.id}",
            res.TechFlowValue.from_dict,
        )

    def get_direct_impacts_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        return self._get_each(
            f"direct-impacts-of/{_tech_id(tech_flow)}",
            res.ImpactValue.from_dict,
        )

    def get_direct_impact_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        val = self._get(
            f"direct-impact-of/{impact_category.id}/{_tech_id(tech_flow)}",
            res.ImpactValue.from_dict,
        )
        if val is None:
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_impact_intensities_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        return self._get_each(
            f"impact-intensities-of/{_tech_id(tech_flow)}",
            res.ImpactValue.from_dict,
        )

    def get_impact_intensity_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        val = self._get(
            f"impact-intensity-of/{impact_category.id}/{_tech_id(tech_flow)}",
            res.ImpactValue.from_dict,
        )
        if val is None:
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_total_impacts_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        return self._get_each(
            f"total-impacts-of/{_tech_id(tech_flow)}", res.ImpactValue.from_dict
        )

    def get_total_impact_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        val = self._get(
            f"total-impact-of/{impact_category.id}/{_tech_id(tech_flow)}",
            res.ImpactValue.from_dict,
        )
        if val is None:
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return val

    def get_impact_factors_of(
        self, impact_category: schema.Ref
    ) -> list[res.EnviFlowValue]:
        return self._get_each(
            f"impact-factors-of/{impact_category.id}",
            res.EnviFlowValue.from_dict,
        )

    def get_impact_factor_of(
        self, impact_category: schema.Ref, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        val = self._get(
            f"impact-factor-of/{impact_category.id}/{_envi_id(envi_flow)}",
            res.EnviFlowValue.from_dict,
        )
        if val is None:
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_flow_impacts_of(
        self, impact_category: schema.Ref
    ) -> list[res.EnviFlowValue]:
        return self._get_each(
            f"flow-impacts-of/{impact_category.id}", res.EnviFlowValue.from_dict
        )

    def get_flow_impact_of(
        self, impact_category: schema.Ref, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        val = self._get(
            f"flow-impact-of/{impact_category.id}/{_envi_id(envi_flow)}",
            res.EnviFlowValue.from_dict,
        )
        if val is None:
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return val

    def get_total_costs(self) -> res.CostValue:
        val = self._get(f"total-costs", res.CostValue.from_dict)
        if val is None:
            return res.CostValue(amount=0)
        return val

    def get_cost_contributions(self) -> list[res.TechFlowValue]:
        return self._get_each(
            f"cost-contributions", res.TechFlowValue.from_dict
        )

    def get_direct_costs_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        val = self._get(
            f"direct-costs-of/{_tech_id(tech_flow)}", res.CostValue.from_dict
        )
        if val is None:
            return res.CostValue(amount=0)
        return val

    def get_cost_intensities_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        val = self._get(
            f"cost-intensities-of/{_tech_id(tech_flow)}",
            res.CostValue.from_dict,
        )
        if val is None:
            return res.CostValue(amount=0)
        return val

    def get_total_costs_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        val = self._get(
            f"total-costs-of/{_tech_id(tech_flow)}", res.CostValue.from_dict
        )
        if val is None:
            return res.CostValue(amount=0)
        return val

    def _get(self, path: str, transform: Callable[[Any], T]) -> T | None:
        return self.client._get(f"result/{self.uid}/{path}", transform)

    def _get_each(self, path: str, transform: Callable[[Any], T]) -> list[T]:
        return self.client._get_each(f"result/{self.uid}/{path}", transform)


def _not_ok(resp: requests.Response) -> bool:
    if resp.status_code == 200:
        return False
    log.error("response status != 200; message=%s", resp.text)
    return True


def _tech_id(tech_flow: res.TechFlow) -> str:
    tech_id = ""
    if tech_flow.provider and tech_flow.provider.id:
        tech_id = tech_flow.provider.id
    if tech_flow.flow and tech_flow.flow.id:
        tech_id += "::" + tech_flow.flow.id
    return tech_id


def _envi_id(envi_flow: res.EnviFlow) -> str:
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
        case schema.Actor:
            return "actors"
        case schema.Currency:
            return "currencies"
        case schema.DQSystem:
            return "dq-systems"
        case schema.Epd:
            return "epds"
        case schema.Flow:
            return "flows"
        case schema.FlowProperty:
            return "flow-properties"
        case schema.ImpactCategory:
            return "impact-categories"
        case schema.ImpactMethod:
            return "impact-methods"
        case schema.Location:
            return "locations"
        case schema.Parameter:
            return "parameters"
        case schema.Process:
            return "processes"
        case schema.ProductSystem:
            return "product-systems"
        case schema.Project:
            return "projects"
        case schema.Result:
            return "results"
        case schema.SocialIndicator:
            return "social-indicators"
        case schema.Source:
            return "sources"
        case schema.UnitGroup:
            return "unit-groups"
        case _:
            log.error("unknown root entity type: %s", model_type)
            return None
