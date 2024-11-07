from components import Component
from system import System
from sla import SLA
from simulation import Simulation


def main() -> None:
    # Define components with their failure rates and repair times
    component1 = Component(name="Transformer", failure_rate=0.0001, repair_time=8.0)
    component2 = Component(name="Substation", failure_rate=0.00005, repair_time=6.0)
    component3 = Component(name="Distribution Line", failure_rate=0.0002, repair_time=4.0)

    components = [component1, component2, component3]

    # Create the system
    system = System(components=components)

    # Define the SLA requirement
    sla = SLA(required_availability=0.999)

    # Run the simulation over one year with hourly time steps
    simulation = Simulation(system=system, sla=sla, total_time=8760.0, time_step=1.0)
    simulation.run()


if __name__ == "__main__":
    main()
