from src.components import Component
from system import System
from sla import SLA
import random


class Simulation:
    def __init__(self, system: System, simulation_time: float) -> None:
        """
        Runs simulation for provided system
        :param system: (System): system that will run on
        :param simulation_time: (float): time for testing the system
        """
        self.system = system
        self.simulation_time = simulation_time
        self.total_uptime = 0
        self.total_downtime = 0

    def run(self) -> tuple[float, float]:
        """
        runs a simulation
        :return: (tuple[float, float]): tuple which contains total_uptime and total_downtime of system
        """
        current_time = 0
        while current_time < self.simulation_time:
            # Choosing a component that will fail
            component: Component = random.choice(self.system.components)
            failure_time = component.generate_failure_time()
            repair_time = component.generate_repair_time()

            if current_time + failure_time > self.simulation_time:
                break

            # Component failure simulation
            self.system.fail_component(component)
            self.total_downtime += repair_time

            # Component repair simulation
            self.system.repair_component(component)
            current_time += failure_time + repair_time

        self.total_uptime = self.simulation_time - self.total_downtime
        return self.total_uptime, self.total_downtime
