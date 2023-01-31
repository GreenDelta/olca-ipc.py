import logging as log
from dataclasses import dataclass
from typing import cast, Any, Optional, Tuple, Type

import requests
import olca_schema as schema
import olca_schema.results as res

from .protocol import E, IpcProtocol, IpcResult


class Client(IpcProtocol):
    """
    A client to communicate with an openLCA IPC server over the JSON-RPC
    protocol.
    """

    def __init__(self, port: int = 8080):
        self.url = "http://localhost:%i" % port
        self.next_id = 1

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
        self, model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> schema.Ref | None:
        params = {"@type": model_type.__name__}
        if uid is not None:
            params["@id"] = uid
        if name is not None:
            params["name"] = name
        result, err = self.rpc_call("data/get/descriptor", params)
        if err:
            log.error("failed to get descriptor: %s", err)
            return None
        return schema.Ref.from_dict(result)

    def get_providers(
        self, flow: schema.Ref | schema.Flow | None = None
    ) -> list[res.TechFlow]:
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
        return [res.TechFlow.from_dict(d) for d in providers]

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
        config: schema.LinkingConfig | None = None,
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
                "process": schema.as_ref(process).to_dict(),
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

    def calculate(self, setup: res.CalculationSetup) -> "Result":
        resp, err = self.rpc_call("result/calculate", setup.to_dict())
        if err:
            return Result(
                uid="", client=self, error=res.ResultState(id="", error=err)
            )
        state = res.ResultState.from_dict(resp)
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
        resp: dict = requests.post(self.url, json=req).json()
        err: dict | None = resp.get("error")
        if err is not None:
            err_msg = "%i: %s" % (err.get("code"), err.get("message"))
            return None, err_msg
        result = resp.get("result")
        if result is None:
            return None, "No error and no result: invalid JSON-RPC response"
        return result, None


