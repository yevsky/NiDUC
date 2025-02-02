from components import Component
from simulation import Simulation
from system import System
from sla import SLA
from GUI.histograms import draw_histogram
import numpy as np


def run_sla_simulation(system: System, sla_thresholds: dict, simulation_time=1000.0, num_trials=1000):
    """
    Runs the simulation for the given system and SLA thresholds.
    Collects availability, breaks, max break time, repair times, and cost.
    Then checks if the system meets the SLA.
    """
    # Create SLA object
    sla = SLA(sla_level_name=sla_thresholds.get('name', 'SLA'), thresholds=sla_thresholds)

    # Run simulation
    simulation = Simulation(system, simulation_time, num_trials)
    availability_list, break_counts, total_break_time, max_break_time, revenue_punishments = simulation.run()

    # Compute averages for SLA checks
    avg_availability = float(np.average(availability_list))
    avg_breaks = int(np.average(break_counts))
    avg_total_break_time = float(np.average(total_break_time))
    avg_max_break_time = float(np.average(max_break_time))

    # Compute other metrics
    avg_revenue_punishment = float(np.average(revenue_punishments))

    # Check SLA compliance
    compliant = sla.is_sla_compliant(
        average_availability=avg_availability,
        total_breaks=avg_breaks,
        total_break_time=avg_total_break_time,
        max_break_time=avg_max_break_time
    )

    # Print results
    print(f"\n--- {sla_thresholds['name']} SLA Results ---")
    print(f"Average Availability: {avg_availability * 100:.2f}%")
    print(f"Average Number of Breaks: {avg_breaks:.2f}")
    print(f"Average Total Break Time: {avg_total_break_time:.2f} h")
    print(f"Average Max Break Time: {avg_max_break_time:.2f} h")
    print(f"Average Revenue Punishment: {avg_revenue_punishment:.2f}zł")
    print(f"SLA Compliant: {compliant}")

    # Optionally draw histogram for availability distribution
    draw_histogram(
        data=availability_list,
        bins=50,
        title=f"Availability Distribution for {sla_thresholds['name']} SLA",
        x_label="Availability",
        y_label="Frequency"
    )


def main() -> None:
    budget_sla_thresholds = {
        'name': 'Budget',
        'availability': 0.85,  # >90%
        'max_breaks': 500,  # <40
        'max_break_time': 100.0,  # <100 h
        'total_break_time': 500.0,  # <100 h
    }

    standard_sla_thresholds = {
        'name': 'Standard',
        'availability': 0.95,  # >95%
        'max_breaks': 20,  # <20
        'max_break_time': 50.0,  # <50 h
        'total_break_time': 50.0,  # <50 h
    }

    premium_sla_thresholds = {
        'name': 'Premium',
        'availability': 0.975,  # >97.5%
        'max_breaks': 10,  # <10
        'max_break_time': 25.0,  # <25 h
        'total_break_time': 25.0,  # <25 h
    }

    simulation_time = 2000.0
    num_trials = 1000

    # Define 3 different systems with different component configurations.
    # The idea is to choose component parameters that are likely to meet each SLA.

    # Budget system: Each component in its own group (no redundancy)
    budget_components = [
        Component(name="Budget_Server1", failure_rate=0.003, time_to_repair=10, repair_cost=100),
        Component(name="Budget_Server2", failure_rate=0.003, time_to_repair=11, repair_cost=100),
        Component(name="Budget_Server3", failure_rate=0.003, time_to_repair=10, repair_cost=100)
    ]
    budget_system = System(groups=[
        [budget_components[0]],
        [budget_components[1]],
        [budget_components[2]]
    ], revenue_penalty_per_hour=500)

    # Standard system: Each component in its own group (no redundancy)
    standard_components = [
        Component(name="Standard_Server1", failure_rate=0.002, time_to_repair=5, repair_cost=200),
        Component(name="Standard_Server2", failure_rate=0.001, time_to_repair=5, repair_cost=200),
        Component(name="Standard_Server3", failure_rate=0.0015, time_to_repair=5, repair_cost=200)
    ]
    standard_system = System(groups=[
        [standard_components[0]],
        [standard_components[1]],
        [standard_components[2]]
    ], revenue_penalty_per_hour=1000)

    # Premium system: One group with a main and alternative component, others single-component groups
    premium_main = Component(name="Premium_Server1", failure_rate=0.001, time_to_repair=2, repair_cost=300)
    premium_alt = Component(name="Premium_Server1_alt", failure_rate=0.001, time_to_repair=2, repair_cost=300)
    premium_other1 = Component(name="Premium_Server2", failure_rate=0.001, time_to_repair=2, repair_cost=300)
    premium_other2 = Component(name="Premium_Server3", failure_rate=0.001, time_to_repair=2, repair_cost=300)

    premium_system = System(groups=[
        [premium_main, premium_alt],  # Redundant group
        [premium_other1],
        [premium_other2]
    ], revenue_penalty_per_hour=1500)

    # Run simulations for each system
    run_sla_simulation(budget_system, budget_sla_thresholds, simulation_time, num_trials)
    run_sla_simulation(standard_system, standard_sla_thresholds, simulation_time, num_trials)
    run_sla_simulation(premium_system, premium_sla_thresholds, simulation_time, num_trials)


if __name__ == "__main__":
    main()
