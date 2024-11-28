from components import Component
from simulation import Simulation
from system import System
from sla import SLA
from GUI.histograms import draw_histogram
import numpy as np


def main() -> None:
    component1 = Component(name="Server1", failure_rate=0.005, time_to_repair=9)
    component2 = Component(name="Server2", failure_rate=0.004, time_to_repair=10)

    system = System(components=[component1, component2])

    sla_thresholds = {'availability': 0.95}
    sla = SLA(sla_level_name="Standard", thresholds=sla_thresholds)

    simulation_time = 1000
    simulation = Simulation(system, simulation_time, trials=100)
    reliability_data = simulation.run()

    print(f"SLA Compliance: {sla.is_sla_compliant(np.average(reliability_data))}")

    draw_histogram(data=reliability_data, bins=20)


if __name__ == "__main__":
    main()
