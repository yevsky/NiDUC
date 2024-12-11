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

        # Data for SLA checks
        self.break_counts = []
        self.max_break_times = []
        self.average_repair_times = []
        self.annual_maintenance_costs = []

    def run(self) -> list[float]:
        """
        Runs the simulation over the specified simulation time.
        :returns: list[float]: list is availability for system over specified time
        """
        for _ in range(self.num_trials):
            (availability,
             total_breaks,
             max_break_time,
             avg_repair_time,
             maintenance_cost) = self.run_single_simulation()

            self.availability_results.append(availability)
            self.break_counts.append(total_breaks)
            self.max_break_times.append(max_break_time)
            self.average_repair_times.append(avg_repair_time)
            self.annual_maintenance_costs.append(maintenance_cost)

        return self.availability_results

    def run_single_simulation(self):
        current_time = 0.0
        last_event_time = 0.0
        total_operational_time = 0.0

        # Initialize system state: all components are operational
        self.system.failed_components = []

        # Metrics for SLA checks
        total_breaks = 0
        downtime_intervals = []
        current_downtime_start = None
        total_repair_time = 0.0
        repair_events_count = 0

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

            # Before processing the event, check if system was operational
            was_operational = self.system.is_operational()

            # Update the operational time if the system was operational
            if was_operational:
                operational_time = event_time - last_event_time
                total_operational_time += operational_time

            # Advance the current time
            current_time = event_time
            last_event_time = current_time

            # Process the event
            if event_type == 'failure':
                self.system.fail_component(component)
                total_breaks += 1

                # If the system just became non-operational, record start of downtime
                if was_operational and not self.system.is_operational():
                    current_downtime_start = current_time

                # Schedule a repair event
                r_time = component.generate_repair_time()
                repair_time = current_time + r_time
                event_queue.append((repair_time, 'repair', component))
            elif event_type == 'repair':
                self.system.repair_component(component)
                repair_events_count += 1
                total_repair_time += (event_time - (repair_time - component.repair_time))

                # If the system became operational now, record this downtime interval
                if self.system.is_operational() and current_downtime_start is not None:
                    downtime_length = current_time - current_downtime_start
                    downtime_intervals.append(downtime_length)
                    current_downtime_start = None

                # Schedule the next failure event
                next_failure_time = current_time + component.generate_failure_time()
                event_queue.append((next_failure_time, 'failure', component))

            # Re-sort the event queue
            event_queue.sort(key=lambda x: x[0])

        # After simulation ends, if system is still down, record that downtime
        if current_time < self.simulation_time and self.system.is_operational():
            operational_time = self.simulation_time - last_event_time
            total_operational_time += operational_time
        else:
            # If still down at the end of simulation, close off downtime interval
            if current_downtime_start is not None:
                downtime_length = self.simulation_time - current_downtime_start
                downtime_intervals.append(downtime_length)

        # Calculate the availability
        availability = total_operational_time / self.simulation_time

        # Determine max break time
        max_break_time = max(downtime_intervals) if downtime_intervals else 0.0

        # Average repair time
        average_repair_time = (total_repair_time / repair_events_count) if repair_events_count > 0 else 0.0

        # Compute annual maintenance cost (example: fixed overhead + cost per break)
        fixed_annual_overhead = 5000.0
        cost_per_break = 1000.0
        maintenance_cost = fixed_annual_overhead + total_breaks * cost_per_break

        return availability, total_breaks, max_break_time, average_repair_time, maintenance_cost
