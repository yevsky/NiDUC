from components import Component
from simulation import Simulation
from system import System
from sla import SLA
from GUI.histograms import draw_histogram
import numpy as np


def main() -> None:
    # Primary and alternative components for group 1
    primary1 = Component(name="Server1", failure_rate=0.005, time_to_repair=6)
    alternative1 = Component(name="Server1_alt", failure_rate=0.006, time_to_repair=5)

    # Only one component in group 2 (no redundancy here)
    primary2 = Component(name="Server2", failure_rate=0.004, time_to_repair=4)

    system = System(groups=[
        [primary1, alternative1],
        [primary2]
    ])

    sla_thresholds = {'availability': 0.95,
                      'max_breaks': 20,
                      'max_break_time': 50.0,
                      'average_repair_time': 6.0,
                      'max_cost_per_year': 950000.0
                      }
    sla = SLA(sla_level_name="Standard", thresholds=sla_thresholds)

    simulation_time = 1000.0
    num_trials = 1000
    simulation = Simulation(system, simulation_time, num_trials)

    availability = simulation.run()

    # Compute averages for SLA checks
    avg_availability = float(np.average(availability))
    avg_breaks = np.average(simulation.break_counts)
    avg_max_break_time = np.average(simulation.max_break_times)
    avg_repair_time = np.average(simulation.average_repair_times)
    avg_cost = np.average(simulation.annual_maintenance_costs)

    compliant = sla.is_sla_compliant(
        average_availability=avg_availability,
        total_breaks=avg_breaks,
        max_break_time=avg_max_break_time,
        average_repair_time=avg_repair_time,
        annual_maintenance_cost=avg_cost
    )

    print(f"Average Availability: {avg_availability}")
    print(f"Average Number of Breaks: {avg_breaks}")
    print(f"Average Maximum Break Time: {avg_max_break_time}")
    print(f"Average Repair Time: {avg_repair_time}")
    print(f"Average Annual Maintenance Cost: {avg_cost}")
    print(f"SLA Compliant: {compliant}")

    draw_histogram(data=availability, bins=50, title="Availability over multiple simulations", x_label="Availability",
                   y_label="Frequency")


if __name__ == "__main__":
    main()
