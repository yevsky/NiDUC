from src.components import Component
from system import System
import random

class Simulation:
    def __init__(self, system: System, simulation_time: float, trials: int) -> None:
        """
        Initializes the simulation with multiple trials for histogram data.
        :param system: (System): System to simulate
        :param simulation_time: (float): Duration of each simulation run
        :param trials: (int): Number of trials to run
        """
        self.system = system
        self.simulation_time = simulation_time
        self.trials = trials
        self.reliability_data = []  # List to store uptime percentages for each trial

    def run(self) -> list[float]:
        """
        Runs multiple trials of the simulation and collects reliability data.
        :return: (list[float]): List of uptime percentages for each trial
        """
        for _ in range(self.trials):
            total_uptime, total_downtime = self._run_single_simulation()
            uptime_percentage = total_uptime / self.simulation_time  # Calculate uptime percentage
            self.reliability_data.append(uptime_percentage)
        return self.reliability_data

    def _run_single_simulation(self) -> tuple[float, float]:
        """
        Runs a single simulation trial.
        :return: (tuple[float, float]): Tuple containing total uptime and total downtime
        """
        current_time = 0
        total_downtime = 0

        while current_time < self.simulation_time:
            # Choosing a component that will fail
            component: Component = random.choice(self.system.components)
            failure_time = component.generate_failure_time()
            repair_time = component.generate_repair_time()

            if current_time + failure_time > self.simulation_time:
                break

            # Component failure simulation
            self.system.fail_component(component)
            total_downtime += repair_time

            # Component repair simulation
            self.system.repair_component(component)
            current_time += failure_time + repair_time

        total_uptime = self.simulation_time - total_downtime
        return total_uptime, total_downtime
