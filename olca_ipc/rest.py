import logging as log
import time
from typing import cast, Any, Callable, Type, TypeVar

import olca_schema as schema
import requests
from olca_schema import results as res

from .protocol import E, IpcProtocol, IpcResult

OK = 200

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

    def get_descriptor(self, model_type: Type[E], uid: str) -> schema.Ref | None:
        return self._get(
            f"data/{_path_of(model_type)}/{uid}/info", schema.Ref.from_dict
        )

    def get_providers(self, flow: schema.Ref | schema.Flow | None = None) -> list[res.TechFlow]:
        url: str
        if flow_id:
            url = f"{self.endpoint}data/providers/{flow_id}"
        else:
            url = f"{self.endpoint}data/providers"
        r = requests.get(url)
        if _not_ok(r):
            log.error("failed to get providers: %s", url)
            return []
        return [res.TechFlow.from_dict(d) for d in r.json()]

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[schema.Parameter] | list[schema.ParameterRedef]:
        path = _path_of(model_type)
        if path is None:
            return []
        r = requests.get(f"{self.endpoint}data/{path}/{uid}/parameters")
        if _not_ok(r):
            log.error(
                "failed to get parameters of type=%s id=%s", model_type, uid
            )
            return []
        if model_type in (schema.ProductSystem, schema.Project):
            return [schema.ParameterRedef.from_dict(d) for d in r.json()]
        else:
            return [schema.Parameter.from_dict(d) for d in r.json()]




class Result:
    def __init__(self, client: RestClient, state: res.ResultState):
        self.client = client
        self.uid = state.id
        self.error: res.ResultState | None = None
        if state.error:
            self.error = state

    def get_state(self) -> res.ResultState:
        if self.error is not None:
            return self.error
        r = self._get("state")
        if not r:
            self.error = res.ResultState(
                id=self.uid,
                error="no result state could be retreived from server",
            )
            return self.error
        state = res.ResultState.from_dict(r)
        if state.error:
            self.error = state
        return state

    def wait_until_ready(self) -> res.ResultState:
        state = self.get_state()
        if not state.is_scheduled:
            return state
        while state.is_scheduled:
            time.sleep(0.5)
            state = self.get_state()
            if not state.is_scheduled:
                return state
        self.error = res.ResultState(self.uid, error="did not finished")
        return self.error

    def dispose(self) -> res.ResultState:
        if self.error:
            return self.error
        url = f"{self.client.endpoint}results/{self.uid}/dispose"
        r = requests.post(url)
        if _not_ok(r):
            self.error = res.ResultState(
                id=self.uid, error="dispose did not return state"
            )
            return self.error
        return res.ResultState.from_dict(r.json())

    def get_tech_flows(self) -> list[res.TechFlow]:
        r = self._get("tech-flows")
        if not r:
            return []
        else:
            return [res.TechFlow.from_dict(d) for d in r]

    def get_envi_flows(self) -> list[res.EnviFlow]:
        r = self._get("envi-flows")
        if not r:
            return []
        else:
            return [res.EnviFlow.from_dict(d) for d in r]

    def get_impact_categories(self) -> list[schema.Ref]:
        r = self._get("impact-categories")
        if not r:
            return []
        else:
            return [schema.Ref.from_dict(d) for d in r]

    def get_total_requirements(self) -> list[res.TechFlowValue]:
        r = self._get("total-requirements")
        if not r:
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_requirements_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.TechFlowValue]:
        r = self._get(f"total-requirements-of/{_tech_id(tech_flow)}")
        if not r:
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_flows(self) -> list[res.EnviFlowValue]:
        r = self._get(f"total-flows")
        if not r:
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_flow_value_of(
        self, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue | None:
        r = self._get(f"total-flow-value-of/{_envi_id(envi_flow)}")
        if not r:
            return None
        return res.EnviFlowValue.from_dict(r)

    def _get(self, path: str) -> Any:
        url = f"{self.client.endpoint}results/{self.uid}/{path}"
        r = requests.get(url)
        if _not_ok(r):
            log.error("GET: %s; failed for result=%s", path, self.uid)
            return None
        return r.json()


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
