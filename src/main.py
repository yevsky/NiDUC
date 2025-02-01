import json
from components import Component
from simulation import Simulation
from src.GUI.histograms import draw_sla_histogram
from system import System
from sla import SLA
from GUI.histograms import draw_histogram
import numpy as np


def load_sla_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)


def run_sla_simulation(system: System, sla_thresholds: dict, simulation_time=1000.0, num_trials=1000):
    sla = SLA(sla_level_name=sla_thresholds.get('name', 'SLA'), thresholds=sla_thresholds)
    simulation = Simulation(system, simulation_time, num_trials)
    availability_list, break_counts, total_break_time, max_break_time, revenue_punishments = simulation.run()

    avg_availability = float(np.average(availability_list))
    avg_breaks = int(np.average(break_counts))
    avg_total_break_time = float(np.average(total_break_time))
    avg_max_break_time = float(np.average(max_break_time))
    avg_revenue_punishment = float(np.average(revenue_punishments))

    compliant = sla.is_sla_compliant(
        average_availability=avg_availability,
        total_breaks=avg_breaks,
        total_break_time=avg_total_break_time,
        max_break_time=avg_max_break_time
    )

    print(f"\n--- {sla_thresholds['name']} SLA Results ---")
    print(f"Average Availability: {avg_availability * 100:.2f}%")
    print(f"Average Number of Breaks: {avg_breaks:.2f}")
    print(f"Average Total Break Time: {avg_total_break_time:.2f} h")
    print(f"Average Max Break Time: {avg_max_break_time:.2f} h")
    print(f"Average Revenue Punishment: {avg_revenue_punishment:.2f}zł")
    print(f"SLA Compliant: {compliant}")

    draw_histogram(
        data=availability_list,
        bins=50,
        title=f"Availability Distribution for {sla_thresholds['name']} SLA",
        x_label="Availability",
        y_label="Frequency"
    )

    return avg_breaks, avg_total_break_time, avg_max_break_time, avg_revenue_punishment


def main():
    sla_thresholds = load_sla_config('sla_config.json')
    simulation_time = 2000.0
    num_trials = 1000

    systems = {
        "Budget": System(
            groups=[[Component(name="Budget_Server1", failure_rate=0.01, time_to_repair=10, repair_cost=100)],
                    [Component(name="Budget_Server2", failure_rate=0.01, time_to_repair=11, repair_cost=100)],
                    [Component(name="Budget_Server3", failure_rate=0.008, time_to_repair=10, repair_cost=100)]],
            revenue_penalty_per_hour=500),
        "Standard": System(
            groups=[[Component(name="Standard_Server1", failure_rate=0.005, time_to_repair=5, repair_cost=200)],
                    [Component(name="Standard_Server2", failure_rate=0.004, time_to_repair=5, repair_cost=200)],
                    [Component(name="Standard_Server3", failure_rate=0.004, time_to_repair=5, repair_cost=200)]],
            revenue_penalty_per_hour=1000),
        "Premium": System(
            groups=[[Component(name="Premium_Server1", failure_rate=0.001, time_to_repair=2, repair_cost=300),
                     Component(name="Premium_Server1_alt", failure_rate=0.001, time_to_repair=2, repair_cost=300)],
                    [Component(name="Premium_Server2", failure_rate=0.001, time_to_repair=2, repair_cost=300)],
                    [Component(name="Premium_Server3", failure_rate=0.001, time_to_repair=2, repair_cost=300)]],
            revenue_penalty_per_hour=1500)
    }

    results = {}
    for sla_name, system in systems.items():
        results[sla_name] = run_sla_simulation(system, sla_thresholds[sla_name.lower()], simulation_time, num_trials)

    metrics = ["Average Number of Breaks", "Average Total Break Time", "Average Max Break Time",
               "Average Revenue Punishment"]
    colors = ["red", "green", "magenta", "purple"]

    for i, metric in enumerate(metrics):
        draw_sla_histogram(
            sla_names=list(results.keys()),
            values=[res[i] for res in results.values()],
            title=metric,
            x_label='SLA Level',
            y_label=metric,
            color=colors[i]
        )


if __name__ == "__main__":
    main()
