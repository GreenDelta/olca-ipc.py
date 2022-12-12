import logging as log
import time
from typing import cast, Any, Type, TypeVar

import olca_schema as lca
import requests
from olca_schema import results as res

E = TypeVar("E", bound=lca.RootEntity)
OK = 200


class RestClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint if endpoint.endswith("/") else endpoint + "/"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def close(self):
        return

    def get(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> E | None:
        path = _path_of(model_type)
        if path is None:
            return None
        if not uid and not name:
            log.error("no ID or name given")
            return

        url: str
        if uid:
            url = f"{self.endpoint}data/{path}/{uid}"
        else:
            url = f"{self.endpoint}data/{path}/name/{name}"

        r = requests.get(url)
        if _not_ok(r):
            log.error("failed to get %s id=%s: %s", model_type, uid, r.text)
            return None
        return cast(E, model_type.from_dict(r.json()))

    def get_all(self, model_type: Type[E]) -> list[E]:
        path = _path_of(model_type)
        if path is None:
            return []
        r = requests.get(f"{self.endpoint}data/{path}/all")
        if _not_ok(r):
            log.error("failed to get all objects of type %s", model_type)
            return []
        return cast(list[E], [model_type.from_dict(d) for d in r.json()])

    def get_descriptors(self, model_type: Type[E]) -> list[lca.Ref]:
        path = _path_of(model_type)
        if path is None:
            return []
        r = requests.get(f"{self.endpoint}data/{path}")
        if _not_ok(r):
            log.error("failed to get descriptors of type %s", model_type)
            return []
        return [lca.Ref.from_dict(d) for d in r.json()]

    def get_descriptor(self, model_type: Type[E], uid: str) -> lca.Ref | None:
        path = _path_of(model_type)
        if path is None:
            return None
        r = requests.get(f"{self.endpoint}data/{path}/{uid}/info")
        if _not_ok(r):
            log.error("failed to get descriptor type=%s id=%s", model_type, uid)
            return None
        return lca.Ref.from_dict(r.json())

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[lca.Parameter] | list[lca.ParameterRedef]:
        path = _path_of(model_type)
        if path is None:
            return []
        r = requests.get(f"{self.endpoint}data/{path}/{uid}/parameters")
        if _not_ok(r):
            log.error(
                "failed to get parameters of type=%s id=%s", model_type, uid
            )
            return []
        if model_type in (lca.ProductSystem, lca.Project):
            return [lca.ParameterRedef.from_dict(d) for d in r.json()]
        else:
            return [lca.Parameter.from_dict(d) for d in r.json()]

    def get_providers(self, flow_id: str | None = None) -> list[res.TechFlow]:
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

    def get_impact_categories(self) -> list[lca.Ref]:
        r = self._get("impact-categories")
        if not r:
            return []
        else:
            return [lca.Ref.from_dict(d) for d in r]

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
        case lca.Actor:
            return "actors"
        case lca.Currency:
            return "currencies"
        case lca.DQSystem:
            return "dq-systems"
        case lca.Epd:
            return "epds"
        case lca.Flow:
            return "flows"
        case lca.FlowProperty:
            return "flow-properties"
        case lca.ImpactCategory:
            return "impact-categories"
        case lca.ImpactMethod:
            return "impact-methods"
        case lca.Location:
            return "locations"
        case lca.Parameter:
            return "parameters"
        case lca.Process:
            return "processes"
        case lca.ProductSystem:
            return "product-systems"
        case lca.Project:
            return "projects"
        case lca.Result:
            return "results"
        case lca.SocialIndicator:
            return "social-indicators"
        case lca.Source:
            return "sources"
        case lca.UnitGroup:
            return "unit-groups"
        case _:
            log.error("unknown root entity type: %s", model_type)
            return None
