import time

from abc import abstractmethod
from typing import TypeVar, Type

import olca_schema as o

E = TypeVar("E", bound=o.RootEntity)


class IpcProtocol:
    @abstractmethod
    def get(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> E | None:
        pass

    @abstractmethod
    def get_all(self, model_type: Type[E]) -> list[E]:
        pass

    @abstractmethod
    def get_descriptors(self, model_type: Type[E]) -> list[o.Ref]:
        pass

    @abstractmethod
    def get_descriptor(
        self,
        model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> o.Ref | None:
        pass

    def find(self, model_type: Type[E], name: str) -> o.Ref | None:
        for d in self.get_descriptors(model_type):
            if d.name == name:
                return d

    @abstractmethod
    def get_providers(
        self, flow: o.Ref | o.Flow | None = None
    ) -> list[o.TechFlow]:
        pass

    @abstractmethod
    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[o.Parameter | o.ParameterRedef]:
        pass

    @abstractmethod
    def put(self, model: o.RootEntity) -> o.Ref | None:
        pass

    def put_all(self, *models: o.RootEntity):
        for model in models:
            self.put(model)

    @abstractmethod
    def create_product_system(
        self,
        process: o.Ref | o.Process,
        config: o.LinkingConfig | None = None,
    ) -> o.Ref | None:
        pass

    @abstractmethod
    def delete(self, model: o.RootEntity | o.Ref) -> o.Ref | None:
        pass

    def delete_all(self, *models: o.RootEntity | o.Ref):
        for model in models:
            self.delete(model)

    @abstractmethod
    def calculate(self, setup: o.CalculationSetup) -> "IpcResult":
        pass

    @abstractmethod
    def simulate(self, setup: o.CalculationSetup) -> "IpcResult":
        pass


class IpcResult:
    @abstractmethod
    def get_state(self) -> o.ResultState:
        pass

    @abstractmethod
    def simulate_next(self) -> o.ResultState:
        pass

    def wait_until_ready(self) -> o.ResultState:
        state = self.get_state()
        if not state.is_scheduled:
            return state
        while state.is_scheduled:
            time.sleep(0.5)
            state = self.get_state()
            if not state.is_scheduled:
                return state
        return o.ResultState(error="did not finished")

    @abstractmethod
    def dispose(self):
        pass

    @abstractmethod
    def get_demand(self) -> o.TechFlowValue | None:
        pass

    @abstractmethod
    def get_tech_flows(self) -> list[o.TechFlow]:
        pass

    @abstractmethod
    def get_envi_flows(self) -> list[o.EnviFlow]:
        pass

    @abstractmethod
    def get_impact_categories(self) -> list[o.Ref]:
        pass

    # region: tech-flows

    @abstractmethod
    def get_total_requirements(self) -> list[o.TechFlowValue]:
        pass

    @abstractmethod
    def get_total_requirements_of(
        self, tech_flow: o.TechFlow
    ) -> o.TechFlowValue:
        pass

    @abstractmethod
    def get_scaling_factors(self) -> list[o.TechFlowValue]:
        pass

    @abstractmethod
    def get_scaled_tech_flows_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        pass

    @abstractmethod
    def get_unscaled_tech_flows_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.TechFlowValue]:
        pass

    # endregion

    # region: inventory results

    @abstractmethod
    def get_total_flows(self) -> list[o.EnviFlowValue]:
        pass

    @abstractmethod
    def get_total_flow_value_of(self, envi_flow: o.EnviFlow) -> o.EnviFlowValue:
        pass

    @abstractmethod
    def get_flow_contributions_of(
        self, envi_flow: o.EnviFlow
    ) -> list[o.TechFlowValue]:
        pass

    @abstractmethod
    def get_direct_interventions_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        pass

    @abstractmethod
    def get_direct_intervention_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        pass

    @abstractmethod
    def get_flow_intensities_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlow]:
        pass

    @abstractmethod
    def get_flow_intensity_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        pass

    @abstractmethod
    def get_total_interventions_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.EnviFlowValue]:
        pass

    @abstractmethod
    def get_total_intervention_of(
        self, envi_flow: o.EnviFlow, tech_flow: o.TechFlow
    ) -> o.EnviFlowValue:
        pass

    @abstractmethod
    def get_upstream_interventions_of(
        self, envi_flow: o.EnviFlow, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        pass

    # endregion

    # region: impacts

    @abstractmethod
    def get_total_impacts(self) -> list[o.ImpactValue]:
        pass

    @abstractmethod
    def get_total_impact_value_of(
        self, impact_category: o.Ref
    ) -> o.ImpactValue:
        pass

    @abstractmethod
    def get_normalized_impacts(self) -> list[o.ImpactValue]:
        pass

    @abstractmethod
    def get_weighted_impacts(self) -> list[o.ImpactValue]:
        pass

    @abstractmethod
    def get_impact_contributions_of(
        self, impact_category: o.Ref
    ) -> list[o.TechFlowValue]:
        pass

    @abstractmethod
    def get_direct_impacts_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        pass

    @abstractmethod
    def get_direct_impact_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        pass

    @abstractmethod
    def get_impact_intensities_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        pass

    @abstractmethod
    def get_impact_intensity_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        pass

    @abstractmethod
    def get_total_impacts_of(
        self, tech_flow: o.TechFlow
    ) -> list[o.ImpactValue]:
        pass

    @abstractmethod
    def get_total_impact_of(
        self, impact_category: o.Ref, tech_flow: o.TechFlow
    ) -> o.ImpactValue:
        pass

    @abstractmethod
    def get_impact_factors_of(
        self, impact_category: o.Ref
    ) -> list[o.EnviFlowValue]:
        pass

    @abstractmethod
    def get_impact_factor_of(
        self, impact_category: o.Ref, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue:
        pass

    @abstractmethod
    def get_flow_impacts_of(
        self, impact_category: o.Ref
    ) -> list[o.EnviFlowValue]:
        pass

    @abstractmethod
    def get_flow_impact_of(
        self, impact_category: o.Ref, envi_flow: o.EnviFlow
    ) -> o.EnviFlowValue:
        pass

    @abstractmethod
    def get_upstream_impacts_of(
        self, impact_category: o.Ref, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        pass

    # endregion

    # region: costs

    @abstractmethod
    def get_total_costs(self) -> o.CostValue:
        pass

    @abstractmethod
    def get_cost_contributions(self) -> list[o.TechFlowValue]:
        pass

    @abstractmethod
    def get_direct_costs_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        pass

    @abstractmethod
    def get_cost_intensities_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        pass

    @abstractmethod
    def get_total_costs_of(self, tech_flow: o.TechFlow) -> o.CostValue:
        pass

    @abstractmethod
    def get_upstream_cost_of(
        self, path: list[o.TechFlow]
    ) -> list[o.UpstreamNode]:
        pass

    # endregion

    @abstractmethod
    def get_sankey_graph(self, config: o.SankeyRequest) -> o.SankeyGraph:
        pass
