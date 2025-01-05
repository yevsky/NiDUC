from system import System
from components import Component


class Simulation:
    def __init__(self, system: System, simulation_time: float, num_trials: int = 1000) -> None:
        """
        Initializes the simulation.
        :param system: System to simulate
        :param simulation_time: Duration of each simulation run
        :param num_trials: number of trials simulation will run for. Default is 1000
        :param simulation_step: Step of simulation. Default value is 1
        """
        self.system = system
        self.simulation_time = simulation_time
        self.num_trials = num_trials
        self.availability_results = []

        # Data for SLA checks
        self.break_counts = []
        self.total_break_times = []
        self.max_break_times = []
        self.revenue_punishments = []

    def run(self) -> tuple[list[float], list[int], list[float], list[float], list[float]]:
        """
        Runs the simulation over the specified simulation time.
        :returns: list[float]: list is availability for system over specified time
        """
        for _ in range(self.num_trials):
            (availability,
             total_breaks,
             total_break_time,
             max_break_time,
             revenue_lost,) = self.run_single_simulation()

            self.availability_results.append(availability)
            self.break_counts.append(total_breaks)
            self.total_break_times.append(total_break_time)
            self.max_break_times.append(max_break_time)
            self.revenue_punishments.append(revenue_lost)

        return self.availability_results, self.break_counts, self.total_break_times, self.max_break_times, self.revenue_punishments

    def run_single_simulation(self):
        current_time = 0.0
        last_event_time = 0.0
        total_operational_time = 0.0

        # Initialize system state: all components are operational
        self.system.failed_components = []

        # Metrics for SLA checks
        total_breaks = 0
        downtime_intervals = []
        current_downtime_start: float | None = None
        revenue_lost = 0.0

        # Flatten all components for event queue initialization
        all_components = [comp for group in self.system.groups for comp in group]

        event_queue = self.initialize_event_queue(all_components)

        while current_time < self.simulation_time and event_queue:
            # Get the next event
            event_time, event_type, component = event_queue.pop(0)
            event_time = min(event_time, self.simulation_time)

            # Before processing the event, check if system was operational
            was_operational = self.system.is_operational()

            # Update the operational time if the system was operational
            if was_operational:
                total_operational_time += event_time - last_event_time

            # Advance the current time
            current_time = event_time
            last_event_time = current_time

            # Process the event
            if event_type == 'failure':
                self.handle_failure_event(component, current_time, event_queue)
                total_breaks += 1
                revenue_lost += component.repair_cost
                # If the system just became non-operational, record start of downtime
                if was_operational and not self.system.is_operational():
                    current_downtime_start = current_time
            elif event_type == 'repair':
                self.handle_repair_event(component, current_time, event_queue)

                # If the system became operational now, record this downtime interval
                if self.system.is_operational() and current_downtime_start is not None:
                    downtime_length = current_time - current_downtime_start
                    downtime_intervals.append(downtime_length)
                    current_downtime_start = None

            # Re-sort the event queue
            event_queue.sort(key=lambda x: x[0])

        # After simulation ends, if system is still down, record that downtime
        if current_time < self.simulation_time and self.system.is_operational():
            total_operational_time += self.simulation_time - last_event_time
        elif current_downtime_start is not None:
            downtime_intervals.append(self.simulation_time - current_downtime_start)

        # Calculate the availability
        availability = total_operational_time / self.simulation_time

        # Determine total break time of a system
        total_break_time = sum(downtime_intervals, 0.0)

        # Determine the longest single downtime duration
        max_break_time = max(downtime_intervals, default=0.0)

        revenue_lost += (self.simulation_time - total_operational_time) * self.system.revenue_penalty_per_hour

        return availability, total_breaks, total_break_time, max_break_time, revenue_lost

    @staticmethod
    def initialize_event_queue(all_components: list[Component]) -> list[tuple[float, str, Component]]:
        """
        Initializes the event queue with the first failure time of each component.
        :param all_components: list of all components in the system
        :return: list of tuples representing events
        """
        event_queue = [(comp.generate_failure_time(), 'failure', comp) for comp in all_components]
        event_queue.sort(key=lambda x: x[0])

        return event_queue

    def handle_failure_event(self, component: Component, current_time: float,
                             event_queue: list[tuple[float, str, Component]]) -> None:
        """
        Handles a failure event for a component.
        :param component: Component that failed
        :param current_time: Current time in the simulation
        :param event_queue: List of events
        """
        self.system.fail_component(component)
        repair_time = current_time + component.generate_repair_time()
        event_queue.append((repair_time, 'repair', component))

    def handle_repair_event(self, component: Component, current_time: float,
                            event_queue: list[tuple[float, str, Component]]) -> None:
        """
        Handles a repair event for a component.
        :param component: Component that was repaired
        :param current_time: Current time in the simulation
        :param event_queue: List of events
        """
        self.system.repair_component(component)
        next_failure_time = current_time + component.generate_failure_time()
        event_queue.append((next_failure_time, 'failure', component))
