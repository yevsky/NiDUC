from system import System
from sla import SLA


class Simulation:
    def __init__(
            self, system: System, sla: SLA, total_time: float, time_step: float
    ) -> None:
        self.system: System = system
        self.sla: SLA = sla
        self.total_time: float = total_time  # in hours
        self.time_step: float = time_step  # in hours
        self.current_time: float = 0.0
        self.uptime: float = 0.0

    def run(self) -> None:
        while self.current_time < self.total_time:
            if self.system.is_operational():
                self.uptime += self.time_step
            self.system.update(self.time_step)
            self.current_time += self.time_step

        availability: float = self.uptime / self.total_time
        sla_compliant: bool = self.sla.check_compliance(availability)
        print(f"System Availability: {availability:.2%}")
        print(f"SLA Compliance: {'Met' if sla_compliant else 'Not Met'}")
