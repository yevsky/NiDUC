from system import System

class Simulation:
    def __init__(self, system: System, simulation_time: float, num_trials: int = 1000,
                 simulation_step: float = 1) -> None:
        """
        Initializes the simulation.
        :param system: System to simulate
        :param simulation_time: Duration of each simulation run
        :param num_trials: number of trials simulation will run for. Default is 1000
        :param simulation_step: Step of simulation. Default value is 1
        """
        self.system = system
        self.simulation_time = simulation_time
        self.simulation_step = simulation_step
        self.num_trials = num_trials
        self.availability_results = []

    def run(self) -> list[float]:
        """
        Runs the simulation over the specified simulation time.
        :returns: list[float]: list is availability for system over specified time
        """
        for _ in range(self.num_trials):
            self.system.failed_components = []
            availability = self.run_single_simulation()
            self.availability_results.append(availability)
        return self.availability_results

    def run_single_simulation(self):
        current_time = 0.0
        last_event_time = 0.0
        total_operational_time = 0.0

        # Initialize system state: all components are operational
        self.system.failed_components = []

        # Initialize the event queue with the first failure time of each component
        event_queue = []
        for component in self.system.components:
            t_failure = component.generate_failure_time()
            event_queue.append((t_failure, 'failure', component))

        # Sort the event queue by event time
        event_queue.sort(key=lambda x: x[0])

        while current_time < self.simulation_time and event_queue:
            # Get the next event
            event_time, event_type, component = event_queue.pop(0)

            # If the event occurs after the simulation time, adjust the event time
            if event_time > self.simulation_time:
                event_time = self.simulation_time

            # Update the operational time if the system was operational
            if self.system.is_operational():
                operational_time = event_time - last_event_time
                total_operational_time += operational_time

            # Advance the current time
            current_time = event_time
            last_event_time = current_time

            # Process the event
            if event_type == 'failure':
                self.system.fail_component(component)
                # Schedule a repair event
                repair_time = current_time + component.generate_repair_time()
                event_queue.append((repair_time, 'repair', component))
            elif event_type == 'repair':
                self.system.repair_component(component)
                # Schedule the next failure event
                next_failure_time = current_time + component.generate_failure_time()
                event_queue.append((next_failure_time, 'failure', component))

            # Re-sort the event queue
            event_queue.sort(key=lambda x: x[0])

        # After the simulation ends, account for any remaining operational time
        if current_time < self.simulation_time and self.system.is_operational():
            operational_time = self.simulation_time - last_event_time
            total_operational_time += operational_time

        # Calculate the availability
        availability = total_operational_time / self.simulation_time
        return availability
