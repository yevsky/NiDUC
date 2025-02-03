import json
from components import Component
from simulation import Simulation
from src.GUI.histograms import draw_sla_histogram
from system import System
from sla import SLA
from GUI.histograms import draw_histogram
import numpy as np


def load_sla_config(config_file):
    """
    Loads the SLA configuration from a JSON file.
    :param config_file: path to the SLA configuration file
    :return: a dictionary containing the SLA configuration
    """
    with open(config_file, 'r') as file:
        return json.load(file)


def create_system_from_config(config):
    """
    Creates a system object based on the provided configuration.
    :param config: a dictionary containing system configuration including components and penalty rate
    :return: a System object with initialized components
    """
    components = [
        [Component(name=c["name"], failure_rate=c["failure_rate"], time_to_repair=c["time_to_repair"], repair_cost=c["repair_cost"]) for c in group]
        for group in config["components"]
    ]
    return System(groups=components, revenue_penalty_per_hour=config["revenue_penalty_per_hour"])


def run_sla_simulation(system: System, sla_thresholds: dict, simulation_time=24.0, num_trials=1000):
    """
    Runs the SLA simulation for the provided system based on given SLA thresholds.
    :param system: the System object representing the infrastructure to simulate
    :param sla_thresholds: the SLA thresholds that the system is expected to meet
    :param simulation_time: total time for the simulation in hours (default 24.0)
    :param num_trials: number of simulation trials to run (default 1000)
    :return: average values for breaks, break time, max break time, and revenue punishment
    """
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
    """
    Main function that loads the SLA configuration, runs simulations for different system configurations,
    and visualizes the results.
    """
    sla_config = load_sla_config('sla_config.json')
    simulation_time = 2000.0
    num_trials = 1000

    systems = {
        "Budget": create_system_from_config(sla_config["budget"]),
        "Standard": create_system_from_config(sla_config["standard"]),
        "Premium": create_system_from_config(sla_config["premium"])
    }

    results = {}
    for sla_name, system in systems.items():
        results[sla_name] = run_sla_simulation(system, sla_config[sla_name.lower()], simulation_time, num_trials)

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
