from components import Component
from simulation import Simulation
from system import System
from sla import SLA
from GUI.histograms import draw_histogram


def main() -> None:
    component1 = Component(name="Server1", failure_rate=0.01, time_to_repair=9)
    component2 = Component(name="Server2", failure_rate=0.02, time_to_repair=10)

    system = System(components=[component1, component2])

    sla_thresholds = {'availability': 0.95}
    sla = SLA(sla_level_name="Standard", thresholds=sla_thresholds)

    simulation_time = 1000
    simulation = Simulation(system, simulation_time)
    uptime, downtime = simulation.run()

    availability = sla.calculate_availability(uptime, simulation_time)

    print(f"Total Uptime: {uptime}")
    print(f"Total Downtime: {downtime}")
    print(f"Availability: {availability}")
    print(f"SLA Compliance: {sla.is_sla_compliant()}")

    draw_histogram(x_label="Time", y_label="Availability",x=[4,2],y=[2,4] )


if __name__ == "__main__":
    main()
