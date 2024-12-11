from components import Component


class System:
    def __init__(self, groups: list[list[Component]]) -> None:
        """
        Initialize the system with redundancy groups.
        Each element in `groups` is a list of components that are considered redundant.
        The system is operational as long as at least one component in each group is up.
        :param groups: A list of lists of components representing redundancy groups.
        """
        self.groups = groups
        self.failed_components: list[Component] = []

    def is_operational(self) -> bool:
        """
        The system is operational if each group has at least one functioning component.
        """
        for group in self.groups:
            # Check if the entire group is failed
            if all(component in self.failed_components for component in group):
                return False

        return True

    def fail_component(self, component: Component) -> None:
        """
        Adds component to list of failed components
        :param component: component that failed
        """
        if component not in self.failed_components:
            self.failed_components.append(component)

    def repair_component(self, component: Component) -> None:
        """
        Removes component from failed components list simulating that it was repaired
        :param component: component that was repaired
        """
        if component in self.failed_components:
            self.failed_components.remove(component)
