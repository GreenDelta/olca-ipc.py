import time

from abc import abstractmethod
from typing import TypeVar, Type

import olca_schema as schema
import olca_schema.results as res

E = TypeVar("E", bound=schema.RootEntity)


class IpcProtocol:
    @abstractmethod
    def get(self, model_type: Type[E], uid="", name="") -> E | None:
        pass

    @abstractmethod
    def get_all(self, model_type: Type[E]) -> list[E]:
        pass

    @abstractmethod
    def get_descriptors(self, model_type: Type[E]) -> list[schema.Ref]:
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
    def get_descriptor(
        self, model_type: Type[E], uid="", name=""
    ) -> schema.Ref | None:
        pass

    @abstractmethod
    def put(self, model: schema.RootEntity) -> schema.Ref | None:
        pass

    def put_all(self, *models: schema.RootEntity):
        for model in models:
            self.put(model)

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
    def get_demand(self) -> res.TechFlowValue:
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
    def get_total_requirements_of(self, tech_flow: res.TechFlow) -> float:
        pass

    @abstractmethod
    def get_total_flows(self) -> list[res.EnviFlowValue]:
        pass

    @abstractmethod
    def get_total_flow_value_of(self, envi_flow: res.EnviFlow) -> float:
        pass

    @abstractmethod
    def get_direct_flow_values_of(
        self, envi_flow: res.EnviFlow
    ) -> list[res.TechFlowValue]:
        pass

    @abstractmethod
    def get_total_flow_values_of(
        self, envi_flow: res.EnviFlow
    ) -> list[res.TechFlowValue]:
        pass
