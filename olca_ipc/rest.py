import logging as log

import olca_schema as lca
import requests

from typing import cast, Type, TypeVar

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
        r = requests.get(f"{self.endpoint}/data/{path}/{uid}/info")
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
        r = requests.get(f"{self.endpoint}/data/{path}/{uid}/parameters")
        if _not_ok(r):
            log.error(
                "failed to get parameters of type=%s id=%s", model_type, uid
            )
            return []
        if model_type in (lca.ProductSystem, lca.Project):
            return [lca.ParameterRedef.from_dict(d) for d in r.json()]
        else:
            return [lca.Parameter.from_dict(d) for d in r.json()]


def _not_ok(resp: requests.Response) -> bool:
    if resp.status_code == 200:
        return False
    log.error("response status != 200; message=%s", resp.text)
    return True


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
