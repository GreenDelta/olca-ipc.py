import time

from abc import abstractmethod
from typing import TypeVar, Type

import olca_schema as schema
import olca_schema.results as res

E = TypeVar("E", bound=schema.RootEntity)


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
    def get_descriptors(self, model_type: Type[E]) -> list[schema.Ref]:
        pass

    @abstractmethod
    def get_descriptor(
        self, model_type: Type[E],
        uid: str | None = None,
        name: str | None = None,
    ) -> schema.Ref | None:
        pass

    def find(self, model_type: Type[E], name: str) -> schema.Ref | None:
        for d in self.get_descriptors(model_type):
            if d.name == name:
                return d

    @abstractmethod
    def get_providers(
        self, flow: schema.Ref | schema.Flow | None = None
    ) -> list[res.TechFlow]:
        pass

    @abstractmethod
    def get_parameters(
        self, model_type: Type[E], uid: str
    ) -> list[schema.Parameter | schema.ParameterRedef]:
        pass

    @abstractmethod
    def put(self, model: schema.RootEntity) -> schema.Ref | None:
        pass

    def put_all(self, *models: schema.RootEntity):
        for model in models:
            self.put(model)

    @abstractmethod
    def create_product_system(
        self,
        process: schema.Ref | schema.Process,
        config: schema.LinkingConfig | None = None,
    ) -> schema.Ref | None:
        pass

    @abstractmethod
    def delete(
        self, model: schema.RootEntity | schema.Ref
    ) -> schema.Ref | None:
        pass

    def delete_all(self, *models: schema.RootEntity | schema.Ref):
        for model in models:
            self.delete(model)

    @abstractmethod
    def calculate(self, setup: res.CalculationSetup) -> "IpcResult":
        pass


class IpcResult:
    @abstractmethod
    def get_state(self) -> res.ResultState:
        pass

    def wait_until_ready(self) -> res.ResultState:
        state = self.get_state()
        if not state.is_scheduled:
            return state
        while state.is_scheduled:
            time.sleep(0.5)
            state = self.get_state()
            if not state.is_scheduled:
                return state
        return res.ResultState(error="did not finished")

    @abstractmethod
    def dispose(self):
        pass

    @abstractmethod
    def get_demand(self) -> res.TechFlowValue | None:
        pass

    @abstractmethod
    def get_tech_flows(self) -> list[res.TechFlow]:
        pass

    @abstractmethod
    def get_envi_flows(self) -> list[res.EnviFlow]:
        pass

    @abstractmethod
    def get_impact_categories(self) -> list[schema.Ref]:
        pass

    @abstractmethod
    def get_total_requirements(self) -> list[res.TechFlowValue]:
        pass

    @abstractmethod
    def get_total_requirements_of(
        self, tech_flow: res.TechFlow
    ) -> res.TechFlowValue:
        pass

    @abstractmethod
    def get_total_flows(self) -> list[res.EnviFlowValue]:
        pass

    @abstractmethod
    def get_total_flow_value_of(
        self, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        pass

    @abstractmethod
    def get_flow_contributions_of(
        self, envi_flow: res.EnviFlow
    ) -> list[res.TechFlowValue]:
        pass

    @abstractmethod
    def get_direct_interventions_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        pass

    @abstractmethod
    def get_direct_intervention_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        pass

    @abstractmethod
    def get_flow_intensities_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlow]:
        pass

    @abstractmethod
    def get_flow_intensity_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        pass

    @abstractmethod
    def get_total_interventions_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.EnviFlowValue]:
        pass

    @abstractmethod
    def get_total_intervention_of(
        self, envi_flow: res.EnviFlow, tech_flow: res.TechFlow
    ) -> res.EnviFlowValue:
        pass

    # region: impacts

    @abstractmethod
    def get_total_impacts(self) -> list[res.ImpactValue]:
        pass

    @abstractmethod
    def get_total_impact_value_of(
        self, impact_category: schema.Ref
    ) -> res.ImpactValue:
        pass

    @abstractmethod
    def get_normalized_impacts(self) -> list[res.ImpactValue]:
        pass

    @abstractmethod
    def get_weighted_impacts(self) -> list[res.ImpactValue]:
        pass

    @abstractmethod
    def get_impact_contributions_of(
        self, impact_category: schema.Ref
    ) -> list[res.TechFlowValue]:
        pass

    @abstractmethod
    def get_direct_impacts_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        pass

    @abstractmethod
    def get_direct_impact_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        pass

    @abstractmethod
    def get_impact_intensities_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        pass

    @abstractmethod
    def get_impact_intensity_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        pass

    @abstractmethod
    def get_total_impacts_of(
        self, tech_flow: res.TechFlow
    ) -> list[res.ImpactValue]:
        pass

    @abstractmethod
    def get_total_impact_of(
        self, impact_category: schema.Ref, tech_flow: res.TechFlow
    ) -> res.ImpactValue:
        pass

    @abstractmethod
    def get_impact_factors_of(
        self, impact_category: schema.Ref
    ) -> list[res.EnviFlowValue]:
        pass

    @abstractmethod
    def get_impact_factor_of(
        self, impact_category: schema.Ref, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        pass

    @abstractmethod
    def get_flow_impacts_of(
        self, impact_category: schema.Ref
    ) -> list[res.EnviFlowValue]:
        pass

    @abstractmethod
    def get_flow_impact_of(
        self, impact_category: schema.Ref, envi_flow: res.EnviFlow
    ) -> res.EnviFlowValue:
        pass

    # endregion: impacts

    @abstractmethod
    def get_total_costs(self) -> res.CostValue:
        pass

    @abstractmethod
    def get_cost_contributions(self) -> list[res.TechFlowValue]:
        pass

    @abstractmethod
    def get_direct_costs_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        pass

    @abstractmethod
    def get_cost_intensities_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        pass

    @abstractmethod
    def get_total_costs_of(self, tech_flow: res.TechFlow) -> res.CostValue:
        pass
