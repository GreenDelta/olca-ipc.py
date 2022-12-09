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

    def get(self, model_type: Type[E], uid: str) -> E | None:
        path = _path_of(model_type)
        if path is None:
            return None
        url = f"{self.endpoint}data/{path}/{uid}"
        r = requests.get(url)
        if r.status_code != OK:
            log.warn("failed to get %s id=%s: %s", model_type, uid, r.text)
            return None
        obj = r.json()
        return cast(E, model_type.from_dict(obj))


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
