from typing import List
from components import Component


class System:
    def __init__(self, components: List[Component]) -> None:
        self.components: List[Component] = components

    def is_operational(self) -> bool:
        # The system is operational if all components are operational
        return all(component.is_operational for component in self.components)

    def update(self, delta_time: float) -> None:
        for component in self.components:
            component.update(delta_time)