@dataclass
class Result(IpcResult):
    uid: str
    client: "Client"
    error: Optional[res.ResultState]

    def get_state(self) -> res.ResultState:
        if self.error is not None:
            return self.error
        (state, err) = self.client.rpc_call("result/state", {"@id": self.uid})
        if err:
            return res.ResultState(id=self.uid, error=err)
        return res.ResultState.from_dict(state)

    def dispose(self):
        if self.error is not None:
            return
        self.client.rpc_call("result/dispose", {"@id": self.uid})

    def get_demand(self) -> res.TechFlowValue | None:
        (data, err) = self.client.rpc_call("result/demand", {"@id": self.uid})
        if err:
            log.error("failed to get demand: %s", err)
            return None
        return res.TechFlowValue.from_dict(data)

    def get_tech_flows(self) -> list[res.TechFlow]:
        (data, err) = self.client.rpc_call(
            "result/tech-flows", {"@id": self.uid}
        )
        if err:
            log.error("failed to query /tech-flows: %s", err)
            return []
        return [res.TechFlow.from_dict(d) for d in data]

    def get_envi_flows(self) -> list[res.EnviFlow]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/envi-flows", args)
        if err:
            log.error("request envi-flows failed: %s", err)
            return []
        return [res.EnviFlow.from_dict(d) for d in r]

    def get_impact_categories(self) -> list[schema.Ref]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/impact-categories", args)
        if err:
            log.error("request impact-categories failed: %s", err)
            return []
        return [schema.Ref.from_dict(d) for d in r]

    def get_total_requirements(self) -> list[res.TechFlowValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-requirements", args)
        if err:
            log.error("request total-requirements failed: %s", err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_total_requirements_of(
        self, tech_flow: res.TechFlow
    ) -> res.TechFlowValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-requirements-of", args)
        if err:
            log.error("request total-requirements-of failed: %s", err)
            return res.TechFlowValue(amount=0, tech_flow=tech_flow)
        return res.TechFlowValue.from_dict(r)

    # region: flows

    def get_total_flows(self) -> list[res.EnviFlowValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-flows", args)
        if err:
            log.error("request total-flows failed: %s", err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_flow_value_of(
        self, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        args = {"@id": self.uid, "enviFlow": envi_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-flow-value-of", args)
        if err:
            log.error("request total-flow-value-of failed: %s", err)
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return res.EnviFlowValue.from_dict(r)

    def get_flow_contributions_of(
        self, envi_flow: res.EnviFlow
    ) -> list[res.TechFlowValue]:
        args = {"@id": self.uid, "enviFlow": envi_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/flow-contributions-of", args)
        if err:
            log.error("request direct-flow-values-of failed: %s", err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_direct_interventions_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/direct-interventions-of", args)
        if err:
            log.error("request direct-flows-of failed: %s", err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_direct_intervention_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/direct-intervention-of", args)
        if err:
            log.error("request direct-flow-of failed: %s", err)
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return res.EnviFlowValue.from_dict(r)

    def get_flow_intensities_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/flow-intensities-of", args)
        if err:
            log.error("request total-flows-of-one failed: %s", err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_flow_intensity_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/flow-intensity-of", args)
        if err:
            log.error("request total-flow-of-one failed: %s", err)
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return res.EnviFlowValue.from_dict(r)

    def get_total_interventions_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-interventions-of", args)
        if err:
            log.error("request total-flows-of failed: %s", err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_total_intervention_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        args = {
            "@id": self.uid,
            "enviFlow": envi_flow.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/total-intervention-of", args)
        if err:
            log.error("request total-flow-of failed: %s", err)
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return res.EnviFlowValue.from_dict(r)

    # endregion: flows

    def get_total_impacts(self) -> list[res.ImpactValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-impacts", args)
        if err:
            log.error("request total-impacts failed: %s", err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_value_of(
        self, impact_category: schema.Ref
    ) -> res.ImpactValue:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/total-impact-value-of", args)
        if err:
            log.error("request total-impact-value-of failed: %s", err)
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return res.ImpactValue.from_dict(r)

    def get_normalized_impacts(self) -> list[res.ImpactValue]:
        (r, err) = self.client.rpc_call(
            "result/total-impacts/normalized", {"@id": self.uid}
        )
        if err:
            log.error("failed to get normalized impacts: %s", err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_weighted_impacts(self) -> list[res.ImpactValue]:
        (r, err) = self.client.rpc_call(
            "result/total-impacts/weighted", {"@id": self.uid}
        )
        if err:
            log.error("failed to get weighted impacts: %s", err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_impact_contributions_of(
        self, impact_category: schema.Ref
    ) -> list[res.TechFlowValue]:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/impact-contributions-of", args)
        if err:
            log.error("request direct-impact-values-of failed: %s", err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_direct_impacts_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/direct-impacts-of", args)
        if err:
            log.error("request direct-impacts-of failed: %s", err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_direct_impact_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/direct-impact-of", args)
        if err:
            log.error("request direct-impact-of failed: %s", err)
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return res.ImpactValue.from_dict(r)

    def get_impact_intensities_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-impacts-of-one", args)
        if err:
            log.error("request total-impacts-of-one failed: %s", err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_impact_intensity_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/impact-intensity-of", args)
        if err:
            log.error("request total-impact-of-one failed: %s", err)
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return res.ImpactValue.from_dict(r)

    def get_total_impacts_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-impacts-of", args)
        if err:
            log.error("request total-impacts-of failed: %s", err)
            return []
        return [res.ImpactValue.from_dict(d) for d in r]

    def get_total_impact_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "techFlow": tech_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/total-impact-of", args)
        if err:
            log.error("request total-impact-of failed: %s", err)
            return res.ImpactValue(amount=0, impact_category=impact_category)
        return res.ImpactValue.from_dict(r)

    def get_impact_factors_of(
        self, impact_category: schema.Ref
    ) -> list[res.EnviFlowValue]:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/impact-factors-of", args)
        if err:
            log.error("request impact-factors-of failed: %s", err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_impact_factor_of(
        self, impact_category: schema.Ref, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "enviFlow": envi_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/impact-factor-of", args)
        if err:
            log.error("request impact-factor-of failed: %s", err)
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return res.EnviFlowValue.from_dict(r)

    def get_flow_impacts_of(
        self, impact_category: schema.Ref
    ) -> list[res.EnviFlowValue]:
        args = {"@id": self.uid, "impactCategory": impact_category.to_dict()}
        (r, err) = self.client.rpc_call("result/flow-impacts-of", args)
        if err:
            log.error("request flow-impacts-of failed: %s", err)
            return []
        return [res.EnviFlowValue.from_dict(d) for d in r]

    def get_flow_impact_of(
        self, impact_category: schema.Ref, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        args = {
            "@id": self.uid,
            "impactCategory": impact_category.to_dict(),
            "enviFlow": envi_flow.to_dict(),
        }
        (r, err) = self.client.rpc_call("result/flow-impact-of", args)
        if err:
            log.error("request flow-impact-of failed: %s", err)
            return res.EnviFlowValue(amount=0, envi_flow=envi_flow)
        return res.EnviFlowValue.from_dict(r)

    def get_total_costs(self) -> res.CostValue:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/total-costs", args)
        if err:
            log.error("request total-costs failed: %s", err)
            return res.CostValue(amount=0)
        return res.CostValue.from_dict(r)

    def get_cost_contributions(self) -> list[res.TechFlowValue]:
        args = {"@id": self.uid}
        (r, err) = self.client.rpc_call("result/cost-contributions", args)
        if err:
            log.error("request direct-cost-values failed: %s", err)
            return []
        return [res.TechFlowValue.from_dict(d) for d in r]

    def get_direct_costs_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/direct-costs-of", args)
        if err:
            log.error("request direct-costs-of failed: %s", err)
            return res.CostValue(amount=0)
        return res.CostValue.from_dict(r)

    def get_cost_intensities_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/cost-intensities-of", args)
        if err:
            log.error("request total-costs-of-one failed: %s", err)
            return res.CostValue(amount=0)
        return res.CostValue.from_dict(r)

    def get_total_costs_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        args = {"@id": self.uid, "techFlow": tech_flow.to_dict()}
        (r, err) = self.client.rpc_call("result/total-costs-of", args)
        if err:
            log.error("request total-costs-of failed: %s", err)
            return res.CostValue(amount=0)
        return res.CostValue.from_dict(r)
