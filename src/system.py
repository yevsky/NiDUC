from components import Component


class System:
    def __init__(self, components: list[Component]) -> None:
        """
        Initialize system with given components
        :param components: List of components in system
        """
        self.components = components
        self.failed_components: list[Component] = []

    def is_operational(self) -> bool:
        """
        Determines if system is operational. The system is operational as long as all components are operational
        :return: bool: is system operational
        """
        return len(self.failed_components) == 0

    def fail_component(self, component: Component) -> None:
        """
        Adds component to list of failed components
        :param component: component that failed
        """
        self.failed_components.append(component)

    def repair_component(self, component: Component) -> None:
        """
        Removes component from failed components list simulating that it was repaired
        :param component: component that was repaired
        """
        self.failed_components.remove(component)
