import logging as log

import requests
import olca_schema as schema
import olca_schema.results as results

from .protocol import E, IpcProtocol
from .result import Result

from typing import Any, Optional, Tuple, Type


class Client(IpcProtocol):
    """
    A client to communicate with an openLCA IPC server over the JSON-RPC
    protocol.
    """

    def __init__(self, port: int = 8080):
        self.url = "http://localhost:%i" % port
        self.next_id = 1

    def get(self, model_type: Type[E], uid="", name="") -> E | None:
        params = {"@type": model_type.__name__}
        if uid != "":
            params["@id"] = uid
        if name != "":
            params["name"] = name
        result, err = self.rpc_call("data/get", params)
        if err:
            log.warning("failed to get entity of type %s: %s", model_type, err)
            return None
        return model_type.from_dict(result)

    def get_all(self, model_type: Type[E]) -> list[E]:
        params = {"@type": model_type.__name__}
        result, err = self.rpc_call("data/get/all", params)
        if err:
            log.error("failed to get all of type %s: %s", model_type, err)
        return [model_type.from_dict(r) for r in result]

    def get_descriptors(self, model_type: Type[E]) -> list[schema.Ref]:
        params = {"@type": model_type.__name__}
        result, err = self.rpc_call("data/get/descriptors", params)
        if err:
            log.error(
                "failed to get descriptors of type %s: %s", model_type, err
            )
            return []
        return [schema.Ref.from_dict(r) for r in result]

    def get_descriptor(
        self, model_type: Type[E], uid="", name=""
    ) -> schema.Ref | None:
        params = {"@type": model_type.__name__}
        if uid != "":
            params["@id"] = uid
        if name != "":
            params["name"] = name
        result, err = self.rpc_call("data/get/descriptor", params)
        if err:
            log.error("failed to get descriptor: %s", err)
            return None
        return schema.Ref.from_dict(result)

    def get_providers(
        self, flow: schema.Ref | schema.Flow | None = None
    ) -> list[results.TechFlow]:
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
        return [results.TechFlow.from_dict(d) for d in providers]

    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[schema.Parameter | schema.ParameterRedef]:
        params = {"@type": model_type.__name__, "@id": uid}
        params, err = self.rpc_call("data/get/parameters", params)
        if err:
            log.error("failed to get parameters of %s id=%d", model_type, uid)
            return []
        if model_type in (schema.Process, schema.ImpactCategory):
            return [schema.Parameter.from_dict(p) for p in params]
        else:
            return [schema.ParameterRedef.from_dict(p) for p in params]

    def put(self, model: schema.RootEntity) -> schema.Ref | None:
        if model is None:
            return None
        resp, err = self.rpc_call("data/put", model.to_dict())
        if err:
            log.error("failed to insert model: %s", err)
            return None
        return schema.Ref.from_dict(resp)

    def create_product_system(
        self,
        process: schema.Ref | schema.Process,
        config: schema.LinkingConfig | None = None
    ) -> schema.Ref | None:
        conf = config
        if conf is None:
            conf = schema.LinkingConfig(
                prefer_unit_processes=False,
                provider_linking=schema.ProviderLinking.PREFER_DEFAULTS,
            )
        r, err = self.rpc_call(
            "data/create/system",
            {
                "process": schema.as_ref(process),
                "config": conf.to_dict(),
            },
        )
        if err:
            log.error("failed to create product system: %s", err)
            return None
        return schema.Ref.from_dict(r)

    def delete(
        self, model: schema.RootEntity | schema.Ref
    ) -> schema.Ref | None:
        if model is None:
            return
        ref = schema.as_ref(model).to_dict()
        resp, err = self.rpc_call("data/delete", ref)
        if err:
            log.error("failed to delete model: %s", err)
            return None
        return schema.Ref.from_dict(resp)

    def calculate(self, setup: results.CalculationSetup) -> Result:
        resp, err = self.rpc_call("result/calculate", setup.to_dict())
        if err:
            return Result(
                uid="", client=self, error=results.ResultState(id="", error=err)
            )
        state = results.ResultState.from_dict(resp)
        return Result(uid=state.id, client=self, error=None)

    def rpc_call(self, method: str, params) -> Tuple[Any, Optional[str]]:
        """
        Performs a JSON-RPC request with the given parameters.

        It returns a tuple (result, error).
        """
        req = {
            "jsonrpc": "2.0",
            "id": self.next_id,
            "method": method,
            "params": params,
        }
        self.next_id += 1
        resp: dict = requests.post(self.url, json=req).json()
        err: dict | None = resp.get("error")
        if err is not None:
            err_msg = "%i: %s" % (err.get("code"), err.get("message"))
            return None, err_msg
        result = resp.get("result")
        if result is None:
            return None, "No error and no result: invalid JSON-RPC response"
        return result, None
